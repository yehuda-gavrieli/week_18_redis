import json
import os
import redis
from priority_logic import calculate_priority

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, decode_responses=True)

def run_producer():
    with open('/app/data/border_alerts.json', 'r') as f:
        alerts = json.load(f)
    
    for alert in alerts:
        priority = calculate_priority(alert)
        alert["priority"] = priority  
        
        if priority == "URGENT":
            queue = "urgent_queue" 
        else:
            "normal_queue"
        r.rpush(queue, json.dumps(alert))

if __name__ == "__main__":
    run_producer()