from pydantic import BaseModel

class TodoIn(BaseModel):
    task: str

class TodoOut(BaseModel):
    task_id: int
    task: str
    status: int