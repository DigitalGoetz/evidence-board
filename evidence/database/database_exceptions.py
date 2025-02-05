class ObjectNotFoundException(Exception):

    def __init__(self, action: str, target: str, type: str):
        self.action = action
        self.target = target
        self.type = type

    def __str__(self):
        return f"ObjectNotFoundException: Could not find {self.type}({self.target}) during {self.action}"

    def return_dict(self):
        return {"type": "error", "category": "ObjectNotFoundException", "message": self.__str__()}


class ObjectAlreadyExistsException(Exception):

    def __init__(self, target: str, type: str):
        self.target = target
        self.type = type

    def __str__(self):
        return f"ObjectAlreadyExistsException: {self.type}({self.target}) already exists"

    def return_dict(self):
        return {"type": "error", "category": "ObjectAlreadyExistsException", "message": self.__str__()}


class ObjectInfoExistsException(Exception):

    def __init__(self, target: str, type: str, info: str):
        self.target = target
        self.type = type
        self.info = info

    def __str__(self):
        return f"ObjectInfoExistsException: {self.type}({self.target}) already contains a reference to {self.info}"

    def return_dict(self):
        return {"type": "error", "category": "ObjectInfoExistsException", "message": self.__str__()}


class ObjectInfoDoesNotExistException(Exception):

    def __init__(self, target: str, type: str, info: str):
        self.target = target
        self.type = type
        self.info = info

    def __str__(self):
        return f"ObjectInfoDoesNotExistException: {self.type}({self.target}) does not have a reference to {self.info}"

    def return_dict(self):
        return {"type": "error", "category": "ObjectInfoDoesNotExistException", "message": self.__str__()}
