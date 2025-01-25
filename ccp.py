from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os

router = APIRouter()

@router.post("/ccp/push")
async def api_output_push():
    return