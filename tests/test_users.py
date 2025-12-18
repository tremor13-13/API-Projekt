
from config.base_test import BaseTest

class TestUsers(BaseTest):

    def test_create_user(self):
        create_user = self.user_api.create_user()
        login_users = self.user_api.loggin_users()
        # print(user.email)
