from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    lang = State()
    address = State()
    account = State()
    counter_image = State()


class Language:
    def __init__(self, lang):
        self.lang = lang

    def get_lang(self):
        return self.lang

    def set_lang(self, lang):
        self.lang = lang


messages_text = {
    "eng": {
        "address": "Please provide your address:",
        "account": "Please provide your personal account number:",
        "greetings": "Nice to meet you!",
        "success": "Thank you for your response!",
    },
    "ukr": {
        "address": "Введіть вашу адресу:",
        "account": "Введіть ваш номер особового рахунку:",
        "greetings": "Доброго дня!",
        "success": "Дякуємо за відповідь!",
    }
}
