import asyncio
import logging
import sys
from os import getenv

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.filters import Filter

from utils import messages_text, Form, Language
from filters import LangFilter
from db.manager import create_or_update_user, create_counter

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
lang_type = Language("eng")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


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
    await message.answer(replies["success"], reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
