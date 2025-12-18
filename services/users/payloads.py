from faker import Faker
# Убираем глобальный faker - он создаётся при импорте модуля
# faker = Faker()  # ❌ Потенциальная проблема при параллельном запуске

class Payload:
    def __init__(self):
        # Каждый экземпляр получает свой генератор
        # Если тесты запускаются в разных процессах - у каждого свой Faker
        # Если в одном процессе - всё равно безопасно
        self.faker = Faker()

    def create_user(self,
                    email: str = None,  # ✅ None вместо вычисленного значения
                    nickname: str = None,
                    password: str = None):  # ✅ Добавляем password параметр!
        """
        тело запроса POST для создания Юзера
        """
        # email: если не передан - генерируем
        if email is None:
            email = self.faker.email()  # ✅ Генерируется при каждом вызове!

        # nickname: если не передан - генерируем
        if nickname is None:
            nickname = self.faker.user_name()  # ✅ Генерируется при каждом вызове!

        # password: если не передан - генерируем
        if password is None:
            password = self.faker.password()  # ✅ Генерируется при каждом вызове!

        return {
            "email": email,
            "password": password,  # ✅ Теперь можно передать конкретный пароль!
            "name": self.faker.name(),  # ✅ Всегда генерируется новый
            "nickname": nickname
        }

    def login_users(self,
                    email: str = None,
                    password: str = None):
        """
        тело запроса POST для логина пользователя
        """
        if email is None:
            email = self.faker.email()
        if password is None:
            password = self.faker.password()

        return {
            "email": email,
            "password": password
        }




# from faker import Faker
# faker = Faker()
#
# class Payload:
#     """
#     класс тело (содержание) запроса по сервисам
#     генерация данных
#     """
#
#     def create_user(self,
#                     email: str = faker.email(),
#                     nickname: str = faker.user_name()):
#         """
#         тело запроса POST для создания Юзера
#         генерируемые поля
#         """
#         return {
#             "email": email,
#             "password": faker.password(),
#             "name": faker.name(),
#             "nickname": nickname
#         }
#
#     def login_users(self,
#                     email: str = faker.email(),
#                     password: str = faker.password()):
#         """
#         тело запроса POST для логина пользователя
#         """
#         return {
#             "email": email,
#             "password": password
#         }