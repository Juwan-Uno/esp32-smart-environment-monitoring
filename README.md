An ESP32-based Smart Environment Monitoring System developed using **MicroPython**.  
This project monitors environmental conditions using multiple sensors and displays real-time data on a **web-based dashboard** hosted directly by the ESP32 in **WiFi Access Point mode**.

The system works **offline** and can be accessed using a smartphone or any WiFi-enabled device without requiring an external internet connection.

## 📌 Features

- ESP32 operates as a **WiFi Access Point**
- Web-based dashboard accessible via browser
- Real-time monitoring of:
  - 🌡 Temperature (DHT11)
  - 💧 Humidity (DHT11)
  - 👤 Presence Detection (IR Sensor)
  - 🔊 Noise Detection (Sound Sensor)
  - ☔ Rain / Water Detection
- Auto-refreshing dashboard
- Non-blocking sensor reading for system stability
- Mobile-friendly UI design

---

## 🧰 Hardware Components

| Component | Description |
|--------|------------|
| ESP32 | Main microcontroller |
| DHT11 | Temperature & humidity sensor |
| IR Sensor (Flying Fish) | Motion / presence detection |
| Sound Sensor (HW-080) | Noise detection |
| Rain Sensor | Water detection |

---

## 🔌 Pin Configuration

| Sensor | ESP32 GPIO |
|------|-----------|
| DHT11 Data | GPIO 4 |
| IR Sensor | GPIO 14 |
| Sound Sensor | GPIO 27 |
| Rain Sensor | GPIO 26 |

---

## 🌐 How It Works

1. ESP32 creates its own WiFi Access Point.
2. Sensors collect environmental data.
3. ESP32 hosts a lightweight web server.
4. Sensor data is displayed on a web dashboard.
5. User connects via smartphone browser to monitor data in real time.

---

## 📲 How to Use

1. Flash **MicroPython** firmware to the ESP32.
2. Upload `main.py` to the ESP32 using Thonny.
3. Power the ESP32.
4. Connect your phone to the WiFi network:
5. Open a browser and go to:
https://192.168.4.1

---

## 📁 Project Structure

esp32-smart-environment-monitoring/
├── main.py
├── README.md
├── LICENSE
└── images/ (optional)

---

## 🚀 Applications

- Smart home monitoring
- Classroom embedded systems project
- Offline IoT systems
- Disaster and remote area monitoring
- Embedded systems learning and demonstrations

---

## 🛡 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this project with proper attribution.

---

## 👤 Author

**Juwan Ronquillo**  
Computer Engineering Student  
ESP32 • Embedded Systems • MicroPython • IoT

---

## ⭐ Acknowledgments

This project was developed for educational and embedded systems learning purposes.