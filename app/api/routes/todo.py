from fastapi import APIRouter, Form, HTTPException, Path
from app.models.todo import TodoIn, TodoOut
from app.services.todo import TodoService

router = APIRouter()

@router.post("/tasks", response_model=TodoOut)
async def create_task(task: str = Form(...)):
    todo = await TodoService.create_task(TodoIn(task=task))
    return todo

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int = Path(...)):
    success = await TodoService.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/complete", response_model=dict)
async def complete_task(task_id: int = Path(...)):
    success = await TodoService.complete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task completed successfully"}

@router.get("/tasks", response_model=list[TodoOut])
async def get_tasks():
    tasks = await TodoService.get_all_tasks()
    return tasks