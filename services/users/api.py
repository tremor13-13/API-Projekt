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
        # создаем юзера (фейковые данные) и сохраняем их в payload
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
            # mode="json" автоматически преобразует UUID в строку
            # model_dump() вместо dict() в пайдентик дикт
            # при валидации данных считается устаревшим методом
            self.created_user_data = validated_data.model_dump(mode="json")
            self.created_user_data["password"] = payload["password"]
            # UUID уже строка, не нужно передавать в str()
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
            # если данных нет генерируем новые случайные данные
            login_payload = self.payloads.login_users()
        #  отправляем сформированный запрос на сервер
        response = requests.post(
            url=self.endpoints.loggin_user,
            headers=self.headers.basic,
            json=login_payload
        )
        return self.validate_response(response, UserResponse)

    @allure.step("get user by UUID")
    def get_user_by_uuid(self, user_uuid: str = None) -> UserResponse:  # 1. Опечатка в названии: ger → get
        """
        Получение данных пользователя по UUID
        :param user_uuid: UUID пользователя, если значение пустое то берем из сохраненного
        :return: UserResponse объект
        """
        # 1. Определяем какой UUID использовать
        if user_uuid is None:
            if not self.created_user_data or "uuid" not in self.created_user_data:
                raise ValueError("UUID не указан и нет сохраненного пользователя")
            user_uuid = self.created_user_data["uuid"]  # 2. Квадратные скобки, не круглые!

        # 2. Формируем URL с подставленным UUID
        url = self.endpoints.get_user.format(user_uuid=user_uuid)

        # 3. Отправляем GET запрос
        response = requests.get(
            url=url,
            headers=self.headers.basic  # 3. "headers", не "heders"
        )
        # 4. Валидируем ответ
        validated_data = self.validate_response(response, UserResponse)
        return validated_data

    def get_created_user_data(self):
        """
        Получить данные созданного пользователя
        """
        return self.created_user_data