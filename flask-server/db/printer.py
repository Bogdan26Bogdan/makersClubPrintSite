from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base, create_engine_instance
from db.print_tracker import PrintTracker
from sqlalchemy.orm import Session

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

    def finish_print(self):
        assert self.Status == STATUS_PRINTING, "Printer was not printing when told that it finished a print."
        

        with Session(create_engine_instance()) as sql_session:
            self.Status = STATUS_IDLE
            
            print = sql_session.query(PrintTracker).filter_by(id=self.PrintInProgress).first()
            if print: 
                print.Completed = True
                sql_session.add(print)
            self.PrintInProgress = None
            sql_session.add(self)
            sql_session.commit()



