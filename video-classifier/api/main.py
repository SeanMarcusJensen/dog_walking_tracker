from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

from ultralytics import YOLO
import numpy as np
import cv2
import base64
from io import BytesIO

model = YOLO("yolo11n.pt")

def predict(img):
    results = model.predict(source=img, save=True, save_txt=True, save_conf=True)
    return results

app = FastAPI()


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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}