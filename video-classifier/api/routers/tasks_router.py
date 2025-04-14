from typing import Union

from fastapi import APIRouter, BackgroundTasks
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ..internal.tasks import classify_video_task

router = APIRouter()


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


@router.post("/notify/", tags=["tasks"])
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


@router.get("/status/", tags=["tasks"])
async def get_prediction_status():
    """
    Get the status of the prediction task. This is a placeholder function.
    """
    return {"status": "Prediction task is in progress"}
