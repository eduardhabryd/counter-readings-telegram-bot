import asyncio
import logging
import sys
import os
from os import getenv
import requests

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, PhotoSize
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from utils.utils import messages_text, Form, Language
from db.manager import create_or_update_user

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
lang_type = Language("eng")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Load Google API credentials from JSON file
creds_filename = 'creds.json'
creds = None
if os.path.exists(creds_filename):
    creds = Credentials.from_authorized_user_file(creds_filename)

drive_service = build('drive', 'v3', credentials=creds)

sheets_service = build('sheets', 'v4', credentials=creds)


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.lang)
    kb = [
        [types.KeyboardButton(text="🇬🇧 English")],
        [types.KeyboardButton(text="🇺🇦 Ukrainian")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Choose your language"
    )
    await message.answer("What language do you prefer?", reply_markup=keyboard)


@dp.message(Form.lang)
async def language_state(message: Message, state: FSMContext) -> None:
    if message.text == "🇺🇦 Ukrainian":
        lang_type.set_lang("ukr")

    await state.set_data(
        {
            "telegram_user_id": message.from_user.id,
            "language": lang_type.get_lang()
        }
    )

    replies = messages_text[lang_type.get_lang()]
    greetings = replies["greetings"]

    await message.reply(greetings, reply_markup=types.ReplyKeyboardRemove())
    await message.answer(replies["address"], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.address)


@dp.message(Form.address)
async def command_address(message: Message, state: FSMContext) -> None:
    replies = messages_text[lang_type.get_lang()]
    address = message.text
    await state.update_data(address=address)
    await message.answer(replies["account"], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.account)


@dp.message(Form.account)
async def account_state(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    telegram_user_id = data.get("telegram_user_id")
    language = data.get("language")
    address = data.get("address")
    account = message.text
    await create_or_update_user(telegram_user_id, language, address, account)
    print(data, account)
    replies = messages_text[lang_type.get_lang()]
    await message.answer(replies["image"], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.counter_image)


@dp.message(Form.counter_image)
async def command_counter(message: Message, state: FSMContext) -> None:
    # Assuming the user sends a photo
    photo: PhotoSize = message.photo[-1]  # Get the largest available photo

    # Download the photo
    file_info = await message.bot.get_file(photo.file_id)
    file_path = file_info.file_path
    photo_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    response = requests.get(photo_url)
    file_name = f'{message.from_user.id}_{message.message_id}.jpg'

    # Save the photo to a local folder
    local_file_path = f'photos/{file_name}'
    with open(local_file_path, 'wb') as f:
        f.write(response.content)

    # Upload the photo to Google Drive
    file_metadata = {
        'name': file_name,
        'parents': [getenv("GOOGLE_DRIVE_FOLDER_ID")]
    }
    media = MediaFileUpload(local_file_path, mimetype='image/jpeg')
    drive_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = drive_file.get('id')

    # Add a record to Google Sheets
    sheet_id = getenv("GOOGLE_SHEET_ID")
    values = [[message.from_user.id, file_id]]
    body = {'values': values}
    sheets_service.spreadsheets().values().append(spreadsheetId=sheet_id, range='Sheet1', valueInputOption='USER_ENTERED', body=body).execute()

    await message.answer("Photo uploaded successfully!")
    await state.clear()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
