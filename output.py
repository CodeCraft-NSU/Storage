from fastapi import APIRouter, HTTPException, File, UploadFile, Form
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