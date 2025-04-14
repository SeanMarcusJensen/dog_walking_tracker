from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


from ultralytics import YOLO
import numpy as np
import cv2
import base64
from io import BytesIO
import uuid


app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")

model = YOLO("yolo11n.pt")


def predict(img):
    results = model.predict(source=img, save=True,
                            save_txt=True, save_conf=True)
    return results


class QueueItem(BaseModel):
    url: str = Field(..., description="URL of the video to be processed")


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Read image
        contents = await file.read()
        npimg = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Run YOLO prediction
        results = model.predict(img)

        # Plot results (draw boxes)
        results[0].plot()  # This draws directly on the image array
        drawn_img = results[0].plot()  # Optional: if you want to assign it

        # Convert BGR to RGB for browser
        img_rgb = cv2.cvtColor(drawn_img, cv2.COLOR_BGR2RGB)

        # Encode image to base64
        _, buffer = cv2.imencode('.jpg', img_rgb)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        # Create HTML with the image
        html_content = f"""
        <html>
            <body>
                <h2>Prediction Results for: {file.filename}</h2>
                <img src="data:image/jpeg;base64,{img_base64}" alt="Predicted image"/>
                <br><a href="/">Upload another</a>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    except Exception as e:
        return HTMLResponse(content=f"<h1>Error:</h1><p>{str(e)}</p>")


@app.post("/predict/")
async def predict_endpoint(file: UploadFile = File(...)):
    try:
        # Read image
        contents = await file.read()
        npimg = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Run YOLO prediction
        results = model.predict(img)

        # Plot results (draw boxes)
        results[0].plot()  # This draws directly on the image array
        drawn_img = results[0].plot()  # Optional: if you want to assign it

        # Convert BGR to RGB for browser
        img_rgb = cv2.cvtColor(drawn_img, cv2.COLOR_BGR2RGB)

        # Encode image to base64
        _, buffer = cv2.imencode('.jpg', img_rgb)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return {"image": img_base64}

    except Exception as e:
        return HTMLResponse(content=f"<h1>Error:</h1><p>{str(e)}</p>")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/uploadvideo/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Save the uploaded video
        input_video_path = f"static/{uuid.uuid4().hex}_{file.filename}"
        with open(input_video_path, "wb") as f:
            file = await file.read()
            f.write(file)

        # Load video
        cap = cv2.VideoCapture(input_video_path)

        # VideoWriter to save output
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        fps = cap.get(cv2.CAP_PROP_FPS)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_path = input_video_path.replace(".mp4", "_out.mp4")
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Predict on frame
            results = model.predict(frame, verbose=False)
            result_img = results[0].plot()

            # Write the frame
            out.write(result_img)

        cap.release()
        out.release()
        return RedirectResponse(url=f"/video/{output_path.split('/')[-1]}")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error:</h1><p>{str(e)}</p>")


@app.get("/video/{video_path:path}")
async def get_video(video_path: str):
    try:
        video_path = f"static/{video_path}"
        with open(video_path, "rb") as video_file:
            video_data = video_file.read()
            return HTMLResponse(content=video_data, media_type="video/mp4")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error:</h1><p>{str(e)}</p>")
