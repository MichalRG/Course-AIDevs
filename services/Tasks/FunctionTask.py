from services.TaskService import TaskService


class FunctionTask(TaskService):
  def perform_task(self):
    self.answer = {
      "name": "addUser",
      "description": "Add new user to database",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "name of the user"
          },
          "surname": {
            "type": "string",
            "description": "surname of the user"
          },
          "year": {
            "type": "integer",
            "description": "year of birthday"
          }
        }
      }
    }
    