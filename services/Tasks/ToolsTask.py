import json
from services.TaskService import TaskService


class ToolsTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client = 'langchain'):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client
  def perform_task(self):
    process_llm_method = self.get_method_adjusted_to_client('gpt-3.5-turbo', 'perform_request')

    system_message  = """
      Based on user prompt assign proper category. There are two categories: "ToDo" and "Calendar".
      If u recognised ToDo task and it won't have defined date then return json: {"tool": "ToDo", "desc": "description of task"}. As desc property return one sentence description for task.
      If u recognised Calendar task, so it will have defined date then return json: {"tool": "Calendar", "desc": "description of task", "date": "2024-04-10"}. Date alwyas return in format YYYY-MM-DD.
      Always return only proper json without any additional text or information.

      Today is 2024-04-09

      Example###
      User: "Wyjśc z psem na spacer"
      Response: "{"tool":"ToDo", "desc": "Spacer z psem"}"
      User: "Spotkać się ze znajomym pojutrze"
      Response: "{"tool":"Calendar", "desc": "Spotkanie z znajomym", "date": "2024-04-11"}"
    """
    user_prompt = self.task_data.get("question","")

    response = json.loads(process_llm_method(system_message, user_prompt))

    print(f"[PROCESSING DETAILS]: Response of model: {response}")

    self.answer = response

