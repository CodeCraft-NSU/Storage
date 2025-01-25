from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os, shutil, tarfile

router = APIRouter()

@router.post("/ccp/push")
async def api_output_push(pid: int):
    remote_folder = f'/data/PMS/{pid}'
    archive_path = f'/tmp/{pid}_output.tar.gz'

    with tarfile.open(archive_path, 'w:gz') as tar:
        tar.add(remote_folder, arcname=os.path.basename(remote_folder))

    return FileResponse(archive_path, media_type='application/gzip', filename=f"{pid}_output.tar.gz")