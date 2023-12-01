import sys

# because I can only use Python 3.7 on UDS -Tommy
if sys.version_info >= (3, 8):
    from typing import TypedDict, Literal, overload  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict, Literal, overload


class CategoriesModel(TypedDict):
    ID:      int
    NAME:    str



# class CategoriesModel(object):

#     def __init__(self, ID: int, NAME: str):
#         self.__ID     = ID
#         self.__NAME   = NAME



#     # Getter & setter
#     @property
#     def ID(self) -> int:
#         return self.__ID
    
#     @ID.setter
#     def ID(self, value):
#         self.__ID = value
    


#     @property
#     def NAME(self) -> int:
#         return self.__NAME
    
#     @NAME.setter
#     def NAME(self, value):
#         self.__NAME = value
    


#     # Database method
#     @property
#     def to_db(self) -> dict:
#         return {"ID": self.__ID, "NAME": self.__NAME}