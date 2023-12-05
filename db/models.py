from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True)
    language = Column(String)
    address = Column(String)
    account = Column(String)

    def __str__(self):
        return (
            f"User(id={self.id}, "
            f"telegram_user_id={self.telegram_user_id}, "
            f"language={self.language}, "
            f"address={self.address}, "
            f"account={self.account})"
        )
