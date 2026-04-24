import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

try:
    from app.main import app
    print("app.main imported successfully")
except Exception as e:
    print(f"Error importing app.main: {e}")
    import traceback
    traceback.print_exc()

try:
    from app.services.map_service import map_service
    print("map_service imported successfully")
except Exception as e:
    print(f"Error importing map_service: {e}")
    import traceback
    traceback.print_exc()

try:
    from app.services.optimizer import optimizer_service
    print("optimizer_service imported successfully")
except Exception as e:
    print(f"Error importing optimizer_service: {e}")
    import traceback
    traceback.print_exc()
