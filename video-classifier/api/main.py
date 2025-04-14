from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routers import prediction, tasks_router

import os


if not os.path.exists("static"):
    os.makedirs("static")

app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")

app.include_router(prediction.router, prefix="/api", tags=["prediction"])
app.include_router(tasks_router.router, prefix="/tasks", tags=["tasks"])


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
