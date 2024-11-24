from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class project_init(BaseModel):
    PUID: int

@router.post("/project/init")
async def init_file_system(payload: project_init):
    base_path = "/data/PMS"
    puid = str(payload.PUID)
    root_path = os.path.join(base_path, puid)

    folder_structure = ["WBS","MM","SD","OD","RS","UT","IT","ETC"]

    try:
        os.makedirs(root_path, exist_ok=True)
        for folder in folder_structure:
            folder_path = os.path.join(root_path, folder)
            os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        return {"RESULT_CODE": 500, "RESULT_MSG": str(e)}

    return True
