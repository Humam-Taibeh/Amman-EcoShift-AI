from __future__ import annotations
import time
from datetime import datetime
import hashlib
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        self.cache: dict[str, dict[str, Any]] = {}
        self.ttl = ttl

    def get(self, key: str):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['data']
            else:
                del self.cache[key]
        return None

    def set(self, key: str, data: dict[str, Any]):
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
            logger.warning(f"Map service returned error: {routes_response['error']}")
            raise HTTPException(status_code=400, detail=routes_response["error"])
        
        # 2. Process Routes
        optimized_routes = []
        routes = routes_response.get("routes", [])
        
        if not routes:
            logger.info("No routes found for the given locations.")
            return {
                "origin": request.origin,
                "destination": request.destination,
                "vehicle_type": request.vehicle_type,
                "processed_at": amman_time,
                "routes": [],
                "message": "No routes available."
            }

        for route in routes:
            # Elevation
            polyline = route.get("polyline", {}).get("encodedPolyline")
            elevation_results = []
            if polyline:
                try:
                    elevation_resp = await map_service.get_elevation_data(polyline)
                    elevation_results = elevation_resp.get("results", [])
                except Exception as elev_e:
                    logger.error(f"Failed to fetch elevation: {elev_e}")

            # AI Advisory Scoring
            try:
                ai_analysis = await optimizer_service.calculate_efficiency_score_ai(
                    route, 
                    elevation_data=elevation_results,
                    vehicle_type=request.vehicle_type,
                    current_time=amman_time
                )
            except Exception as ai_e:
                logger.error(f"AI Optimization failed: {ai_e}")
                # Fallback to basic analysis if AI fails
                ai_analysis = {
                    "score": 70,
                    "optimal_speed_kmh": 45,
                    "eco_zones": [],
                    "master_tip": "Drive smoothly and avoid rapid acceleration.",
                    "terrain_metrics": {"ascent": 0, "descent": 0, "elevation_range": 0}
                }
            
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
                "elevation_profile": [r.get("elevation") for r in elevation_results],
                "polyline": polyline,
                "labels": route.get("routeLabels", [])
            })
            
        # --- Route Categorization (3-Route Battle) ---
        if len(optimized_routes) >= 1:
            # Sort by duration for FAST
            optimized_routes.sort(key=lambda x: int(x["duration"].replace("s", "")))
            optimized_routes[0]["type"] = "FAST-PATH"
            
            # Sort by efficiency for ECO
            optimized_routes.sort(key=lambda x: x["efficiency_score"], reverse=True)
            optimized_routes[0]["type"] = "ECO-PATH"
            
            # If we have a 3rd route, label it BALANCED, otherwise label ECO/FAST
            if len(optimized_routes) >= 3:
                # Find one that isn't ECO or FAST
                for r in optimized_routes:
                    if "type" not in r:
                        r["type"] = "BALANCED"
                        break
            elif len(optimized_routes) == 2:
                # If only 2, and both are labeled (one as FAST, one as ECO), that's fine.
                # If they are the same route, ECO wins label.
                pass

        result = {
            "origin": request.origin,
            "destination": request.destination,
            "vehicle_type": request.vehicle_type,
            "processed_at": amman_time,
            "routes": optimized_routes
        }

        cache.set(cache_key, result)
        return {**result, "cached": False}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Critical failure in Elite Optimization")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
