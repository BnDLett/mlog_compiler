class Assignment:
    data: any
    representation: str
    name: str

    def __init__(self, data: any, name: str):
        self.data = data
        self.name = name
        self.representation = f"set {name} {data}"


class Control:
    representation: str
    block: str
    enabled: str

    def __init__(self, block: str, enabled: str):
        self.block = block
        self.enabled = enabled
        self.representation = f"control enabled {self.block} {self.enabled} 0 0 0"


class Sense:
    representation: str
    block: str
    sensor: str

    def __init__(self, block: str, sensor: str, target_var: str):
        self.block = block
        self.sensor = sensor
        self.target_var = target_var
        self.representation = f"sensor {self.target_var} {self.block} @{self.sensor}"
