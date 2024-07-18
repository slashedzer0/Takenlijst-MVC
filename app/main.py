import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.routes import todo

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(todo.router, prefix="/api")

@app.get("/")
async def home(request: Request):
    await asyncio.sleep(1)  # Simulating the time.sleep(1) from Flask
    hint = 'Task is saved successfully.'
    return templates.TemplateResponse("index.html", {"request": request, "hint": hint})

@app.get("/todos")
async def todos(request: Request):
    return templates.TemplateResponse("todos.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)