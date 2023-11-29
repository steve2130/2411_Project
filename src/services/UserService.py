from src.repositories.User import UserRepository


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def get_user_by_id(self, user_id: int):
        return self.user_repo.find(user_id)

    def get_user_by_username(self, username: str):
        return self.user_repo.find_by_username(username)

    def change_avatar(self, user_id: int, avatar_url: str):
        self.user_repo.update(user_id, {'avatar_url': avatar_url})
