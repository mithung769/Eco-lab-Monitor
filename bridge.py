import json
import time
import requests
import serial
from serial.tools import list_ports

API_BASE = "http://127.0.0.1:8000"
DATA_URL = f"{API_BASE}/data"
BAUD = 9600

def find_port():
    ports = list(list_ports.comports())
    for p in ports:
        if "usb" in (p.description or "").lower():
            return p.device
    return ports[0].device if ports else None

def send_relay(ser, state):
    cmd = "RELAY_ON\n" if state else "RELAY_OFF\n"
    ser.write(cmd.encode())

def main():
    port = find_port()
    if not port:
        print("Arduino NOT connected")
        return

    print("Using:", port)

    ser = serial.Serial(port, BAUD, timeout=2)
    time.sleep(2)

    last_relay = None

    while True:
        try:
            line = ser.readline().decode().strip()
            if not line:
                continue

            data = json.loads(line)
            requests.post(DATA_URL, json=data)

            # Relay sync
            r = requests.get(f"{API_BASE}/relay_state")
            desired = r.json()["relay"]

            if desired != last_relay:
                send_relay(ser, desired)
                last_relay = desired
                print("Relay:", "ON" if desired else "OFF")

        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()