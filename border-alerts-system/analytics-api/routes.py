from fastapi import APIRouter
import json
import redis
import os
from dal import DataAccessLayer

router = APIRouter()
dal = DataAccessLayer()
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, decode_responses=True)

@router.get("/analytics/top-urgent-zones")
def top_zones():
    cached = r.get("top_zones")
    if cached:
        return json.loads(cached)
    
    result = dal.get_top_zones()
    r.setex("top_zones", 60, json.dumps(result)) 
    return result