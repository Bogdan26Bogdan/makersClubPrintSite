from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base
from db.print_tracker import PrintTracker

STATUS_IDLE = "Idle"
STATUS_PRINTING = "Printing"
STATUS_ERROR = "Error"
STATUS_OFFLINE = "Offline"
STATUS_MAINTENANCE = "Maintenance"

STATUSES = [
    STATUS_IDLE,
    STATUS_PRINTING,
    STATUS_ERROR,
    STATUS_OFFLINE,
    STATUS_MAINTENANCE,
]


class Printer(Base):
    __tablename__ = "printers"

    id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False, unique=True)
    Status = Column(String(50), nullable=False)
    PrintInProgress = Column(
        Integer, ForeignKey(PrintTracker.__tablename__ + ".id"), nullable=True
    )
