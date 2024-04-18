import json
from typing import List
import requests
from services.TaskService import TaskService


class OptimaldbTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client = 'openai'):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client

  def perform_task(self):
    
    database_url = self.task_data.get("database")
    data = self.__get_database_data(database_url)

    zygfryd_information = data.get("zygfryd")
    stefan_information = data.get("stefan")
    ania_information = data.get("ania")

    zygfryd_string, stefan_string, ania_string = self.__concat_information({"zygfryd": zygfryd_information, "stefan": stefan_information, "ania": ania_information})

    llm_request_method = self.get_method_adjusted_to_client("gpt-4-turbo", "send_message_to_text_model")

    system_prompt = """
    You will receive from user information, your task is to summerize it, you have to keep all information! You don't allow to ommit anything! Kepp it in super minimal context! You don't have to follow grammatic rule, keep polish language.
    """

    zygryd_sumup = llm_request_method(system_prompt, zygfryd_string)
    stefan_sumup = llm_request_method(system_prompt, stefan_string)
    ania_sumup = llm_request_method(system_prompt, ania_string)

    sumup_string = f"{zygryd_sumup}###{stefan_sumup}###{ania_sumup}"
    
    print(f"[PROCESSING DETAILS]: sumup string {sumup_string}")

    self.answer = sumup_string
    
  def __concat_information(self, users_data: dict[str, List[str]]):
    keys = list(users_data.keys())

    zygfryd = f"Jestem {keys[0]}, {' '.join(users_data[keys[0]])}"
    stefan = f"Jestem {keys[1]}, {' '.join(users_data[keys[1]])}"
    ania = f"Jestem {keys[2]}, {' '.join(users_data[keys[2]])}"

    return (zygfryd, stefan, ania)


  def __get_database_data(self, url) -> dict:
    return json.loads(requests.get(url).content)
    