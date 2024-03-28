import io
from typing import List, Optional
from openai import OpenAI


class OpenAIService:
  def __init__(self, openai_token: str, model: str):
    self.model = model
    self.openai_client = OpenAI(
      api_key=openai_token
    )
  
  def send_message_to_text_model(self, system_message: Optional[str], user_message: Optional[str], stream=False) -> str:
    openai_message = []

    if system_message:
      openai_message.append({"role": "system","content": system_message})
    if user_message:
      openai_message.append({"role": "user","content": user_message})

    openai_response = self.openai_client.chat.completions.create(
      model=self.model,
      messages=openai_message,
      stream=stream
    )

    if stream:
      response = []
      for chunk in openai_response:
        if chunk.choices[0].delta.content is not None:
          response.append(chunk.choices[0].delta.content)
    else:
      response = openai_response.choices[0].message.content

    return response

  def moderate_input_text(self, text_to_moderate: str, model:str = "text-moderation-latest"):
    response = self.openai_client.moderations.create(
      model=model,
      input=text_to_moderate
    )

    return response.results
  
  def get_embedding(self, input:str) -> List[float]:
    return self.openai_client.embeddings.create(
      input=[input],
      model=self.model
    ).data[0].embedding
  
  def get_translation(self, mp3_file: bytes) -> str:
     mp3_file_like = io.BytesIO(mp3_file)
     mp3_file_like.name = "file.mp3"

     return self.openai_client.audio.transcriptions.create(
      model=self.model,
      file=mp3_file_like
    ).text
