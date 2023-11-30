class ProductSKUsModel(object):

    def __init__(self, ID: int, PRODUCT_ID: int, TITLE: str, DESCRIPTION: str, PRICE: float, STOCK: int):
        self.__ID           = ID
        self.__PRODUCT_ID   = PRODUCT_ID
        self.__TITLE        = TITLE
        self.__DESCRIPTION  = DESCRIPTION
        self.__PRICE        = PRICE
        self.__STOCK        = STOCK



    # Getter & setter
    #ID
    @property
    def ID(self) -> int:
        return self.__ID
    
    @ID.setter
    def ID(self, value):
        self.__ID = value
    


    #PRODUCT_ID
    @property
    def PRODUCT_ID(self) -> int:
        return self.__PRODUCT_ID
    
    @PRODUCT_ID.setter
    def PRODUCT_ID(self, value):
        self.__PRODUCT_ID = value
    


    #TITLE
    @property
    def TITLE(self) -> int:
        return self.__TITLE
    
    @PRODUCT_ID.setter
    def TITLE(self, value):
        self.__TITLE = value



    #DESCRIPTION
    @property
    def DESCRIPTION(self) -> int:
        return self.__DESCRIPTION
    
    @PRODUCT_ID.setter
    def DESCRIPTION(self, value):
        self.__DESCRIPTION = value



    #PRICE
    @property
    def PRICE(self) -> int:
        return self.__PRICE
    
    @PRICE.setter
    def PRICE(self, value):
        self.__PRICE = value



    #STOCK
    @property
    def STOCK(self) -> int:
        return self.__STOCK
    
    @STOCK.setter
    def STOCK(self, value):
        self.__STOCK = value



    # Database method
    @property
    def to_db(self) -> dict:
        return {"ID": self.__ID, "PRODUCT_ID": self.__PRODUCT_ID, "TITLE": self.__TITLE, "DESCRIPTION": self.__DESCRIPTION, "PRICE": self.__PRICE, "STOCK": self.__STOCK}