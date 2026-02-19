import json
from mongo_connection import get_mongo_client
from redis_connection import get_redis_client


db = get_mongo_client()
cache = get_redis_client()
TTL = 300 

def get_cached_or_query(cache_key, pipeline):
    cached_data = cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    result = list(db.aggregate(pipeline))
    
    cache.setex(cache_key, TTL, json.dumps(result))
    return result



def get_alerts_border_and_priority():
    pipeline = [
        {"$group": {
            "_id": {"border": "$border", "priority": "$priority"},
            "count": {"$sum": 1}
        }}
    ]
    return get_cached_or_query("alerts_border_and_priority", pipeline)



def get_top_zones_rgent():
    pipeline = [
        {"$match": {"priority": "URGENT"}},
        {"$group": {"_id": "$zone", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    return get_cached_or_query("get_top_zones_rgent", pipeline)



def get_distance_distribution():
    pipeline = [
        {"$bucket": {
            "groupBy": "$distance_from_fence_m",
            "boundaries": [0,300, 800, 1500],
            "default": "Far",
            "output": {"count": {"$sum": 1}}
        }}
    ]
    return get_cached_or_query("distance_distribution", pipeline)



def get_low_visibility_high_activity():
    pipeline = [
        {"$match": {"visibility_quality": {"$lt": 0.4}, "people_count": {"$gt": 2}}},
        {"$group": {"_id": "$zone", "alert_count": {"$sum": 1}}}
    ]
    return get_cached_or_query("low_visibility_high_activity", pipeline)



def get_hot_zones():
    pipeline = [
        {"$match": {"priority": "URGENT"}},
        {"$group": {
            "_id": "$zone",
            "urgent_count": {"$sum": 1},
            "avg_distance": {"$avg": "$distance_from_fence_m"}
        }},
        {"$match": {"urgent_count": {"$gt": 3}, "avg_distance": {"$lt": 100}}}
    ]
    return get_cached_or_query("hot_zones", pipeline)