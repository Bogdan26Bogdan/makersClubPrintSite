from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base
from typing import Tuple


class PrintTracker(Base):
    __tablename__ = "print_tracker"

    id = Column(Integer, primary_key=True)
    Userid: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    PrintName = Column(String(255), nullable=False)
    GramsUsed = Column(
        Integer, nullable=False
    )  # in grams * 100 to avoid float issues
    Duration = Column(Integer, nullable=False)  # in minutes
    Printer = Column(String(100), nullable=False)
    Color = Column(String(50), nullable=False)
    Completed = Column(Boolean, default=False)
    Submitted = Column(DateTime, nullable=False)


def validate_GramsUsed(value: str) -> Tuple[bool, int]:
    """Validate that we have been provided a valid grams used value. 
    Returns whether the value is valid and the value in integer format."""
    try:
        value = value.strip("g")

        if "." in value: 
            parts = value.split(".")
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                return (False, 0)

            left_side = parts[0]
            right_side = parts[1]
            if len(right_side) > 2:
                return (False, 0)


            grams = int(left_side) * 100 + int(right_side.ljust(2, "0")[:2])
            return (True, grams)
        else: 
            grams = int(value)
            return (True, grams)

    except Exception:
        return (False, 0)
    


