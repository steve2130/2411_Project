from src.repositories.Address import AddressRepository


class AddressService:
    def __init__(self):
        self.address_repo = AddressRepository()

    def get_user_addresses(self, user_id: int):
        return self.address_repo.get_by_user_id(user_id)

    def add_address_to_user(self, user_id: int, address_details: str):
        self.address_repo.create(user_id, address_details)

    def update_address(self, address_id: int, address_details: str):
        self.address_repo.update(address_id, address_details)

    def delete_address(self, address_id: int):
        self.address_repo.delete(address_id)
