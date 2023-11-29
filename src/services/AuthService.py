import bcrypt

from src.models import User
from src.repositories.UserRepo import UserRepository


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, username: str, password: str):
        """
        Register a new regular user.
        :param username: the username used to log in
        :param password: the plain text password
        :return: the newly created user
        """

        self.user_repo.create(
            username=username,
            password=self.__hash_password(password),
            avatar_url="https://placehold.co/500x500",
            is_admin=False,
        )

        return self.user_repo.find_by_username(username)

    def authenticate(self, username: str, password: str) -> User or None:
        """
        Authenticate a user by credentials.
        :param username: the username used to log in
        :param password: the plain text password
        :return: the user if the authentication was successful, None otherwise
        """

        user = self.user_repo.find_by_username(username)

        if user is None:
            return None

        if not self.__check_password(password, user.password):
            return None

        # TODO: save the user in session

        return user

    def change_password(self, user_id: int, old_password: str, new_password: str):
        """
        Change the password of a user.
        :param user_id: the id of the user
        :param old_password: the old password used to confirm the identity
        :param new_password: the new password to set
        :return: True if the password was changed, False otherwise
        """

        user = self.user_repo.find(user_id)

        if user is None:
            return False

        if not self.__check_password(old_password, user.password):
            return False

        self.user_repo.update(
            user_id,
            {'password': self.__hash_password(new_password)}
        )

        return True

    @staticmethod
    def __check_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())

    @staticmethod
    def __hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
