from settings import load_config
from sqlalchemy import create_engine, MetaData, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = load_config()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
session._model_changes = {}
Base = declarative_base()


class TgAccounts(Base):
    __tablename__ = 'tg_accounts'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    telegram_user_id = Column(Integer, primary_key=True)

    created_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return {"id": self.id, "telegram_user_id": self.telegram_user_id}


class UserTgAccounts(Base):
    __tablename__ = 'user_tg_accounts'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, primary_key=True)
    tg_account_id = Column(Integer, primary_key=True)

    created_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return {"id": self.id, "user_id": self.user_id, "tg_account_id": self.tg_account_id}
