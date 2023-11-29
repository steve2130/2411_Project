from typing import TypedDict


class UserModel(TypedDict):
    id: int
    username: str
    avatar_url: str
    is_admin: bool
