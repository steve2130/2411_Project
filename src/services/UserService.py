from src.models.User import UserModel


class UserService:
    def __init__(self):
        self.user_model = UserModel()

    def register(self, username, password):
        """
        Register a new regular user.
        :param username: the username used to log in
        :param password: the plain text password
        :return: the newly created user
        """

        # TODO: we probably want to hash the password
        self.user_model.create(
            username=username,
            password=password,
            avatar_url="https://placehold.co/500x500",
            is_admin=False,
        )

        return self.user_model.get_by_username(username)
