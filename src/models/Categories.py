class CategoriesModel(object):

    def __init__(self, ID: int, NAME: str):
        self.__ID     = ID
        self.__NAME   = NAME



    # Getter & setter
    @property
    def ID(self) -> int:
        return self.__ID
    
    @ID.setter
    def ID(self, value):
        self.__ID = value
    


    @property
    def NAME(self) -> int:
        return self.__NAME
    
    @NAME.setter
    def NAME(self, value):
        self.__NAME = value
    


    # Database method
    @property
    def to_db(self) -> dict:
        return {"ID": self.__ID, "NAME": self.__NAME}