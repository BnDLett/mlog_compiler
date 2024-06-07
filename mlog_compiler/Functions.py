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
