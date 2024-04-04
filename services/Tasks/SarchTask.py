import json
from typing import Optional
import requests
from integrations.Qdrant.QdrantService import QdrantService
from services.TaskService import TaskService
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, UpsertOperation, PointsList

class SearchTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, collection_name = "unknown_collection"):
    super().__init__(aidevs_token, openai_token)
    
    self.qdrant_service = QdrantService(collection_name)

  def perform_task(self):
    self.qdrant_service.delete_collection()
    data = self.__get_newsleter_dataset()
    question = self.task_data.get("question")

    self.__prepare_database_and_data(data)
    self.__process_question(question)

  def __process_question(self, question: str):
    embeded_question = self.__generate_embeddings([{"info": question}])

    results = self.qdrant_service.get_vectors(embeded_question[0]["vector"])

    best_result = max(results, key=lambda result: result.score)

    self.answer = best_result.payload.get("url","")

  
  def __prepare_database_and_data(self, data: list[dict[str, str]]):
    embeddings = self.__generate_embeddings(data)
    vector_length = len(embeddings[0]["vector"])

    self.qdrant_service.create_collection(vector_size=vector_length)
    self.qdrant_service.put_vectors_into_collection(embeddings)
    
  def __generate_embeddings(self, data: list[dict[str,str]]):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = [model.encode(article['info']) for article in data]
    
    return [
      {
        "id": idx,
        "vector": embedding.tolist(), 
        "payload": article
      } for idx, (embedding, article) in enumerate(zip(embeddings, data), 1)
    ]

  def __get_newsleter_dataset(self) -> list[dict[str,str]]:
    return json.loads(requests.get("https://unknow.news/archiwum_aidevs.json").content)




##########################################################################################
#
###
#   Before I achive sucessful result I had many attempts below are two most promising 
###
#
##########################################################################################


# if __name__ == '__main__':
  # st = SearchTask('1','2')
  # points = st.perform_task()

  ############### ATTEMPT II - it works :)
  # client = QdrantClient(url="http://localhost:6333")

  # client.delete_collection("unknown_collection")
  # # client.delete_collection("my_collection")

  # colections = client.get_collections().collections

  # if not "unknown_collection" in [colection.name for colection in colections]:
  #   client.create_collection(
  #     collection_name="unknown_collection",
  #     vectors_config=VectorParams(size=len(points[0]['vector']), distance=Distance.COSINE),
  #   )
    
  # pointsStruct = [
  #   PointStruct(
  #     id=point['id'],
  #     vector=point['vector'].tolist() if hasattr(point['vector'], "tolist") else point['vector'],
  #     payload=point['payload']
  #   ) for point in points
  # ]
  # response = client.batch_update_points(
  #   collection_name="unknown_collection",
  #   update_operations=[
  #     UpsertOperation(
  #       upsert=PointsList(
  #         points=pointsStruct
  #       )
  #     )
  #   ]
  # )
  # print(response)

  # search_result = client.scroll(
  #   collection_name="unknown_collection", limit=10, with_payload=True, with_vectors=True
  # )

  # print(search_result)

  # search_result = client.search(
  #   collection_name="unknown_collection", query_vector=points[0]['vector']
  # )
  
  # print(search_result)

  #########################################################################
  # Ensure the collection exists before inserting
  # You may need to add additional parameters for the collection schema if required
  # collection_url = 'http://localhost:6333/collections/my_collection'
  
  #   # Check if the collection exists
  # response = requests.get(collection_url)
  # if response.status_code == 404:  # If not found, create the collection
  #     # Create the collection schema
  #     collection_schema = {
  #         "vector_size": len(points[0]['vector']),
  #         "distance": "Cosine"  # Or "Euclidean", "Dot", etc., based on your preference
  #     }
  #     response = requests.put(collection_url, json=collection_schema)
  
  #     if response.status_code != 201:
  #         print(f"Failed to create collection: {response.text}")
  #         exit(1)  # Exit if cannot create collection
  
  
  # # Insert the points into the collection
  # insert_url = f'{collection_url}/points/batch'
  # insert_payload = {
  #     "operations": [
  #         {
  #             "type": "upsert",
  #             "id": point['id'],
  #             "vector": point['vector'].tolist() if hasattr(point['vector'], "tolist") else point['vector'],
  #             "payload": point['payload']
  #         } for point in points
  #     ]   
  # }

  # response = requests.post(insert_url, json=insert_payload)
  # print(response.text)  # You can log the response or handle errors as needed

  # search_payload = {
  #   "vector": [0] * len(points[0]['vector']),  # An example zero-vector
  #   "top": 10,  # Number of closest points you want to retrieve
  #   # More parameters may be added depending on your Qdrant setup and the type of search you're performing.
  # }
  # search_url = f'{collection_url}/points/search'
  # response = requests.post(search_url, json=search_payload)
  # if response.status_code == 200:
  #     print("Search results:", response.json())
  # else:
  #     print("Search failed:", response.text)


  ### ATTEMPT TO WORK WITH MILVUS IT FAILS BECAUSE I WASNT ABLE TO RUN MILVUS LOCALY - RECEIVED ERROR WITH TINI MAYBE BECAUSE OF CPU HAVENT FOUND SOLUTION
  ### https://github.com/milvus-io/milvus/issues/27028

  # fields = [
  #   FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
  #   FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)  # Assuming embedding size of 384
  # ]
  # schema = CollectionSchema(fields, description="Article Embeddings")
  # collection_name = "articles"

  # if not collection_name in utility.list_collections():
  #   collection = Collection(name=collection_name, schema=schema)
  # else:
  #     collection = Collection(name=collection_name)

  # data = {
  #   "embedding": embedings
  # }

  # result_insert = mr = collection.insert(data)
  # collection.load()
