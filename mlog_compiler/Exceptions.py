class MissingEOL(Exception):
    pass


class UnknownOperation(Exception):
    pass


class CallDoesNotExist(TypeError):
    pass


class InvalidPath(ImportError):
    pass
