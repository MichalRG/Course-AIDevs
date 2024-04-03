import requests

from constans.constans import BASE_URL
from typing import Optional
from integrations.langchain.LangChainService import LangChainProvider
from integrations.openai.OpenAIService import OpenAIService
from utils.backoff_jitter import perfrom_backof_jitter_request


class TaskService:
    def __init__(self, aidevs_token: str, openai_token: Optional[str] = None):
        self.aidevs_token = aidevs_token
        self.openai_token = openai_token
        self.base_task_url = f"{BASE_URL}/task"
        self.base_answer_url = f"{BASE_URL}/answer"
        self.task_data = None
        self.answer = None
        self.base_client = None

    def get_task(self):
        response = perfrom_backof_jitter_request(f"{self.base_task_url}/{self.aidevs_token}", 6)

        if response and response.status_code == 200:
            print(f"[TASK DETAILS]: Task json response: {response.json()}")
            self.task_data = response.json()
        else:
            print(f"ERROR: Problem with fetching task. Message: {response}")

    def send_answer(self):
        url = f"{self.base_answer_url}/{self.aidevs_token}"

        data = {
            "answer": self.answer
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"[RESULT OF TASK]: Response msg: {response.json()}")
        else:
            print(f"ERROR: Error with processing answer request: {self.answer}. Message: {response.json().get('msg')}")

    def setup_openai_client(self, model: str):
      if not self.openai_token:
          raise Exception("Lack of openai token to process requests")
      
      self.openai_service = OpenAIService(self.openai_token, model)

    def setup_openai_langchain_client(self, model: Optional[str]):
        if not self.openai_token:
          raise Exception("Lack of openai token to process requests")

        self.langchain_service = LangChainProvider(self.openai_token, model)

    def get_method_adjusted_to_client(self, model_name: str, method_name: str):
        if self.base_client == "openai":
            self.setup_openai_client(model_name)
        
            return getattr(self.openai_service, method_name)
        else:
            self.setup_openai_langchain_client(model_name)

            return getattr(self.langchain_service, method_name)