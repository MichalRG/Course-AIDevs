import base64
import requests
from services.TaskService import TaskService


class GnomeTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client = 'openai'):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client

  def perform_task(self):
    encoded_img = self.__get_encoded_img()

    send_message_with_imgs_method = self.get_method_adjusted_to_client("gpt-4-turbo", "send_message_with_imgs")

    system_propmpt = """
      Your task is to recognised does img presents gnome from fantasy worlds/tales/fables.
      If the image presents gnome then return one single word which describe the color of gnome's hat.
      If the image doesn't present gnome then return sinlge word "error"
      ALWAYS response in polish language!

      Example###
      User: What is it {{image_of_gnome_with_green_hat}}
      Response: green
      User: {{image_of_devil}}
      Response: error
    """
    user_prompt = ""

    response = send_message_with_imgs_method(system_propmpt, user_prompt, [encoded_img])

    print(f"[PROCESSING DETAILS]: Response of model: {response}")

    self.answer = response
  
  def __get_encoded_img(self) -> str:
    img_url = self.task_data.get("url")
    img_response = requests.get(img_url)

    if img_response.status_code == 200:
      return base64.b64encode(img_response.content).decode("utf-8")
    else:
      raise Exception("Problem with fetching img!")