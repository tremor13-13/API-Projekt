import allure
import requests
from services.users.payloads import Payload
from config.headers import Headers
from services.users.endpoints import Endpoints
from utils.helper import Helper
from services.users.models.model_user import UserResponse


class UsersAPI(Helper):
    def __init__(self):
        self.payloads = Payload()
        self.headers = Headers()
        self.endpoints = Endpoints()
        self.created_user_data = None  # Новый атрибут для хранения данных

    @allure.step("create user")
    def create_user(self) -> UserResponse:
        """
        метод POST создание User
        """
        # создаем юзера (фейковые данные)
        payload = self.payloads.create_user()

        # 2. Сохраняем email и пароль для будущего логина
        self.created_user_data = {
            "email": payload["email"],
            "password": payload["password"]
        }

        # 3. Отправляем запрос с подготовленными данными ранее
        response = requests.post(
            url=self.endpoints.create_user,
            headers=self.headers.basic,
            json=payload
        )

        # 4. Валидируем и сохраняем все данные из response (ответа)
        validated_data = self.validate_response(response, UserResponse)
        if validated_data:
            # mode="json" автоматически преобразует UUID → строку
            self.created_user_data = validated_data.model_dump(mode="json")
            self.created_user_data["password"] = payload["password"]
            # UUID уже строка, не нужно делать str()
        return validated_data

    @allure.step("login user")
    def loggin_users(self, use_created_user: bool = True):
        """
        Логин пользователя
        :param use_created_user: если True - использует данные созданного пользователя
        """
        if use_created_user and self.created_user_data:
            # Используем сохраненные данные
            login_payload = {
                "email": self.created_user_data["email"],
                "password": self.created_user_data["password"]
            }
        else:
            # Генерируем новые случайные данные
            login_payload = self.payloads.login_users()

        response = requests.post(
            url=self.endpoints.loggin_user,
            headers=self.headers.basic,
            json=login_payload
        )
        return self.validate_response(response, UserResponse)

    def get_created_user_data(self):
        """Получить данные созданного пользователя"""
        return self.created_user_data
