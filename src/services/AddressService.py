from models import Address
from repositories.AddressRepo import AddressRepository


class AddressService:
    def __init__(self, connection, cursor):
        self.address_repo = AddressRepository(connection, cursor)

    def get_user_addresses(self, user_id: int) -> list:
        return self.address_repo.get_by_user_id(user_id)

    def add_address_to_user(self, user_id: int, contact_name: str, contact_phone: str, address_details: str):
        self.address_repo.create(user_id, contact_name, contact_phone, address_details)

    def update_address(self, address_id: int, contact_name: str, contact_phone: str, address_details: str):
        self.address_repo.update(address_id, contact_name, contact_phone, address_details)

    def delete_address(self, address_id: int):
        self.address_repo.delete(address_id)
