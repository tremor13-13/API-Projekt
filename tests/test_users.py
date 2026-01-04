
from config.base_test import BaseTest

class TestUsers(BaseTest):

    def test_create_user(self):
        create_user = self.user_api.create_user()
        login_users = self.user_api.loggin_users()
        get_user_by_uuid = self.user_api.get_user_by_uuid()
        delete_user_by_uuid = self.user_api.delete_user_by_uuid()
        # print(user.email)
