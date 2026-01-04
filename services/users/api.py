
import json
from datetime import datetime

import allure
import requests
from services.users.payloads import Payload
from config.headers import Headers
from services.users.endpoints import Endpoints
from utils.helper import Helper
from services.users.models.model_user import UserResponse


class UsersAPI(Helper):
    """Инициализация методов для дальнейшего использования """
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
    def get_user_by_uuid(self, user_uuid: str = None) -> UserResponse:
        """
        Получение данных пользователя по "UUID"
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
            headers=self.headers.basic
        )
        # 4. Валидируем ответ
        validated_data = self.validate_response(response, UserResponse)
        return validated_data

    @allure.step("delete user by UUID")
    def delete_user_by_uuid(self, user_uuid: str = None) -> dict:
        """
        Удаление данных пользователя по UUID
        Вазвращает dict с информацией об удалении, НЕ UserResponse!
        """
        if user_uuid is None:
            if not self.created_user_data or "uuid" not in self.created_user_data:
                raise ValueError("UUID не указан и нет сохраненного пользователя")
            user_uuid = self.created_user_data["uuid"]

        print(f"\n=== DEBUG DELETE ===")
        print(f"Deleting user with UUID: {user_uuid}")

        url = self.endpoints.delete_user.format(user_uuid=user_uuid)
        print(f"DELETE URL: {url}")

        response = requests.delete(url=url, headers=self.headers.basic)

        print(f"Response status: {response.status_code}")
        print(f"=== END DEBUG ===\n")

        # Для DELETE с 204 - создаем свой response для Allure
        result_data = {
            "status_code": response.status_code,
            "message": "User deleted successfully",
            "user_uuid": user_uuid,
            "deleted_at": datetime.now().isoformat()
        }

        # Прикрепляем в Allure
        allure.attach(
            body=json.dumps(result_data, indent=4),
            name=f"Status: {response.status_code}",
            attachment_type=allure.attachment_type.JSON
        )

        # Дополнительно прикрепляем параметр user_uuid
        allure.attach(str(user_uuid), name="user_uuid", attachment_type=allure.attachment_type.TEXT)

        # Проверяем что DELETE успешен
        assert response.status_code in [200, 204], \
            f"Delete failed with status {response.status_code}: {response.text}"

        # Возвращаем словарь, НЕ UserResponse!
        return result_data
    # @allure.step("delete user by UUID")
    # def delete_user_by_uuid(self, user_uuid: str = None):
    #     """
    #     Удаление данных пользователя по UUID
    #     """
    #     if user_uuid is None:
    #         if not self.created_user_data or "uuid" not in self.created_user_data:
    #             raise ValueError("UUID не указан и нет сохраненного пользователя")
    #         user_uuid = self.created_user_data["uuid"]
    #
    #     # URL должен быть для DELETE, а не для GET!
    #     url = self.endpoints.delete_user.format(user_uuid=user_uuid)  # ← Другой endpoint!
    #
    #     # Должен быть DELETE запрос!
    #     response = requests.delete(  # ← DELETE, а не GET!
    #         url=url,
    #         headers=self.headers.basic
    #     )
    #
    #     # При удалении обычно приходит 204 No Content или 200 OK
    #     # Проверяем успешный статус
    #     if response.status_code in [200, 204]:
    #         # Для 204 No Content - пустой ответ
    #         if response.status_code == 204:
    #             return {"status": "success", "message": "User deleted (204 No Content)"}
    #         else:
    #             # Если есть контент - валидируем
    #             return self.validate_response(response, UserResponse, status_code=response.status_code)
    #     else:
    #         # Если ошибка - валидируем с ожидаемым статусом ошибки
    #         return self.validate_response(response, UserResponse, status_code=response.status_code,
    #                                       expected_success=False)

    def get_created_user_data(self):
        """
        Получить данные созданного пользователя
        """
        return self.created_user_data