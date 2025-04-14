from internal.tasks import classify_video_task
from pydantic import BaseModel, Field
from fastapi import APIRouter, BackgroundTasks
from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import os

if not os.path.exists("static"):
    os.makedirs("static")

app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")


@app.get("/")
async def main():
    content = """
<body>
<form action="/api/uploadvideo/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
<form action="/api/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


class Task(BaseModel):
    """
    Task model for prediction tasks.
    """
    task_id: str = Field(..., description="Unique identifier for the task")
    status: str = Field(..., description="Status of the task")
    result: Union[str, None] = Field(None, description="Result of the task")
    error: Union[str, None] = Field(None, description="Error message if any")


class CreateTaskRequest(BaseModel):
    """
    Request model for creating a new task.
    """
    video_id: str = Field(..., description="Unique identifier for the video")
    video_url: str = Field(..., description="URL of the video to be processed")
    callback_url: str = Field(...,
                              description="URL to send the result back to")


@app.post("/tasks/notify/", tags=["tasks"])
async def create_new_prediction_task(background_tasks: BackgroundTasks, request: CreateTaskRequest) -> Task:
    """
    Create a new prediction task. This is a placeholder function.
    """
    task = Task(
        task_id="12345",
        status="pending",
        result=None,
        error=None
    )

    background_tasks.add_task(
        classify_video_task,
        video_id=request.video_id,
        video_url=request.video_url,
        callback_url=request.callback_url
    )

    # Simulate task creation and processing
    # In a real-world scenario, you would save this task to a database
    # and update its status as the task progresses.
    # For now, we just return the task with a pending status.

    return task
