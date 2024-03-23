from typing import List
from services.TaskService import TaskService


class ModerationTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None):
    super().__init__(aidevs_token, openai_token)

    self.setup_openai_client(model="gpt-3.5-turbo")


  def perform_task(self):
    content_to_moderate = self.task_data.get("input", [])

    banned_conntent: List[int] = []
    for content in content_to_moderate:
      moderation_result = self.openai_service.moderate_input_text(content)

      banned_conntent.append(1 if moderation_result[0].flagged else 0)

    print(f"[PROCESSING DETAILS]: Banned content: {banned_conntent}")

    self.answer =banned_conntent
