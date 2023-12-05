# 🤖 Telegram Bot for Counter Data Collection

## 🌐 Overview
Bilingual Telegram bot based on Python with `Aiogram` for efficient data
collection.
The bot integrates an inline keyboard to streamline the process of gathering
user personal data, such as addresses and account information, and
receiving photos of meter readings.


## 🎯 Features:


1. Personal Data Collection:

   - Request user address and account details through interactive messages.
   - Store collected data in a secure local database.

2. Meter Reading Photo Submission:

   - Enable users to submit photos of meter readings.
   - Store submitted photos securely on Google Drive.

3. Data Recording in Google Sheets:
   - Record essential information about meter submissions. 
   - Store links to submitted photos in Google Sheets for comprehensive record-keeping.

## 🚀 How to Run the Project

🗝️ Environment Variables and Tokens

1. Create .env File:

   - Duplicate .env.sample as .env.
   - Open the .env file in a text editor.

2. Fill in the Required Values:

   - `BOT_TOKEN`: Obtain your Telegram Bot Token from the BotFather.
   - `GOOGLE_SHEET_ID`: Obtain the Google Sheet ID for recording data.
   - `GOOGLE_DRIVE_FOLDER_ID`: Obtain the Google Drive Folder ID for storing 
     photos.

3. Save the Changes:

   - Save the .env file with the provided values.

4. Obtain Google API Credentials:

   - Obtain credentials in JSON format from your Google API project.
   - Save the credentials in the root folder as `creds.json`.

### 💻 Instructions for Windows

1. Clone the repository
    ```bash
    git clone https://github.com/eduardhabryd/counter-readings-telegram-bot.git
    ```
2. Create and Activate Virtual Environment:
    ```bash
    python3 -m venv venv
    source .\venv\Scripts\activate
    ```
3. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Project:
    ```bash
    python main.py
    ```
   
## 🍎 Instructions for Mac/Linux

1. Clone the repository
    ```bash
    git clone https://github.com/eduardhabryd/counter-readings-telegram-bot.git
    ```
2. Create and Activate Virtual Environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Project:
    ```bash
    python3 main.py
    ```
   