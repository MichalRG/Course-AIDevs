from services.TaskService import TaskService


class EmbeddingTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client: str = "langchain"):
    super().__init__(aidevs_token, openai_token)
    self.embedding_client = client;


  def perform_task(self):
    input_text = "Hawaiian pizza"

    get_embedding = self.__get_method_adjusted_to_client()

    self.answer = get_embedding(input_text)
    print(f"[PROCESSING DETAILS]: {len(self.answer)}, first 10 elements: {self.answer[:10]}")

  def __get_method_adjusted_to_client(self):
    if self.embedding_client == "openai":
      self.setup_openai_client("text-embedding-ada-002")
      
      return self.openai_service.get_embedding
    else:
      self.setup_openai_langchain_client("text-embedding-ada-002")

      return self.langchain_service.get_embedding
