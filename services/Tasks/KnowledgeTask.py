import json
from typing import Any, List, Optional
import requests
from services.TaskService import TaskService


class KnowledgeTask(TaskService):
  def __init__(self, aidevs_token: str, openai_token: str | None = None, client = 'langchain'):
    super().__init__(aidevs_token, openai_token)
    self.base_client = client

  def perform_task(self):
    process_request_llm = self.get_method_adjusted_to_client("gpt-3.5-turbo", "perform_request")
    prices = self.__get_current_currency_prices()
    string_which_describe_prices = self.__get_str_data_from_prices_table(prices)

    popluation = self.__get_population_data()
    string_which_describe_popluations = self.__get_str_data_from_population_talbe(popluation)

    question = self.task_data.get("question", "")

    category_of_question = self.__what_is_question_about(question, process_request_llm)
    print(f"[PROCESSING DETAILS]: Categorized as: {category_of_question}")

    match category_of_question.lower():
      case "population":
        self.answer = self.__get_answer_on_question(process_request_llm, question, string_which_describe_popluations)
      case "currency":
        self.answer = self.__get_answer_on_question(process_request_llm, question, string_which_describe_prices)
      case "general":
        self.answer = self.__get_answer_on_question(process_request_llm, question)

  def __get_answer_on_question(self, method_llm_request, question:str, str_data: Optional[str] = None) -> str:
    system_message = f"""
      Use below context or your general knowledge to answer briefly, short and precisely on question. Try to answer in just single word if it's possible.

      Context###
      {str_data or ''}
    """
    user_prompt = question

    response = method_llm_request(system_message, user_prompt)

    print(f"[PROCESSING DETAILS]: Response of model: {response}")

    return response


  def __what_is_question_about(self, question: str, method_request_llm) -> str:
    system_message = """
      Behave like a categorzier, always answer only in one word! You have to choose one of three categories to which belogns the question.
      There are 3 categories: "population", "currency", "general". If the question is about exchange rate/ currency return string "currency".
      If the question is about population of country return "population". If it doesnt match to any of these two then return "general"

      Example###
      User: How many people live in New Zeland?
      You: population
    """
    user_message = question

    return method_request_llm(system_message, user_message)
  
  def __get_current_currency_prices(self) -> List[dict[str, Any]]:
    return json.loads(requests.get("http://api.nbp.pl/api/exchangerates/tables/A").content)
  
  def __get_str_data_from_prices_table(self, data) -> str:
    price_string = ""

    for currency in data[0].get("rates"):
      price_string += f"{currency.get('currency','')}, price: {currency.get('mid', '')}\n"
    
    return price_string
  
  def __get_population_data(self) -> List[dict[str, Any]]:
    return json.loads(requests.get("https://restcountries.com/v3.1/all?fields=name,population").content)
  
  def __get_str_data_from_population_talbe(self, data) -> str:
    popluation_string = ""

    for country in data:
      popluation_string += f"{country.get('name',{}).get('official', '')}, population: {country.get('population','')}\n"

    return popluation_string