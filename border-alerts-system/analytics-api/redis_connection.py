import os
import redis

def get_redis_client():
    r = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True)
    return r