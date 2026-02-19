import json
import uuid
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from kafka import KafkaProducer
from pymongo import MongoClient
import redis

app = FastAPI()

mongo_client = MongoClient("mongodb://mongo:27017")
db = mongo_client.pizza_agency
redis_client = redis.Redis(host='redis', port=6379, db=0)


def serialize_order(value):
    return json.dumps(value).encode('utf-8')

def get_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=['kafka:9092'],
                value_serializer=serialize_order            )
            print("API: Connected to Kafka successfully!")
            return producer
        except Exception as e:
            print(f"API: Waiting for Kafka to be ready... ({e})")
            time.sleep(5)

producer = get_kafka_producer()

@app.post("/orders/batch")
def upload_orders(file: UploadFile = File(...)):
    try:
        content = file.file.read()
        orders = json.loads(content)
        processed_count = 0
        
        for order in orders:
            order['order_id'] = order.get('order_id', str(uuid.uuid4()))
            order['status'] = 'PREPARING'
            if 'toppings' not in order:
                order['toppings'] = []
            db.orders.insert_one(order)
            
            if '_id' in order:
                del order['_id']
            
            producer.send("pizza-orders", value=order)
            processed_count += 1
        
        producer.flush()
        return {"message": f"Successfully processed {processed_count} orders."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/order/{order_id}")
def get_order(order_id: str):
    cached = redis_client.get(order_id)
    if cached:
        return {"source": "redis_cache", "data": json.loads(cached)}
    
    order = db.orders.find_one({"order_id": order_id}, {"_id": 0})
    if order:
        redis_client.setex(order_id, 60, json.dumps(order))
        return {"source": "mongodb", "data": order}
    
    raise HTTPException(status_code=404, detail="Order not found")