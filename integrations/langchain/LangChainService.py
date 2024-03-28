from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class LangChainProvider:
  def __init__(self, key:str, model: str = "gpt-3.5-turbo", provider: str = "OpenAI"):
    match provider:
      case 'OpenAI':
        self.llm_langchain_client = ChatOpenAI(openai_api_key=key, model=model)
        self.embeddings = OpenAIEmbeddings(openai_api_key=key, model=model)
      case _:
        self.llm_langchain_client = ChatOpenAI(openai_api_key=key)

  def perform_request(self, system_message: str, user_message: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
      ("system", system_message),
      ("user", "{input}")
    ])
    parser = StrOutputParser()
    
    chain = prompt | self.llm_langchain_client | parser

    return chain.invoke({"input": user_message})

  def get_embedding(self, input_text:str) -> List[float]:
    return self.embeddings.embed_documents([input_text])[0]
  
  def get_translation(self, mp3_file: bytes):
    raise Exception("Lack of implementation for python langchain whipser. I only found Community Solution #meh and js solution 💣")    

