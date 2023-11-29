from typing import TypedDict


class AddressModel(TypedDict):
    id: int
    user_id: int
    contact_name: str
    contact_phone: str
    details: str
