from data import Data
import uuid
from datetime import datetime


class Print_Job(Data):
    def __init__(
        self,
        order_number: int,
        job_number: int,
        job_status: str,
        filament_used: float,
        job_start_date: int,
        job_end_date: int,
        printer_ID: str,
    ):
        super().__init__()
        self.order_number = order_number
        self.job_number = job_number
        self.job_status = job_status
        self.filament_used = filament_used
        self.job_start_date = job_start_date
        self.job_end_date = job_end_date
        self.printer_ID = printer_ID


def create_job(order_number: int, filament_used: float, printer_ID: str) -> Print_Job:
    """A function for creating a print job."""
    # Create all of the values
    job_number = uuid.uuid4().hex
    job_status = "Printing"
    job_start_date = datetime.today().strftime("%Y-%m-%d-%H:%M:%S")
    job_end_date = None
    order_number = order_number
    filament_used = filament_used
    printer_ID = printer_ID

    job = Print_Job(
        order_number,
        job_number,
        job_status,
        filament_used,
        job_start_date,
        job_end_date,
        printer_ID,
    )

    return job
