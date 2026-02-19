import json
from fastapi import FastAPI
from routes import router
from mongo_connection import *
from redis_connection import *
from fastapi import FastAPI, UploadFile, File, HTTPException


app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
        return {"message": "api is running"}
    
@app.post("/border_alerts")
def upload_orders(file: UploadFile = File(...)):
    try:
        content = file.file.read()
        alerts = json.loads(content)
    
        return {"message": f"Successfully processed{alerts} "}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
