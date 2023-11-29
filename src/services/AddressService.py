from src.models.Address import AddressModel


class AddressService:
    def __init__(self):
        self.address_model = AddressModel()

    def get_user_addresses(self, user_id: int):
        return self.address_model.get_by_user_id(user_id)

    def add_address_for_user(self, user_id: int, address_details: str):
        self.address_model.create(user_id, address_details)

    def delete_address(self, address_id: int):
        self.address_model.delete(address_id)
