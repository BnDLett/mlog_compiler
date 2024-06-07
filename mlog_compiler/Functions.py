class Assignment:
    data: any
    representation: str
    name: str

    def __init__(self, data: any, name: str):
        self.data = data
        self.name = name
        self.representation = f"set {name} {data}"


class Output:
    data: any
    representation: str
    sink: str

    def __init__(self, data, sink):
        self.data = data
        self.representation = f"print"
