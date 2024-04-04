from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, UpsertOperation, PointsList, ScoredPoint


"""
QdrantService works based on localhost instance so to use Qdrant VectorDatabase it's required to
- run docker container with database on 6333 port OR
- run localhost app with database
"""
class QdrantService:
  def __init__(self, collection_name: str) -> None:
    self.client = QdrantClient(url="http://localhost:6333")
    self.collection_name = collection_name

  def get_collections(self):
    return self.client.get_collections().collections

  def delete_collection(self, name: Optional[str] = None):
    response = self.client.delete_collection(name or self.collection_name)

    print(f"[QDRANT] Delete status success:{response}")
  
  def create_collection(self, vector_size: int, name: Optional[str] = None):
    collection_name = name or self.collection_name
    collection_list = self.get_collections()
    if not collection_name in [colection.name for colection in collection_list]:
      response = self.client.create_collection(
        collection_name="unknown_collection",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
      )
      print(f"[QDRANT] Create attempt proceed with success status:{response}")


  def put_vectors_into_collection(self, points):
    pointsStruct = [
      PointStruct(
        id=point['id'],
        vector=point['vector'].tolist() if hasattr(point['vector'], "tolist") else point['vector'],
        payload=point['payload']
      ) for point in points
    ]
     
    response = self.client.batch_update_points(
      collection_name="unknown_collection",
      update_operations=[
        UpsertOperation(
          upsert=PointsList(
            points=pointsStruct
          )
        )
      ]
    )

    print(f"[QDRANT] Put vector status for operation index 0: {response[0].status}")

  def get_data(self, name: Optional[str] = None, limit = 10):
    search_result = self.client.scroll(
      collection_name=name or self.collection_name, limit=limit, with_payload=True, with_vectors=True
    )

    print(f"[QDRANT] Found records: {len(search_result[0])}")

    return search_result

  def get_vectors(self, vector: List[float], name: Optional[str] = None) -> List[ScoredPoint]:
    search_result = self.client.search(
      collection_name=name or self.collection_name, query_vector=vector
    )
    
    print(f"[QDRANT] search_result: {search_result}")

    return search_result
