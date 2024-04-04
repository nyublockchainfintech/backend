from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
async def read_root():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": "hello", "current_time": current_time}

