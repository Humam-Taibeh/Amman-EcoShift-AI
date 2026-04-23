# 🌍 Amman Eco-Shift AI
### *Elite Terrain-Aware & AI-Driven Routing Engine*

**Amman Eco-Shift AI** is a sophisticated backend routing engine designed to optimize fuel efficiency and urban mobility in the unique topography of Amman, Jordan. Built for the Google Antigravity Challenge, it combines real-time traffic data, altitude profiles (The 7 Hills), and Google Gemini AI to recommend the most sustainable routes.

---

## 🚀 Key Features

- **🚠 Terrain-Aware (Elite Level)**: Integrates the **Google Elevation API** to calculate total ascent and descent.
- **🤖 Elite AI Advisory**: Gemini 1.5/2.0 suggests **Optimal Speeds** and identifies **Eco-Zones** (Steep climbs, Bottlenecks) with segment-specific advice.
- **💰 Financial Optimization**: Calculates estimated **Money Saved (in JOD)** based on current fuel prices in Jordan.
- **⚡ Vehicle Profiling**: Tailored routing logic for **Gasoline**, **Hybrid**, and **Electric** vehicles.
- **🧠 Contextual Insights**: Analyzes routes against Amman's "Rush Hour" patterns.
- **💨 Low Latency**: Features a built-in **In-Memory Caching Layer** for lightning-fast repeated requests.
- **🛡️ Production Ready**: Robust error handling with graceful regional fallbacks.

---

## 🏗️ System Architecture

1. **FastAPI**: High-performance Python web framework.
2. **Google Maps Routes API (v2)**: Real-time traffic-aware route computation.
3. **Google Elevation API**: Samples altitude data along the route path.
4. **Google Gemini (flash-latest)**: Large Language Model for deep contextual analysis and scoring.

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd "GDG Project"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   Maps_API_KEY=YOUR_GOOGLE_MAPS_KEY
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   ```

4. **Start the Backend**:
   ```bash
   python -m app.main
   ```

5. **Start the Frontend Dashboard**:
   Open a new terminal and run:
   ```bash
   streamlit run app/frontend.py
   ```

---

## 📡 API Endpoints

### `POST /optimize`
**Payload:**
```json
{
  "origin": {"lat": 31.9515, "lng": 35.9394},
  "destination": {"lat": 31.9527, "lng": 35.8548},
  "vehicle_type": "ELECTRIC"
}
```

**Response Highlights:**
- `efficiency_score`: 0-100 score.
- `co2_savings_grams`: Estimated carbon offset.
- `terrain_metrics`: Ascent/Descent data.
- `ai_insight`: Professional analysis from Gemini.

---

## 🧪 Running Tests

We have included specialized test scripts for Amman:
- `test_amman_route.py`: General routing and cache test.
- `test_hilly_route.py`: Terrain comparison between Gasoline and Electric.

```bash
python test_hilly_route.py
```

---

*Developed for the Google Antigravity Challenge - Amman, Jordan.*
