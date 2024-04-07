from integrations.Qdrant.QdrantService import QdrantService
from services.TaskService import TaskService
from utils.requests_helper import get_json_data_from_url


class PeopleTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client = "langchain", collection_name='people_collection'):
    super().__init__(aidevs_token, openai_token)
    
    self.base_client = client;
    self.qdrant_service = QdrantService(collection_name)
  
  def perform_task(self):
    people = get_json_data_from_url("https://tasks.aidevs.pl/data/people.json")
    embeddings, question_embedded = self.__generate_people_embeddings(people)

    vector_length = len(embeddings[0]["vector"])
    
    self.qdrant_service.delete_collection()
    self.qdrant_service.create_collection(vector_size=vector_length)
    self.qdrant_service.put_vectors_into_collection(embeddings)  
    results = self.qdrant_service.get_vectors(question_embedded)

    best_results = results[:5]
    best_result_string_data = ""

    for best_result in best_results:
      best_result_string_data += f"Na imie mam {best_result.payload.get('imie','')} {best_result.payload.get('nazwisko','')}. Mam {best_result.payload.get('wiek','')} lat. {best_result.payload.get('o_mnie','')}. Mój ulubiony kolor to {best_result.payload.get('ulubiony_kolor', '')}. Ulubiony serial {best_result.payload.get('ulubiony_serial','')}. Ulubiony film {best_result.payload.get('ulubiony_fil','')}. Z Kapitana bomby najbardziej lubię {best_result.payload.get('ulubiona_postac_z _kapitana_bomby','')}"
    
    system_message = f"Answer shortly and briefly focus on question, don't add any additional information. To answer question use context. Context### {best_result_string_data}"
    user_prompt = self.task_data.get("question", "")
    self.setup_openai_langchain_client("gpt-3.5-turbo")    
    self.answer = self.langchain_service.perform_request(system_message,user_prompt)


  def __generate_people_embeddings(self, people):
    get_embedding = self.get_method_adjusted_to_client("text-embedding-ada-002", "get_embedding")
    embeddings = [get_embedding(f"Na imie mam {person.get('imie','')} {person.get('nazwisko','')}. Mam {person.get('wiek','')} lat. {person.get('o_mnie','')}. Mój ulubiony kolor to {person.get('ulubiony_kolor', '')}. Ulubiony serial {person.get('ulubiony_serial','')}. Ulubiony film {person.get('ulubiony_fil','')}. Z Kapitana bomby najbardziej lubię {person.get('ulubiona_postac_z _kapitana_bomby','')}") for person in people]
    
    question_embedded = get_embedding(self.task_data.get("question", ""))

    return (
      [
        {
          "id": idx,
          "vector": embedding, 
          "payload": person
        } for idx, (embedding, person) in enumerate(zip(embeddings, people), 1)
      ], 
      question_embedded
    )
