from db.database import SessionLocal, engine
from db.models import Base, User, Counter

Base.metadata.create_all(bind=engine)


def create_user(telegram_user_id, language, address, account):
    new_user = User(
        telegram_user_id=telegram_user_id,
        language=language,
        address=address,
        account=account
    )
    with SessionLocal() as session:
        session.add(new_user)
        session.commit()


def create_counter(telegram_user_id, counter_image_url):
    new_counter = Counter(
        telegram_user_id=telegram_user_id,
        counter_image_url=counter_image_url
    )
    with SessionLocal() as session:
        session.add(new_counter)
        session.commit()
