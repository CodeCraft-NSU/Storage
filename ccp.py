from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os, shutil, tarfile

router = APIRouter()

def init_ccp_folder(pid):
    try:
        base_path = "/data/CCP"
        folder_path = os.path.join(base_path, str(pid))
        os.makedirs(base_path, exist_ok=True)
        os.makedirs(folder_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating folder: {e}")
        return False

@router.post("/ccp/push")
async def api_ccp_push(pid: int):
    remote_folder = f'/data/PMS/{pid}'
    archive_path = f'/tmp/{pid}_output.tar.gz'

    with tarfile.open(archive_path, 'w:gz') as tar:
        tar.add(remote_folder, arcname=os.path.basename(remote_folder))

    return FileResponse(archive_path, media_type='application/gzip', filename=f"{pid}_output.tar.gz")

@router.post("/ccp/pull")
async def api_ccp_pull(
    pid: int = Form(...),
    file: UploadFile = File(...),
    name: str = Form(...)
):
    if not init_ccp_folder(str(pid)):
        raise HTTPException(status_code=500, detail="Failed to initialize folder")
    file_path = f"/data/CCP/{pid}/{name}"
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"RESULT_CODE": 200, "RESULT_MSG": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file upload: {str(e)}")
