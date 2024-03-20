from services.TaskService import TaskService


class HelloApiTask(TaskService):
    def perform_task(self) -> str:
        self.answer = self.task_data.get("cookie")