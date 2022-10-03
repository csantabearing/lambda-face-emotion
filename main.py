from starlette.responses import StreamingResponse
from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
import io

#We generate a new FastAPI app in the Prod environment
#https://fastapi.tiangolo.com/
app = FastAPI(title='Serverless Lambda FastAPI', root_path="/Prod/")


@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Ok"}
