from data import Data


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
