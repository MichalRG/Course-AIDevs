import requests


class TaskService:
    def __init__(self, token: str):
        self.token = token
        self.base_task_url = "https://tasks.aidevs.pl/task"
        self.base_answer_url = "https://tasks.aidevs.pl/answer"
        self.task_data = None
        self.answer = None

    def get_task(self):
        response = requests.get(f"{self.base_task_url}/{self.token}")

        if response.status_code == 200:
            print(f"Task json response: {response.json()}")
            self.task_data = response.json()
        else:
            print(f"ERROR: Problem with fetching task. Message: {response.json().get('msg')}")

    def send_answer(self):
        url = f"{self.base_answer_url}/{self.token}"

        data = {
            "answer": self.answer
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"Response msg: {response.json()}")
        else:
            print(f"ERROR: Error with processing answer request. Message: {response.json().get('msg')}")