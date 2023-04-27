from data import Data


class Order(Data):
    def __init__(
        self,
        order_number: int,
        print_title: str,
        filament_colour: str,
        weight: float,
        estimated_duration: int,
        price: float,
        order_date: str,
        order_time: str,
        order_status: str,
        student_ID: str,
    ):
        super().__init__()
        self.order_number = order_number
        self.print_title = print_title
        self.filament_colour = filament_colour
        self.weight = weight
        self.estimated_duration = estimated_duration
        self.price = price
        self.order_date = order_date
        self.order_time = order_time
        self.order_status = order_status
        self.student_ID = student_ID
