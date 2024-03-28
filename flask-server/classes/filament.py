from data import Data


class Filament(Data):
    def __init__(
        self,
        colour: str,
        cost_per_gram: float = 0.03,
        material: str = "PLA",
        ID: int = None,
        weight_left: float = None,
        manufacturer: str = None,
    ):
        super().__init__()
        self.ID = ID
        self.cost_per_gram = cost_per_gram
        self.weight_left = weight_left
        self.colour = colour
        self.manufacturer = manufacturer
        self.material = material
