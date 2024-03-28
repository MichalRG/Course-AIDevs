import os
import traceback

from services.AuthorizationService import AuthorizationService
from services.Tasks.BloggerTask import BloggerTask
from services.Tasks.EmbeddingTask import EmbeddingTask
from services.Tasks.HelloApiTask import HelloApiTask
from services.Tasks.InpromptTask import InpromptTask
from services.Tasks.LiarTask import LiarTask
from services.Tasks.ModerationTask import ModerationTask
from services.Tasks.WhisperTask import WhisperTask
from utils.config_manager import load_env_variables

authorization_service = AuthorizationService()

local_variables = load_env_variables()
task_to_perform = local_variables.get("TASK", "helloapi").strip()
client = local_variables.get("CLIENT", 'langchain').strip()
openai_token = os.getenv("APIKEY-OPENAI") 
aidevs_token = authorization_service.get_token(task_to_perform)

if not aidevs_token:
    print("ERROR: Lack of token from AI DEVS")
    exit(1)

try:
    def create_hello_api_instance_task() -> HelloApiTask:
        return HelloApiTask(aidevs_token)

    def create_blogger_instance_task() -> BloggerTask:
        return BloggerTask(aidevs_token, openai_token)
    
    def create_moderation_instance_task() -> ModerationTask:
        return ModerationTask(aidevs_token, openai_token)
    
    def create_liar_instance_task() -> LiarTask:
        return LiarTask(aidevs_token, openai_token)

    def create_inprompt_instance_task() -> InpromptTask:
        return InpromptTask(aidevs_token, openai_token)
    
    def create_embedding_instance_task() -> EmbeddingTask:
        return EmbeddingTask(aidevs_token, openai_token, client)
    
    def create_whisper_instance_task() -> WhisperTask:
        return WhisperTask(aidevs_token, openai_token, client)

except Exception as ex:
    print(f"ERROR: The problem occured during initalization task {task_to_perform}. Error msg: {ex}")


match task_to_perform:
    case "helloapi":
        task_instance = create_hello_api_instance_task()
    case "blogger":
        task_instance = create_blogger_instance_task()
    case "moderation":
        task_instance = create_moderation_instance_task()
    case "liar":
        task_instance = create_liar_instance_task()
    case "inprompt":
        task_instance = create_inprompt_instance_task()
    case "embedding":
        task_instance = create_embedding_instance_task()
    case "whisper":
        task_instance = create_whisper_instance_task()
    case _:
        task_instance = create_hello_api_instance_task()

try:
    task_instance.get_task()
    task_instance.perform_task()
    task_instance.send_answer()
except Exception as ex:
    print(f"ERROR: The problem occured during processing task {task_to_perform}. Error msg: {ex}")
    print(traceback.print_tb(ex.__traceback__))