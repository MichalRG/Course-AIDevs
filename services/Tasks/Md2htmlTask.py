from services.TaskService import TaskService


class Md2htmlTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None):
    super().__init__(aidevs_token, openai_token)
    self.base_client = 'openai'
  
  def perform_task(self):
    method_to_process = self.get_method_adjusted_to_client('ft:gpt-3.5-turbo-0125:personal:md2htmlv4-1:9FdGVcnj','send_message_to_text_model')

    system_prompt = """
      Use md2html translation (markdown to html).
      Focus on your task return only formatted text nothing more, don't add any additional information.
      Don't answer question focus on translation to html!
      Remember special rule for bold text!
      Take a deep breath before you answer and focus on task!
    """
    user_prompt = self.task_data.get("input")

    translated_text = method_to_process(system_prompt, user_prompt)

    print(f"[PROCESSING DETAILS] translated text: {translated_text}")

    self.answer = translated_text.replace("'", "\"")

