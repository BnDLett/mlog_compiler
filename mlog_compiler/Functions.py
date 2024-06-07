class Assignment:
    data: any
    representation: str
    name: str

    def __init__(self, data: any, name: str):
        self.data = data
        self.name = name
        self.representation = f"set {name} {data}"
