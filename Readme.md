# Eco-lab-Monitor

## 📝 Overview
**Eco-Monitor Lab Energy & Environment Auditor** is an IoT-based system that monitors lab conditions and energy usage in real time using sensors and Arduino. Data is processed with Python and displayed on a dashboard, with relay-based device control to improve efficiency and reduce power wastage.

---

## 📂 Project Structure
- **DHT11.ino** (Arduino sketch logic)
- **Components Architecture.pdf** (Visual circuit diagram)
- **Description.pdf** (Arduino sketch logic)
- **main.py** (Backend processing & serial read)
- **bridge.py** (Communication layer)
- **tkinter.py** (Frontend UI Dashboard)
- **.idea/** (IDE configuration (hidden))
- **.venv/** (Python virtual environment)
- **__pycache__/** (Python cache files)
---

## 🛠️ Requirements

### 🔌 Hardware Components
* **Arduino Uno**
* **DHT11 Sensor** (Temperature & Humidity)
* **LDR Sensor** (Light Intensity)
* **Relay Module** (For device control)
* **Breadboard & Jumper Wires**
* **USB Cable**

### 💻 Software & Libraries
* **Arduino IDE** (To upload the hardware code)
* **Python 3.x**
* **Dependencies:**
  `pip install pyserial fastapi uvicorn`

---

## 🚀 Setup & Execution Guide

### Step 1: Hardware Setup
1. Open `architecture.pdf` for the wiring diagram.
2. Connect components to the Arduino:
   - **DHT11** ➡️ Pin **D2**
   - **LDR** ➡️ Pin **A1**
   - **Relay** ➡️ Pin **D8**
   - **VCC** ➡️ **5V** | **GND** ➡️ **GND**
3. Plug the Arduino into your PC via USB.

### Step 2: Upload Arduino Code
1. Open the Arduino IDE.
2. Copy/Paste the contents of `arduino_code.txt`.
3. Select **Arduino Uno** and your active **COM Port**.
4. Click **Upload**.

### Step 3: Run the System
⚠️ **IMPORTANT:** Start the scripts in this exact order:
1. **Backend:** `python main.py`
2. **Bridge:** `python bridge.py`
3. **Frontend:** `python tkinter.py`

---

## 🔄 System Workflow
1. **Data Collection:** Sensors gather environmental metrics.
2. **Transmission:** Arduino sends data via USB Serial.
3. **Processing:** `main.py` parses the incoming stream.
4. **Bridging:** `bridge.py` transfers data to the UI layer.
5. **Visualization:** `tkinter.py` displays live results.
6. **Actuation:** User controls the relay directly via the Dashboard.

---

## ✨ Key Features
* ✅ **Real-time Monitoring:** Live tracking of lab metrics.
* ✅ **Energy Auditing:** Estimates energy usage and costs.
* ✅ **Carbon Footprint:** Automatic calculation of CO2 impact.
* ✅ **Relay Control:** Toggle hardware devices from the UI.
* ✅ **Dashboard:** Clean, interactive visualization.

---

## ⚠️ Important Notes
* **COM Port:** Double-check your port in `main.py`.
* **Connection:** Keep the USB cable connected during operation.
* **Initialization:** Always run the backend before the frontend.
* **Troubleshooting:** If the dashboard is blank, check your physical wiring.