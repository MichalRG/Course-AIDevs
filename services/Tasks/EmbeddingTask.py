from services.TaskService import TaskService


class EmbeddingTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client: str = "langchain"):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client;


  def perform_task(self):
    input_text = "Hawaiian pizza"

    get_embedding = self.get_method_adjusted_to_client("text-embedding-ada-002", "get_embedding")

    self.answer = get_embedding(input_text)
    print(f"[PROCESSING DETAILS]: {len(self.answer)}, first 10 elements: {self.answer[:10]}")
