from data import Data


class Student_Account(Data):
    def __init__(
        self,
        student_ID: str,
        first_name: str,
        last_name: str,
        email: str,
        free_filament_left: float = 150.0,
        paid_filament_left: float = 0.0,
        admin: bool = False
    ):
        super().__init__()
        self.student_ID = student_ID
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.free_filament_left = free_filament_left
        self.paid_filament_left = paid_filament_left
        self.admin = admin
