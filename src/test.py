# import repositories.AddressRepo as AddressRepo
# import repositories.CategoriesRepo as CategoriesRepo
# import repositories.ProductSKUsRepo as ProductSKUsRepo
from repositories.ProductsRepo import ProductRepository
# import repositories.UserRepo as UserRepo
import db


def main():
    connection, cursor = db.connect_to_DB()
    # cursor =  stuff[1]
    a = ProductRepository(connection, cursor)
    a.DeleteRecord("ID", 501)
    a.Commit()

if __name__ == "__main__":
    main()