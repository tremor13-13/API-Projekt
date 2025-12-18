
from services.users.api import UsersAPI

class BaseTest:

    def setup_method(self):
        self.user_api = UsersAPI()