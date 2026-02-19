from fastapi import APIRouter
import dal

router = APIRouter()

@router.get("/alerts-by-border-and-priority")
def alerts_border_and_priority():
    return dal.get_alerts_border_and_priority()

@router.get("/top-urgent-zones")
def top_zones_rgent():
    return dal.get_top_zones_rgent()

@router.get("/distance-distribution")
def distance_distribution():
    return dal.get_distance_distribution()

@router.get("/low-visibility-high-activity")
def low_visibility_high_activity():
    return dal.get_low_visibility_high_activity()

@router.get("/hot-zones")
def hot_zones():
    return dal.get_hot_zones()