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


class Draw:
    representation: str
    operation: str
    a: str
    b: str
    c: str
    d: str
    e: str
    f: str

    def __init__(self, operation: str, a='0', b='0', c='0', d='0', e='0', f='0'):
        self.operation = operation
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

        self.representation = f"draw {operation} {a} {b} {c} {d} {e} {f}"


class DrawFlush:
    representation: str
    display_id: str

    def __init__(self, display_id: str):
        self.display_id = display_id
        self.representation = f"drawflush display{display_id}"


class UnitRadar:
    representation: str
    target_1: str
    target_2: str
    target_3: str
    sort: str
    order: str
    target_var: str

    def __init__(self, target_var: str, target_1: str, target_2: str, target_3: str, sort: str, order: str):
        self.target_var = target_var
        self.target_1 = target_1
        self.target_2 = target_2
        self.target_3 = target_3
        self.sort = sort
        self.order = order

        self.representation = f"uradar {target_1} {target_2} {target_3} {sort} 0 {order} {target_var}"
