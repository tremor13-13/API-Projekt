import json
import allure
import requests
from pydantic import BaseModel, ValidationError


class Helper:
    """
    Класс с методами валидации полей ответа Response
    """

    def attach_response(self, response_data, http_status_code=None):
        """
        В allure-репорт отправляем тело ответа
        :param response_data: JSON данные (словарь/список)
        :param http_status_code: HTTP статус код (200, 404, 500 и т.д.)
        """
        result = json.dumps(response_data, indent=4, ensure_ascii=False)

        # Формируем имя с реальным HTTP статусом
        status_display = f"Status: {http_status_code}" if http_status_code else "Status: N/A"

        allure.attach(
            body=result,
            name=status_display,
            attachment_type=allure.attachment_type.JSON
        )

    def validate_response(self,
                          response: requests.Response,
                          model=type[BaseModel],
                          status_code: int = 200,
                          expected_success: bool = True
                          ):
        """
        Метод валидации ответа Response
        """
        try:
            # Пытаемся получить JSON, если есть контент
            if response.content:
                response_data = response.json()
            else:
                response_data = {"message": "No content"}
        except json.JSONDecodeError:
            # Если не JSON (текст или бинарные данные)
            response_data = {"text": response.text[:500]}  # Ограничиваем длину

        # Прикрепляем в Allure с реальным статусом
        self.attach_response(response_data, http_status_code=response.status_code)

        if expected_success:
            assert response.status_code == status_code, f"Expected {status_code}, got {response.status_code}. Response: {response_data}"

            # Обработчик возвращаемых данных
            if response_data and not isinstance(response_data, str):
                try:
                    if isinstance(response_data, dict):
                        return model(**response_data)
                    elif isinstance(response_data, list):
                        return [model(**item) for item in response_data]
                except ValidationError as e:
                    raise AssertionError(f"Response validation failed: {e}\nResponse data: {response_data}")
            return response_data
        else:
            # Для ожидаемых ошибок (например, тестируем 400 ошибку)
            assert response.status_code != 200, f"Expected error but got success: {response_data}"
            return response_data




# import json
# import allure
# import requests
# from pydantic import BaseModel
#
#
# class Helper:
#     """
#     Класс с методами валидации полей ответа Response
#     """
#     def attach_response(self, response):
#         """
#         в алюр-репорт отправляем тело ответа
#         для отображения в JSON формате
#         :param response:
#         :return: JSON
#         """
#         result = json.dumps(response, indent=4)
#         allure.attach(
#             body=result,
#             name=f"Status: {response.get('status_code', 'N/A')}",
#             attachment_type=allure.attachment_type.JSON
#         )
#     def validate_response(self,
#         response: requests.Response,
#         model=type[BaseModel],
#         status_code: int = 200,
#         expected_success: bool = True
#     ):
#         """
#         Метод валидации ответа Response
#         """
#         self.attach_response(response.json())
#         if expected_success:
#             assert response.status_code == status_code, response.json()
#             # обработчик возвращаемых данных
#             if isinstance(response.json(), dict):
#                 return model(**response.json())
#             elif isinstance(response.json(), list):
#                 return [model(**item) for item in response.json()]
#         else:
#             assert response.status_code != 200, response.json()