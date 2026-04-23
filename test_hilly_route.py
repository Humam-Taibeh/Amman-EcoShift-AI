import requests
import json
import time

def run_terrain_test(vehicle_type: str):
    url = "http://127.0.0.1:8000/optimize"
    payload = {
        "origin": {"lat": 31.9515, "lng": 35.9394},      # Downtown (Valley)
        "destination": {"lat": 31.9527, "lng": 35.8548}, # 7th Circle (High)
        "vehicle_type": vehicle_type
    }

    print(f"\n--- [UNTOUCHABLE V4] Testing: Downtown -> 7th Circle ({vehicle_type}) ---")
    
    start_time = time.time()
    try:
        response = requests.post(url, json=payload)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            route = data.get("routes", [{}])[0]
            
            print(f"Time: {elapsed:.2f}s | Cached: {data.get('cached')}")
            print(f"Efficiency Score: {route.get('efficiency_score')}/100")
            print(f"Money Saved: {route.get('money_saved_jod')} JOD")
            print(f"Optimal Speed: {route.get('optimal_speed_kmh')} km/h")
            print(f"Master Tip: {route.get('master_tip')}")
            
            print("\nEco-Zones Analysis:")
            for zone in route.get("eco_zones", []):
                print(f"  [{zone.get('zone')}]: {zone.get('advice')}")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

def main():
    print("Eco-Shift AI: Untouchable V4 Final Test")
    run_terrain_test("GASOLINE")
    run_terrain_test("ELECTRIC")

if __name__ == "__main__":
    main()
