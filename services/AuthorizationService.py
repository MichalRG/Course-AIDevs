import os
import requests

from typing import Optional
from constans.constans import BASE_URL


class AuthorizationService:
    def __init__(self):
        self.base_url = f"{BASE_URL}/token"

    def get_token(self, task_name: str) -> Optional[str]:
        url = f"{self.base_url}/{task_name}"
        data = {
            "apikey": os.getenv("APIKEY-AIDEVS")
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            return response.json().get("token")
        else:
            print(f"ERROR: there was a problem with fetching token. Message: {response.json().get('msg')}")
