# import repositories.AddressRepo as AddressRepo
# import repositories.CategoriesRepo as CategoriesRepo
# import repositories.ProductSKUsRepo as ProductSKUsRepo
from repositories.ProductsRepo import ProductRepository
# import repositories.UserRepo as UserRepo
from db import DatabaseConnection


def main():
    DBConnection = DatabaseConnection()
    connection, cursor = DBConnection.connect_to_DB()
    # cursor =  stuff[1]
    a = ProductRepository(connection, cursor)
    dict1 = {"ID": 501, "CATEGORY_ID": 0, "TITLE": "Sony Stuff", "DESCRIPTION": "Fun", "IMAGE_URL": "null", "PRICE": 49.99}
    a.AddRecord(dict1)
    a.Commit()

if __name__ == "__main__":
    main()