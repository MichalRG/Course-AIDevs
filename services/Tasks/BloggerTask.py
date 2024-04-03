import json
from services.TaskService import TaskService


class BloggerTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None):
    super().__init__(aidevs_token, openai_token)

    self.setup_openai_client(model="gpt-3.5-turbo")

  def perform_task(self):
    chapters = str(self.task_data.get("blog"))

    system_message = """
    Behave like a journalist. 
    The return response should have form of json with property answer, and value array of string. 
    Each string should contains description for one chapter, it should be blog post so it has to contains some text for each paragrpah. 
    Example### 
    User:["Wstęp: kilka słów na temat historii pizzy","Niezbędne składniki na pizzę","Robienie pizzy","Pieczenie pizzy w piekarniku"]
    You:{"answer":["description for Wstęp", "description for niezbędne składniki", "Description for robienie pizzy", "Description for pieczenie pizzy"]}
    User:["Wstęp: co to modele LLM","Najbardziej popularne LLM","Porównanie LLMów"]
    You:{"answer":["description for Wstęp", "description for popularne LLM", "Description for porównanie LLMów"]}
    ###
    Write the response in answer array in polish language! 
    ]"""
    user_prompt_message = f"{chapters}"
    
    response = self.openai_service.perform_request(
      system_message=system_message, 
      user_message=user_prompt_message
    )

    parsed_response = self.__try_to_parse_response(response=response)
    self.answer = parsed_response.get("answer", [])

    print(f"[PROCESSING DETAILS]: {response}")

  def __try_to_parse_response(self, response:str) -> dict:
    try:
      return json.loads(response)
    except Exception as ex:
      return {}
    
    
