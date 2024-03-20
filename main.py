import os

from services.AuthorizationService import AuthorizationService
from services.Tasks.HelloApiTask import HelloApiTask

authorization_service = AuthorizationService()

task_to_perform = os.getenv("TASK")
token = authorization_service.get_token(task_to_perform)


def create_hello_api_instance_task(token: str) -> HelloApiTask:
    return HelloApiTask(token)


match task_to_perform:
    case 'helloapi':
        task_instance = create_hello_api_instance_task(token)
    case _:
        task_instance = create_hello_api_instance_task(token)

task_instance.get_task()
task_instance.perform_task()
task_instance.send_answer()