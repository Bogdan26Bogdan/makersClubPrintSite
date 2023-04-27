from data import Data
from typing import IO
from bson.binary import Binary


class File(Data):
    """Depicts a file object"""

    def __init__(self, student_id: str, order_number: str, file: IO):
        super().__init__()
        self.student_id = student_id
        self.order_number = order_number
        self.file = file

    def to_dictionary(self):
        # get all but the file
        the_dictionary = {
            k: v
            for k, v in self.__dict__.items()
            if not (k.startswith("__") and k.endswith("__") or k == "file")
        }

        file_bin = Binary(self.file.read())
        the_dictionary["file"] = file_bin

        return the_dictionary
