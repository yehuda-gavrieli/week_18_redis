
def calculate_priority(alert):
    if alert.get("weapons_count", 0) > 0:
        return "URGENT"
    
    if alert.get("distance_from_fence_m", 1000) <= 50:
        return "URGENT"
    
    if alert.get("people_count", 0) >= 8:
        return "URGENT"
    
    if alert.get("vehicle_type") == "truck":
        return "URGENT"
    
    if alert.get("distance_from_fence_m", 1000) <= 150 and alert.get("people_count", 0) >= 4:
        return "URGENT"
    
    if alert.get("vehicle_type") == "jeep" and alert.get('people_count', 0) >= 3:
        return "URGENT"
        
    return "NORMAL"