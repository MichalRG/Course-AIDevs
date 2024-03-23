import requests

from constans.constans import BASE_URL
from typing import Optional
from integrations.openai.OpenAIService import OpenAIService


class TaskService:
    def __init__(self, aidevs_token: str, openai_token: Optional[str] = None):
        self.aidevs_token = aidevs_token
        self.openai_token = openai_token
        self.base_task_url = f"{BASE_URL}/task"
        self.base_answer_url = f"{BASE_URL}/answer"
        self.task_data = None
        self.answer = None

    def get_task(self):
        response = requests.get(f"{self.base_task_url}/{self.aidevs_token}")

        if response.status_code == 200:
            print(f"[TASK DETAILS]: Task json response: {response.json()}")
            self.task_data = response.json()
        else:
            print(f"ERROR: Problem with fetching task. Message: {response.json().get('msg')}")

    def send_answer(self):
        url = f"{self.base_answer_url}/{self.aidevs_token}"

        data = {
            "answer": self.answer
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"[RESULT OF TASK]: Response msg: {response.json()}")
        else:
            print(f"ERROR: Error with processing answer request. Message: {response.json().get('msg')}")

    def setup_openai_client(self, model: str):
      if not self.openai_token:
          raise Exception("Lack of openai token to process requests")
      
      self.openai_service = OpenAIService(self.openai_token, model)