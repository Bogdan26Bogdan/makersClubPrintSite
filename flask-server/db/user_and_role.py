from db.db import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from typing import List
from sqlalchemy.orm import relationship, Session
from db.db import create_engine_instance


association_table = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


class User(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    roles: Mapped[List["Role"]] = relationship(secondary=association_table)

    def has_role(self, role_name: str) -> bool:
        return any(role.role == role_name for role in self.roles)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    def __eq__(self, other):
        if isinstance(other, Role):
            return self.id == other.id
        return False

    @staticmethod
    def valid_role(role_name: str) -> bool:
        with Session(create_engine_instance()) as sql_session:
            role = sql_session.query(Role).filter_by(role=role_name).first()
            return role is not None
