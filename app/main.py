import time
from datetime import datetime
import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from app.services.map_service import map_service
from app.services.optimizer import optimizer_service

app = FastAPI(
    title="Amman Eco-Shift AI - UNTOUCHABLE Edition",
    description="Terrain-aware, AI-Advisory, and Financial-optimized routing for Amman",
    version="4.0.0"
)

# --- Caching Layer ---
class SimpleCache:
    def __init__(self, ttl: int = 300):
        self.cache: Dict[str, Dict] = {}
        self.ttl = ttl

    def get(self, key: str):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['data']
            else:
                del self.cache[key]
        return None

    def set(self, key: str, data: Dict):
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }

cache = SimpleCache()

# --- Models ---
class Location(BaseModel):
    lat: float
    lng: float

class RouteRequest(BaseModel):
    origin: Location
    destination: Location
    vehicle_type: str = "GASOLINE"

@app.post("/optimize")
async def optimize_route(request: RouteRequest):
    """
    Elite Optimization: Traffic + Terrain + AI Advisory + Financial Impact.
    """
    cache_key = hashlib.md5(f"{request.origin}-{request.destination}-{request.vehicle_type}-v4".encode()).hexdigest()
    cached_result = cache.get(cache_key)
    if cached_result:
        return {**cached_result, "cached": True}

    amman_time = datetime.now().strftime("%I:%M %p")

    try:
        # 1. Fetch Routes
        routes_response = await map_service.get_fuel_efficient_route(
            request.origin.lat, request.origin.lng,
            request.destination.lat, request.destination.lng,
            request.vehicle_type
        )
        
        if "error" in routes_response:
            raise HTTPException(status_code=400, detail=routes_response["error"])
        
        # 2. Process Routes
        optimized_routes = []
        for route in routes_response.get("routes", []):
            # Elevation
            polyline = route.get("polyline", {}).get("encodedPolyline")
            elevation_results = []
            if polyline:
                elevation_resp = await map_service.get_elevation_data(polyline)
                elevation_results = elevation_resp.get("results", [])

            # AI Advisory Scoring
            ai_analysis = await optimizer_service.calculate_efficiency_score_ai(
                route, 
                elevation_data=elevation_results,
                vehicle_type=request.vehicle_type,
                current_time=amman_time
            )
            
            # 3. Environmental & Financial Impact
            dist_km = route.get("distanceMeters", 0) / 1000
            score = ai_analysis.get("score", 50)
            
            # Baseline: 230g CO2/km and ~10L/100km fuel in Amman
            # JOD Savings based on 1.10 JOD/L average fuel price
            co2_savings = round(dist_km * 230 * (score / 100) * 0.5, 2)
            money_saved_jod = round(dist_km * 0.10 * 1.10 * (score / 100) * 0.4, 3)

            optimized_routes.append({
                "distance_meters": route.get("distanceMeters"),
                "duration": route.get("duration"),
                "efficiency_score": score,
                "co2_savings_grams": co2_savings,
                "money_saved_jod": money_saved_jod,
                "optimal_speed_kmh": ai_analysis.get("optimal_speed_kmh"),
                "eco_zones": ai_analysis.get("eco_zones"),
                "master_tip": ai_analysis.get("master_tip"),
                "terrain_metrics": ai_analysis.get("terrain_metrics"),
                "labels": route.get("routeLabels", [])
            })
            
        result = {
            "origin": request.origin,
            "destination": request.destination,
            "vehicle_type": request.vehicle_type,
            "processed_at": amman_time,
            "routes": optimized_routes
        }

        cache.set(cache_key, result)
        return {**result, "cached": False}

    except Exception as e:
        return {"error": "Elite Optimization Failed", "message": str(e), "routes": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
