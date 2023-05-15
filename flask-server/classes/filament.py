from data import Data


class Filament(Data):
    def __init__(
        self,
        ID: str,
        cost_per_gram: float,
        weight_left: float,
        colour: str,
        manufacturer: str,
        material: str,
    ):
        super().__init__()
        self.ID = ID
        self.cost_per_gram = cost_per_gram
        self.weight_left = weight_left
        self.colour = colour
        self.manufacturer = manufacturer
        self.material = material
