from data import Data
import uuid
from datetime import datetime

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

def create_order(filament_colour: str, print_title: str, ID: str) -> Order:
    """A function for creating an order."""



    #Create all of the values
    order_number = uuid.uuid4().hex
    print_title = print_title
    filament_colour = filament_colour
    weight = None
    estimated_duration = None
    price = None 
    order_date = datetime.today().strftime('%Y-%m-%d')
    order_time = datetime.today().strftime('%H:%M:%S')
    order_status = None
    student_ID = ID


    order = Order(order_number, print_title, filament_colour, weight, estimated_duration, price, order_date, order_time, order_status, student_ID)
    
    return order 




