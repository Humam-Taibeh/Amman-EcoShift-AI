import requests
import time

def run_test(run_number: int):
    url = "http://127.0.0.1:8000/optimize"
    payload = {
        "origin": {"lat": 31.9527, "lng": 35.8548},      # 7th Circle
        "destination": {"lat": 32.0157, "lng": 35.8672}, # UJ
        "vehicle_type": "ELECTRIC"
    }

    start_time = time.time()
    try:
        response = requests.post(url, json=payload)
        end_time = time.time()
        elapsed = end_time - start_time

        if response.status_code == 200:
            data = response.json()
            cached = data.get("cached", False)
            processed_at = data.get("processed_at")
            route = data.get("routes", [{}])[0]

            print(f"--- Run #{run_number} ---")
            print(f"Time Taken: {elapsed:.4f} seconds")
            print(f"Cached Result: {cached}")
            print(f"Processed At (Amman Time): {processed_at}")
            print(f"Vehicle Type: {data.get('vehicle_type')}")
            print(f"Efficiency Score: {route.get('efficiency_score')}/100")
            print(f"Master Tip: {route.get('master_tip')}")
            print("-" * 50)
            return elapsed
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")
    return 0

def main():
    print("Eco-Shift AI: Final Production Test\n")
    
    # Run 1: Initial Request (API + AI Analysis)
    run_test(1)
    
    # Short pause
    time.sleep(1)
    
    # Run 2: Cached Request
    run_test(2)

if __name__ == "__main__":
    main()
