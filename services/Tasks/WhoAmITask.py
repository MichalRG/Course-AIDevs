import json
from services.TaskService import TaskService


class WhoAmITask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client = "langchain"):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client

  def perform_task(self):
    #below system prompt works maybe in 60% for 3.5 and 100% for 4 in 10 attempts
    system_message_attemp_one_works_well_with_gpt_4 = """
      Use below context and your general knowledge to answer user question. Answer is always something/someone specific not a general concept.
      Return short briefly precisley, answer without any description only if u're 100% otherwise return word "hint"
      Before u make decision take a deep breath and consider are u sure for sure.

      Context###
    """
    #secon version of system prompt - IMO works better then previous one with GPT-3.5 it still makes errors but it's better. I finally force it to ask eagerly for hints ;_;
    system_message = """
      When responding to the user's question, prioritize providing a direct and specific name or identifier relevant to the query. Your response should be concise and to the point, focusing solely on delivering an exact answer. If the question is about a person, respond with the person's name; if it's about a place, the name of the place; and so on.

      If you do not have enough information to confidently provide a specific name or identifier, or if the query does not have a straightforward answer based on the provided context and your general knowledge, simply reply with "hint" to indicate the need for more details.

      Please avoid offering general explanations or broader concepts unless they are directly requested by the user. The aim is to ensure clarity and precision in the response, aligning closely with the user's expectations for specific information.

      Context###
    """
    user_message = "Who am I?"
    send_message_to_model = self.get_method_adjusted_to_client("gpt-3.5-turbo", "perform_request")
    max_attempts = 10
    current_attempt = 0

    while not self.answer and current_attempt < max_attempts:
      hint = self.task_data.get("hint", "")
      
      if not hint in system_message:
        system_message += f"\n{hint}"

        response = send_message_to_model(system_message, user_message)
        print(f"[PROCESSING DETAILS]: Attempt {current_attempt}:\n {response}")
        
        if response.lower() != "hint":
          self.answer = response
          return
    
      self.get_task()
      current_attempt += 1

    raise Exception("ITS A DISASTER! We wasn't able to guess person :(")
