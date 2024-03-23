import requests
from services.TaskService import TaskService


class LiarTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None):
    super().__init__(aidevs_token, openai_token)


  def perform_task(self):
    question = "What is the main god of ancient Orient?"
    question_answer = self.__get_answer_on_question_from_aidevs(question)

    print(f"[PROCESSING DETAILS]: answer on question \"{question}\" is: {question_answer}")

    system_message = f"""
      Always answer 'YES' or 'NO', just single word. Your task is to validate for me does the answer on question keeps topic, is the answer related to topic.
      User question: {question}
    """

    self.setup_openai_langchain_client("gpt-3.5-turbo")    
    system_validation_response = self.langchain_service.perform_request(system_message,question_answer)
    self.answer = system_validation_response

    print(f"[PROCESSING DETAILS] Validation result: {system_validation_response}")

  def __get_answer_on_question_from_aidevs(self, question: str) -> str:
    url = f"{self.base_task_url}/{self.aidevs_token}"
    body = {
      "question": question
    }

    response = requests.post(url=url, data=body)

    return response.json().get("answer")


