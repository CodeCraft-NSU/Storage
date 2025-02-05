from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import os, shutil, tarfile, logging

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

@router.post("/ccp/push_ccp")
async def api_ccp_push_ccp(
    pid: int = Query(..., description="Project ID"),
    ver: int = Query(..., description="Version number of the CCP file")
):
    file_path = f"/data/CCP/{pid}/{pid}_{ver}.ccp"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CCP file not found")
    
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"{pid}_{ver}.ccp"
    )

@router.post("/ccp/pull_output")
async def api_ccp_pull_output(
    pid: int = Form(..., description="Project ID"),
    file: UploadFile = File(..., description="Compressed OUTPUT folder archive (tar.gz)"),
    name: str = Form(..., description="Filename for the OUTPUT archive")
):
    pms_folder = f"/data/PMS/{pid}"
    try:
        if os.path.exists(pms_folder):
            for entry in os.listdir(pms_folder):
                entry_path = os.path.join(pms_folder, entry)
                try:
                    if os.path.isfile(entry_path) or os.path.islink(entry_path):
                        os.unlink(entry_path)
                    elif os.path.isdir(entry_path):
                        shutil.rmtree(entry_path)
                except Exception as e:
                    logging.error(f"Failed to delete {entry_path}: {str(e)}")
        else:
            os.makedirs(pms_folder, exist_ok=True)
        logging.info(f"Cleaned up files in folder: {pms_folder}")
    except Exception as e:
        logging.error(f"Failed to clean PMS folder for pid {pid}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clean PMS folder: {str(e)}")
    archive_path = os.path.join(pms_folder, name)
    try:
        with open(archive_path, "wb") as f:
            f.write(await file.read())
        logging.info(f"Successfully saved OUTPUT archive to {archive_path}")
    except Exception as e:
        logging.error(f"Error during file upload for pid {pid}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during file upload: {str(e)}")
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=pms_folder)
        logging.info(f"Extracted OUTPUT archive in folder: {pms_folder}")
        os.remove(archive_path)
        logging.info(f"Removed archive file: {archive_path}")
    except Exception as e:
        logging.error(f"Error during extraction of OUTPUT archive for pid {pid}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during extraction of OUTPUT archive: {str(e)}")
    
    return JSONResponse(content={"RESULT_CODE": 200, "RESULT_MSG": "Output file uploaded and extracted successfully"})
