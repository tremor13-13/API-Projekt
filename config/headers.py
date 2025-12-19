import os
from dotenv import load_dotenv
load_dotenv()


class Headers:
    '''
    класс Headers с данными авторизации из файла .env
    '''

    basic = {
        "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
        "X-Task-id": "API-3"
    }


