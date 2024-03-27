from typing import List
from services.TaskService import TaskService


class InpromptTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None):
    super().__init__(aidevs_token, openai_token)

    self.setup_openai_langchain_client("gpt-3.5-turbo")
  
  def perform_task(self):
    data = self.task_data.get("input", [])
    question = self.task_data.get("question", "")
    print(f"[PROCESSING DETAILS] question: {question}")

    person_question = self.__get_name_person_from_question(question)

    filtered_person_information = self.__filter_from_data_infromation_about_pointed_person(person_question, data)

    self.answer = self.__get_answer_on_question(question, filtered_person_information)

  def __get_answer_on_question(self, question: str, context: str) -> str:
    system_message = f"Answer in polish using only one single word. If u don't know answer IDK. Use context to get details information. Context### {context}"

    response = self.langchain_service.perform_request(system_message, question)

    print(f"[PROCESSING DETAILS] The answer on question is: {response}")
    return response


  def __filter_from_data_infromation_about_pointed_person(self, name: str, data: List[str]) -> str:
    for person_information_context in data:
      if name in person_information_context:
        return person_information_context
      
    raise Exception(f"Lack of information about {name}")


  def __get_name_person_from_question(self, question:str) -> str:
    system_message = "You will get question in polish language, try to understand the question keep your time. When you will understand the question, then return single word, the name of person whom this question applies, don't answer question! Just give single word the name of this person."
    
    name = self.langchain_service.perform_request(
      system_message=system_message,
      user_message=question
    )

    print(f"[PROCESSING DETAILS] The question ask about {name}")
    return name

