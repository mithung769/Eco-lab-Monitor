from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# ---------------- DATABASE ----------------
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL,
    light REAL,
    power REAL,
    energy REAL
)
""")
conn.commit()

# ---------------- GLOBALS ----------------
relay_state = False
total_energy = 0.0
last_time = datetime.now()

VOLTAGE = 230
CURRENT = 0.2
RATE = 8
CARBON_FACTOR = 0.82

# ---------------- MODELS ----------------
class SensorData(BaseModel):
    temperature: float
    humidity: float
    light: float

class RelayRequest(BaseModel):
    state: str

# ---------------- ENERGY FIXED ----------------
def process_data(data: SensorData):
    global total_energy, last_time

    now = datetime.now()
    elapsed_seconds = (now - last_time).total_seconds()
    last_time = now

    power = VOLTAGE * CURRENT if relay_state else 0.0

    # ✅ CORRECT ENERGY CALCULATION
    delta_energy = (power * elapsed_seconds) / 3600000.0
    total_energy += delta_energy

    cursor.execute("""
    INSERT INTO readings (timestamp, temperature, humidity, light, power, energy)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        now.strftime("%H:%M:%S"),
        data.temperature,
        data.humidity,
        data.light,
        power,
        total_energy
    ))
    conn.commit()

@app.post("/data")
def receive_data(data: SensorData):
    process_data(data)
    return {"message": "Data stored"}

# ---------------- RELAY ----------------
@app.post("/relay")
def control_relay(req: RelayRequest):
    global relay_state
    relay_state = True if req.state.lower() == "on" else False
    return {"relay": relay_state}

@app.get("/relay_state")
def get_relay():
    return {"relay": relay_state}

# ---------------- STATUS ----------------
@app.get("/status")
def get_status():
    cursor.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()

    if row:
        return {
            "temperature": row[2],
            "humidity": row[3],
            "light": row[4],
            "power": row[5],
            "energy": row[6],
            "relay": relay_state
        }
    return {"message": "No data"}

# ---------------- HISTORY ----------------
@app.get("/history")
def get_history():
    cursor.execute("SELECT timestamp, power FROM readings")
    rows = cursor.fetchall()
    return [{"time": r[0], "power": r[1]} for r in rows]

# ---------------- SUMMARY ----------------
@app.get("/summary")
def get_summary():
    return {
        "energy_kwh": total_energy,
        "cost": total_energy * RATE,
        "carbon": total_energy * CARBON_FACTOR
    }

@app.get("/")
def home():
    return {"message": "Server running"}