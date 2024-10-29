from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "root of PMS Storage Server API."}