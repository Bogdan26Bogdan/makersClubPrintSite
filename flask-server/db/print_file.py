from db.db import Base
from db.print_tracker import PrintTracker
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class PrintFile(Base):
    __tablename__ = 'print_files'

    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_data = Column(LargeBinary)
    print_tracker_id: Mapped[int] = mapped_column(Integer, ForeignKey(PrintTracker.__tablename__ + ".id"), nullable=False)

    