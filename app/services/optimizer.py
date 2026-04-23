import os
import google.generativeai as genai
from typing import Dict, Any, List
import json

class RouteOptimizer:
    """
    Elite AI Advisory Optimizer.
    Provides Eco-Zones, Optimal Speeds, and Topography-aware advice for Amman.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def _analyze_terrain(self, elevation_results: List[Dict]) -> Dict[str, float]:
        """
        Calculates total ascent, descent, and elevation range.
        """
        if not elevation_results:
            return {"ascent": 0, "descent": 0, "elevation_range": 0}
        
        ascent = 0
        descent = 0
        elevations = [r.get("elevation", 0) for r in elevation_results]
        
        for i in range(len(elevations) - 1):
            diff = elevations[i+1] - elevations[i]
            if diff > 0:
                ascent += diff
            else:
                descent += abs(diff)
        
        return {
            "ascent": round(ascent, 2),
            "descent": round(descent, 2),
            "elevation_range": round(max(elevations) - min(elevations), 2)
        }

    async def calculate_efficiency_score_ai(
        self, 
        route_data: Dict[str, Any], 
        elevation_data: List[Dict],
        vehicle_type: str = "GASOLINE",
        current_time: str = "Unknown"
    ) -> Dict[str, Any]:
        """
        Elite analysis with segment-specific Eco-Advisory.
        """
        distance_meters = float(route_data.get("distanceMeters", 1))
        duration_seconds = float(route_data.get("duration", "0s").replace("s", ""))
        avg_speed_kmh = (distance_meters / 1000) / (duration_seconds / 3600) if duration_seconds > 0 else 0
        
        terrain = self._analyze_terrain(elevation_data)

        prompt = f"""
        Act as an Elite Eco-Driving Consultant for Amman, Jordan.
        
        CONTEXT:
        - Vehicle: {vehicle_type}
        - Time: {current_time}
        - Terrain Profile: {terrain['ascent']}m ascent, {terrain['descent']}m descent.
        
        ROUTE METRICS:
        - Distance: {distance_meters}m
        - Current Avg Speed: {avg_speed_kmh:.2f}km/h
        
        TASK:
        1. Calculate an efficiency score (0-100).
        2. Identify 'Eco-Zones' along the route (e.g., 'Steep Ascent', 'Traffic Bottleneck', 'Regen Descent').
        3. Suggest an 'Optimal Speed' (km/h) to maximize {vehicle_type} efficiency for this specific terrain.
        4. Provide a 'Master Tip' for the driver.

        RETURN JSON ONLY:
        - "score": number
        - "optimal_speed_kmh": number
        - "eco_zones": [ {{"zone": "string", "advice": "string"}} ]
        - "master_tip": "string"
        - "idling_risk": "Low/Medium/High"
        
        Output valid JSON only.
        """

        try:
            response = await self.model.generate_content_async(prompt)
            result_text = response.text.strip()
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            
            res = json.loads(result_text)
            res["terrain_metrics"] = terrain
            return res
        except Exception as e:
            # Enhanced Fallback with placeholders
            return {
                "score": 75,
                "optimal_speed_kmh": 40,
                "eco_zones": [{"zone": "General", "advice": "Maintain steady throttle on inclines."}],
                "master_tip": f"AI Advisor temporarily unavailable. (Error: {str(e)})",
                "idling_risk": "Medium",
                "terrain_metrics": terrain
            }

optimizer_service = RouteOptimizer()
