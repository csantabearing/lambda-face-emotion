from starlette.responses import StreamingResponse
from fastapi import FastAPI, File, UploadFile
from emotions import Sentiment
from mangum import Mangum
import numpy as np
import base64
import cv2
import io

model_path = './model.h5'
model=Sentiment(model_path)

app = FastAPI(title='Serverless Lambda FastAPI', root_path="/Prod/")

@app.post("/face-sentiment", tags=["Sentiment Analysis"])
async def sentiment(file: UploadFile = File(...)):
    contents=await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_dimensions = str(img.shape)
    return_img = model.predict(img)
    _, png_img = cv2.imencode('.PNG', return_img)
    encoded_img = base64.b64encode(png_img)
    return StreamingResponse(io.BytesIO(png_img.tobytes()), media_type="image/png")

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "Ok"}


handler = Mangum(app=app)