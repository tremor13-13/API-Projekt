from faker import Faker
faker = Faker()

class Payload:
    """
    класс тело (содержание) запроса по сервисам
    генерация данных
    """

    def create_user(self,
                    email: str = faker.email(),
                    nickname: str = faker.user_name()):
        """
        тело запроса POST для создания Юзера
        генерируемые поля
        """
        return {
            "email": email,
            "password": faker.password(),
            "name": faker.name(),
            "nickname": nickname
        }

    def login_users(self,
                    email: str = faker.email(),
                    password: str = faker.password()):
        """
        тело запроса POST для логина пользователя
        """
        return {
            "email": email,
            "password": password
        }