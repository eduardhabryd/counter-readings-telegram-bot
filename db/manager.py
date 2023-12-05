from sqlalchemy.ext.asyncio import AsyncSession
from db.database import SessionLocal
from db.models import User, Counter

from sqlalchemy import select


async def get_user_by_telegram_id(telegram_user_id):
    async with SessionLocal() as session:
        stmt = select(User).where(User.telegram_user_id == telegram_user_id)
        result = await session.execute(stmt)

        user = result.scalar()
        return user


async def create_or_update_user(telegram_user_id, language, address, account):
    async with SessionLocal() as session:
        existing_user = await get_user_by_telegram_id(telegram_user_id)

        if existing_user is not None:
            existing_user.language = language
            existing_user.address = address
            existing_user.account = account
        else:
            new_user = User(
                telegram_user_id=telegram_user_id,
                language=language,
                address=address,
                account=account
            )
            session.add(new_user)

        await session.commit()


async def create_counter(telegram_user_id, counter_image_url):
    async with SessionLocal() as session:
        new_counter = Counter(
            telegram_user_id=telegram_user_id,
            counter_image_url=counter_image_url
        )
        session.add(new_counter)
        await session.commit()
