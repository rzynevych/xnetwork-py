import json

class ResponseObject:
    def __init__(self, status: bool, data: str, error:str = None) -> None:
        self.status = status
        self.data = data
        self.error = error

    def dict(self):
        return self.__dict__ 

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, 
    #         sort_keys=True, indent=4)