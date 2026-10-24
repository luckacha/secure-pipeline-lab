from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Todo App")


class TaskCreate(BaseModel):
    title: str


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


tasks: dict[int, Task] = {}
next_id = 1


@app.get("/tasks")
def list_tasks() -> list[Task]:
    return list(tasks.values())


@app.post("/tasks", status_code=201)
def create_task(data: TaskCreate) -> Task:
    global next_id
    task = Task(id=next_id, title=data.title)
    tasks[task.id] = task
    next_id += 1
    return task


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.patch("/tasks/{task_id}/done")
def complete_task(task_id: int) -> Task:
    task = get_task(task_id)
    task.done = True
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    get_task(task_id)
    del tasks[task_id]
