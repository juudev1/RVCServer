import os
from fastapi import Form, File, UploadFile, FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from jrvc.inference import Inference
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import shutil

app = FastAPI()
# Directorio donde se guardarán los archivos
upload_directory = "uploads"

if not os.path.exists(upload_directory):
    os.mkdir(upload_directory)

class Base(BaseModel):
    url: Optional[str] = None
    method: Optional[str] = None

def deleteFiles(files_and_directories):
    for item in files_and_directories:
        if os.path.isfile(item):
            # Elimina archivos si es un archivo
            os.remove(item)
        elif os.path.isdir(item):
            # Elimina directorios y su contenido si es un directorio
            shutil.rmtree(item)

@app.post("/convert/")
async def conversion(
    base: Base = Depends(),
    audio: UploadFile = File(...),
):
    audio_path = os.path.join(upload_directory, audio.filename)
    with open(audio_path, "wb") as f:
        f.write(audio.file.read())
        
    data = base.dict()
    model_url = data.get('url')
    if model_url:
        print("Converting...")
        infer = Inference(source_audio_path=audio_path, auto_remove=True)
        output = infer.infer_by_model_url(model_url)
        
        return FileResponse(output, background=BackgroundTask(deleteFiles, [audio_path, output, infer.model_dir]))
    
    return None