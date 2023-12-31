import sys

# because I can only use Python 3.7 on UDS -Tommy
if sys.version_info >= (3, 8):
    from typing import TypedDict, Literal, overload  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict, Literal, overload


class ProductModel(TypedDict):
    ID:             int
    CATEGORY_ID:    int
    TITLE:          str
    DESCRIPTION:    str
    IMAGE_URL:      str
    PRICE:          float





# class ProductModel(object):

#     def __init__(self, ID: int, CATEGORY_ID: int, TITLE: str, DESCRIPTION: str, IMAGE_URL: str, PRICE: float):
#         self.__ID            = ID
#         self.__CATEGORY_ID   = CATEGORY_ID
#         self.__TITLE         = TITLE
#         self.__DESCRIPTION   = DESCRIPTION
#         self.__IMAGE_URL     = IMAGE_URL
#         self.__PRICE         = PRICE


#     # Getter & setter
#     @property
#     def ID(self) -> int:
#         return self.__ID
    
#     @ID.setter
#     def ID(self, value):
#         self.__ID = value
    


#     @property
#     def CATEGORY_ID(self) -> int:
#         return self.__CATEGORY_ID
    
#     @CATEGORY_ID.setter
#     def CATEGORY_ID(self, value):
#         self.__CATEGORY_ID = value
    


#     @property
#     def TITLE(self) -> str:
#         return self.__TITLE
        
#     @TITLE.setter
#     def TITLE(self, value):
#         self.__TITLE = value



#     @property
#     def DESCRIPTION(self) -> str:
#         return self.__DESCRIPTION
    
#     @DESCRIPTION.setter
#     def DESCRIPTION(self, value):
#         self.__DESCRIPTION = value



#     @property
#     def IMAGE_URL(self) -> str:
#         return self.__IMAGE_URL
    
#     @IMAGE_URL.setter
#     def IMAGE_URL(self, value):
#         self.__IMAGE_URL = value



#     @property
#     def PRICE(self) -> float:
#         return self.__PRICE
    
#     @PRICE.setter
#     def PRICE(self, value):
#         self.__PRICE = value



#     # Database method
#     @property
#     def to_db(self) -> dict:
#         return {"ID": self.ID, "CATEGORY_ID": self.CATEGORY_ID, "TITLE": self.TITLE, "DESCRIPTION": self.DESCRIPTION, "IMAGE_URL": self.IMAGE_URL, "PRICE": self.PRICE}