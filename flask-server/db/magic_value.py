from db.db import Base, create_engine_instance
from sqlalchemy import Column, Integer, String
from datetime import datetime
import secrets
from sqlalchemy.orm import Session


class MagicValue(Base):
    __tablename__ = "magic_values"
    VALID_TIME = 10 * 60  # 10 minutes in seconds

    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False, unique=True)
    date_created = Column(
        String(100), nullable=False, default=datetime.now().isoformat()
    )
    valid = Column(Integer, nullable=False, default=1)

    @staticmethod
    def generate_magic_value():
        with Session(create_engine_instance()) as sql_session:
            magic_value = secrets.token_urlsafe(16)
            sql_session.add(MagicValue(value=magic_value))
            sql_session.commit()
            return magic_value

    @staticmethod
    def is_magic_value_valid(magic_value: str) -> bool:
        """Checks if the provided magic value is valid.

        #TODO: Not thread safe
        """
        with Session(create_engine_instance()) as sql_session:
            mv = (
                sql_session.query(MagicValue)
                .filter_by(value=magic_value, valid=1)
                .first()
            )
            if mv:
                mv.valid = 0  # either it gets used or it is expired
                time_diff = (
                    datetime.now() - datetime.fromisoformat(mv.date_created)
                ).total_seconds()
                if time_diff <= MagicValue.VALID_TIME:
                    sql_session.commit()
                    return True
            sql_session.commit()
            return False
