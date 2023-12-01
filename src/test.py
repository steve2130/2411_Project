# import repositories.AddressRepo as AddressRepo
# import repositories.CategoriesRepo as CategoriesRepo
# import repositories.ProductSKUsRepo as ProductSKUsRepo
from repositories.ProductsRepo import ProductRepository
# import repositories.UserRepo as UserRepo
from db import DatabaseConnection


def main():
    DBConnection = DatabaseConnection()
    DBConnection.connect_to_DB()
    connection = DBConnection.connection
    cursor = DBConnection.cursor
    # cursor =  stuff[1]
    a = ProductRepository(connection, cursor)
    dict1 = {"ID": 501, "CATEGORY_ID": 0, "TITLE": "Sony Stuff", "DESCRIPTION": "Fun", "IMAGE_URL": "null", "PRICE": 49.99}
    a.AddRecord(501, 0, "Sony Stuff", "Fun", "null", 49.99)
    a.Commit()

    # DBConnection.close_all_connections() # may need async

if __name__ == "__main__":
    main()