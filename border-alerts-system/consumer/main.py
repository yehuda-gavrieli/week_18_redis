import json
import datetime
from redis_connection import r
from mongo_connection import *


def run_consumer():
    while True:
        data = r.blpop(["urgent_queue", "normal_queue"])
        if data:
            alert = json.loads(data[1])
            alert["insertion_time"] = datetime.datetime.now().isoformat()
            collection.insert_one(alert)

if __name__ == "__main__":
    run_consumer()