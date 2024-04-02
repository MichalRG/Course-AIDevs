import requests
from services.TaskService import TaskService
from utils.backoff_jitter import perfrom_backof_jitter_request


class ScraperTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client: str = "langchain"):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client

  def perform_task(self):
    get_answer = self.get_method_adjusted_to_client("gpt-3.5-turbo", "perform_request")
    input_txt_link = self.task_data.get("input")
    question_to_answer = self.task_data.get("question")
  
    print(f"[PROCESSING DETAILS]: Getting data from {input_txt_link}")
    data = perfrom_backof_jitter_request(input_txt_link, 6)

    if not data:
      print("[PROCESSING DETAILS]: Fetching data has failed :(")
      raise Exception(f"Lack of data from {input_txt_link}")
    
    self.answer = get_answer(f"Answer question briefly and precisely just in few words, use your knowledge and context. The answer generate in polish language! Context### {data}", question_to_answer)


  
        
