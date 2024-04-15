from integrations.RenderForm import RenderForm
from services.TaskService import TaskService


class MemeTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None):
    super().__init__(aidevs_token, openai_token)
    self.render_form_service = RenderForm()


  def perform_task(self):
    template_id = "round-devils-return-clearly-1122"
    text = self.task_data.get("text", "")
    img_url = self.task_data.get("image", "")

    url = self.render_form_service.render_image_with_text(template_id, text, img_url)

    print(f"[PROCESSING DETAILS]: url result {url}")

    self.answer=url
