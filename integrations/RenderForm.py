import json
import os
import requests


class RenderForm():
  def __init__(self) -> None:
    self.key = os.getenv("APIKEY-renderfrom")

  def render_image_with_text(self, template_id: str, title: str, image_url: str) -> str:
    data = {
      "template": template_id,
      "data": {
        "title": title,
        "image-url": image_url
      }
    }
    
    response = json.loads(requests.post("https://get.renderform.io/api/v2/render", json=data, headers={
      "X-API-KEY": self.key,
      "Content-Type": "application/json"
    }).content)

    return response.get("href", "")
