from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os

router = APIRouter()

@router.post("/output/otherdoc_add")
async def add_other_document(
    file: UploadFile = File(...),
    fuid: int = Form(...),
    pid: int = Form(...),
    userid: int = Form(...),
):
    UPLOAD_DIR = f"/data/PMS/{pid}/ETC"

    try:
        uploaded_date = datetime.now().strftime("%y%m%d-%H%M%S")
        original_format = file.filename.split('.')[-1]
        new_file_name = f"{fuid}_{uploaded_date}_{userid}.{original_format}"
        file_path = os.path.join(UPLOAD_DIR, new_file_name)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {
            "RESULT_CODE": 200,
            "RESULT_MSG": "File uploaded successfully",
            "FILE_NAME": new_file_name,
            "fuid": fuid,
            "uploaded_date": uploaded_date,
            "userid": userid,
            "original_format": original_format,
            "FILE_PATH": file_path,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file upload: {str(e)}")

@router.post("/output/otherdoc_download")
async def download_otherdoc(file_path: str = Form(...)):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on storage server")
    print(file_path)
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type='application/octet-stream'
    )

@router.post("/output/attach_add")
async def attach_add(
    file: UploadFile = File(...),
    fuid: int = Form(...),
    pid: int = Form(...),
    userid: int = Form(...),
    doc_type: int = Form(...)  # 산출물 종류 (1: 개요서, 2: 요구사항, 3: 회의록, 4: 보고서)
):
    # 1: 프로젝트 개요서 -> OD, 2: 요구사항 명세서 -> RS, 3: 회의록 -> MM, 4: 보고서 -> SD
    folder_mapping = {1: "OD", 2: "RS", 3: "MM", 4: "SD"}
    folder = folder_mapping.get(doc_type, "ETC")
    UPLOAD_DIR = f"/data/PMS/{pid}/{folder}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    try:
        uploaded_date = datetime.now().strftime("%y%m%d-%H%M%S")
        original_format = file.filename.split('.')[-1]
        new_file_name = f"{fuid}_{uploaded_date}_{userid}.{original_format}"
        file_path = os.path.join(UPLOAD_DIR, new_file_name)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {
            "RESULT_CODE": 200,
            "RESULT_MSG": "File uploaded successfully",
            "FILE_NAME": new_file_name,
            "fuid": fuid,
            "uploaded_date": uploaded_date,
            "userid": userid,
            "original_format": original_format,
            "FILE_PATH": file_path,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file upload: {str(e)}")