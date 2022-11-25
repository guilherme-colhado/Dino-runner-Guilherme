from dino_runner.utils.constants import TIME, DEFAULT_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Time(PowerUp):
    def __init__(self):
        self.image = TIME
        self.type = DEFAULT_TYPE
        super().__init__(self.image, self.type)
        