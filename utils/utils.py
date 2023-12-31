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
        "image": "Please, send me an image of the counter :)",
        "success": "Photo was uploaded successfully!",
    },
    "ukr": {
        "address": "Введіть вашу адресу:",
        "account": "Введіть ваш номер особового рахунку:",
        "greetings": "Доброго дня!",
        "image": "Будь ласка, надішліть мені зображення лічильника :)",
        "success": "Зображення було успішно завантажено!",
    }
}
