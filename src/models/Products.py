class ProductModel(object):

    def __init__(self, ID: int, CATEGORY_ID: int, TITLE: str, DESCRIPTION: str, IMAGE_URL: str, PRICE: float):
        self.__ID            = ID
        self.__CATEGORY_ID   = CATEGORY_ID
        self.__TITLE         = TITLE
        self.__DESCRIPTION   = DESCRIPTION
        self.__IMAGE_URL     = IMAGE_URL
        self.__PRICE         = PRICE

    # Getter
    @property
    def ID(self) -> int:
        return self.__ID
    
    @property
    def CATEGORY_ID(self) -> int:
        return self.__CATEGORY_ID
    
    @property
    def TITLE(self) -> str:
        return self.__TITLE
        
    @property
    def DESCRIPTION(self) -> str:
        return self.__DESCRIPTION
    
    @property
    def IMAGE_URL(self) -> str:
        return self.__IMAGE_URL

    @property
    def PRICE(self) -> float:
        return self.__PRICE

    # Database method
    @property
    def to_db(self) -> dict:
        return {"ID": self.__ID, "CATEGORY_ID": self.__CATEGORY_ID, "TITLE": self.__TITLE, "DESCRIPTION": self.__DESCRIPTION, "IMAGE_URL": self.__IMAGE_URL, "PRICE": self.__PRICE}