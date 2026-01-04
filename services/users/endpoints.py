from config.stages import get_stage


class Endpoints:
    """
    Класс вызова STAGE для эндпойнтов разных сервисов {СТЕЙДЖ}/адрес_сервиса

    """

    STAGE = get_stage()

    create_user = f"{STAGE}/users"
    loggin_user = f"{STAGE}/users/login"
    get_user = f"{STAGE}/users/{{user_uuid}}"
    delete_user = f"{STAGE}/users/{{user_uuid}}"