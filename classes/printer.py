from data import Data


class Printer(Data):
    """Depicts the printer object"""

    def __init__(self, ID: str, status: str):
        super().__init__()  # defines self.data = printer
        self.printer_ID = ID
        self.status = status


# TODO get rid of this eventually for actual testing
if __name__ == "__main__":
    x = Printer("01", "Working")
    print(x.to_dictionary())
