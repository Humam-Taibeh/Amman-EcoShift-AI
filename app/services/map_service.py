import os
import httpx
from typing import Dict, Any, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MapService:
    """
    Robust Service to interact with Google Maps Routes API (v2).
    """
    
    def __init__(self):
        self.api_key = os.getenv("Maps_API_KEY")
        self.base_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.elevation_url = "https://maps.googleapis.com/maps/api/elevation/json"
        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.routeLabels,routes.polyline"
        }

    async def get_elevation_data(self, points: str) -> Dict[str, Any]:
        """
        Fetches elevation for a path/polyline.
        """
        params = {
            "path": f"enc:{points}",
            "samples": 10,  # Sample 10 points along the route
            "key": self.api_key
        }
        async with httpx.AsyncClient() as client:
            # Note: Elevation API uses standard 'key' param, not headers for some versions
            response = await client.get(self.elevation_url, params=params)
            return response.json()

    async def get_fuel_efficient_route(
        self, 
        origin_lat: float, origin_lng: float, 
        dest_lat: float, dest_lng: float,
        vehicle_type: str = "GASOLINE"
    ) -> Dict[str, Any]:
        """
        Fetches routes from Google Maps with error handling.
        """
        payload = {
            "origin": {
                "location": {"latLng": {"latitude": origin_lat, "longitude": origin_lng}}
            },
            "destination": {
                "location": {"latLng": {"latitude": dest_lat, "longitude": dest_lng}}
            },
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
            "computeAlternativeRoutes": True
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(self.base_url, json=payload, headers=self.headers)
                
                if response.status_code != 200:
                    logger.error(f"Google API Error: {response.status_code} - {response.text}")
                    return {"error": f"Google Maps API failed with status {response.status_code}"}
                
                return response.json()
        
        except httpx.ConnectError:
            logger.error("Connection Error: Could not connect to Google Maps API.")
            return {"error": "Connection Error: Check your internet connection."}
        except httpx.TimeoutException:
            logger.error("Timeout Error: Google Maps API took too long to respond.")
            return {"error": "Request timed out."}
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return {"error": "An unexpected error occurred in MapService."}

# Singleton instance
map_service = MapService()
