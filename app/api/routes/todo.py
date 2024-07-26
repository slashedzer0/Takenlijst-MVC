from fastapi import APIRouter, Form, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from app.models.todo import TodoIn, TodoOut
from app.services.todo import TodoService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/tasks")
async def create_task(request: Request, task: str = Form(...)):
    todo = await TodoService.create_task(TodoIn(task=task))
    return templates.TemplateResponse(
        "partials/task_form.html",
        {"request": request, "task_added": True}
    )


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int = Path(...)):
    success = await TodoService.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return ""


@router.patch("/tasks/{task_id}/complete")
async def complete_task(request: Request, task_id: int = Path(...)):
    success = await TodoService.complete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    task = await TodoService.get_task(task_id)
    return templates.TemplateResponse(
        "partials/task_list.html", {"request": request, "tasks": [task]}
    )


@router.get("/tasks")
async def get_tasks(request: Request):
    tasks = await TodoService.get_all_tasks()
    return templates.TemplateResponse(
        "partials/task_list.html", {"request": request, "tasks": tasks}
    )