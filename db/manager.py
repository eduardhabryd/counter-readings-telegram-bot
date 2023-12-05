from db.database import SessionLocal
from db.models import User

from sqlalchemy import select


async def get_user_by_telegram_id(telegram_user_id):
    async with SessionLocal() as session:
        stmt = select(User).where(User.telegram_user_id == telegram_user_id)
        result = await session.execute(stmt)
        user = result.scalar_one()
        return user


async def create_or_update_user(telegram_user_id, language, address, account):
    async with SessionLocal() as session:
        existing_user = await get_user_by_telegram_id(telegram_user_id)

        if existing_user is not None:
            print("Existing User:", existing_user)
            print("New Data:", language, address, account)
            existing_user.language = language
            existing_user.address = address
            existing_user.account = account

            updated_user = await session.merge(existing_user)
        else:
            print("Creating New User")
            new_user = User(
                telegram_user_id=telegram_user_id,
                language=language,
                address=address,
                account=account
            )
            session.add(new_user)

        await session.commit()
