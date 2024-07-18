from app.core.database import database
from app.models.todo import TodoIn, TodoOut

class TodoService:
    @staticmethod
    async def create_task(task: TodoIn) -> TodoOut:
        count = await database.tasks.count_documents({})
        task_id = count + 1
        doc = {
            'task_id': task_id,
            'task': task.task,
            'status': 0
        }
        await database.tasks.insert_one(doc)
        return TodoOut(**doc)

    @staticmethod
    async def delete_task(task_id: int) -> bool:
        result = await database.tasks.delete_one({'task_id': task_id})
        return result.deleted_count > 0

    @staticmethod
    async def complete_task(task_id: int) -> bool:
        result = await database.tasks.update_one(
            {'task_id': task_id},
            {'$set': {'status': 1}}
        )
        return result.modified_count > 0

    @staticmethod
    async def get_all_tasks() -> list[TodoOut]:
        tasks = await database.tasks.find({}, {'_id': False}).to_list(None)
        return [TodoOut(**task) for task in tasks]