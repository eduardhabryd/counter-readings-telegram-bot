from aiogram.filters import Filter
from aiogram.types import Message


class LangFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text in ("🇬🇧 English", "🇺🇦 Ukrainian")
