import requests
from services.TaskService import TaskService
from utils.regex_helper import get_link_from_str


class WhisperTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client = "openai"):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client


  def perform_task(self):
    msg_with_link = self.task_data.get("msg")
    print(f"[PROCESSING DETAILS]: Message with link: {msg_with_link}")

    link = get_link_from_str(msg_with_link)[0]
    print(f"[PROCESSING DETAILS]: Extracted link: {link}")

    mp3_file = self.__get_mp3_file(link)

    get_translation_method = self.get_method_adjusted_to_client("whisper-1", "get_translation")
    self.answer = get_translation_method(mp3_file)
    print(f"[PROCESSING DETAILS]: translation of file: {self.answer}")

  def __get_mp3_file(self, link:str) -> bytes:
    return requests.get(link).content