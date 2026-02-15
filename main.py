import network
import socket
import time
from machine import Pin
import dht

# ------------------------
# ACCESS POINT SETUP
# ------------------------
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32_ENV_MONITOR', password='12345678')
time.sleep(2)
ip = ap.ifconfig()[0]
print("Access Point Created")
print("SSID: ESP32_ENV_MONITOR  Password: 12345678")
print("Open: http://{}".format(ip))

# ------------------------
# SENSOR SETUP
# ------------------------
dht_sensor = dht.DHT11(Pin(4))   # DHT11 on GPIO4
ir_sensor = Pin(14, Pin.IN)      # IR sensor on GPIO14
sound_sensor = Pin(27, Pin.IN)   # Sound sensor on GPIO27
rain_sensor = Pin(26, Pin.IN)    # Rain sensor on GPIO26

# ------------------------
# SOCKET SERVER
# ------------------------
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(4)
s.settimeout(1)  # don’t block forever
print("Web server running on http://{}".format(ip))

# ------------------------
# HTML DASHBOARD FUNCTION
# ------------------------
def page_html(t,h,ir,sound,rain):
    return """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>ESP32 Environment Monitor</title>
  <meta http-equiv="refresh" content="3">
  <style>
    body {{ font-family: Arial, sans-serif; margin:0; background:#f4f6f9; }}
    header {{ background:#2c3e50; color:white; padding:15px; text-align:center; }}
    h1 {{ margin:0; font-size:22px; }}
    .container {{ display:flex; flex-wrap:wrap; justify-content:center; margin:20px; }}
    .card {{ background:white; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.15);
            width:220px; margin:10px; padding:20px; text-align:center; }}
    .value {{ font-size:24px; margin:10px 0; }}
    .alert {{ color:#e74c3c; font-weight:bold; }}
    .normal {{ color:#27ae60; font-weight:bold; }}
  </style>
</head>
<body>
  <header>
    <h1>🌍 Smart Environment Dashboard</h1>
  </header>
  <div class="container">
    <div class="card">
      <h2>🌡 Temperature</h2>
      <div class="value">{}</div>
    </div>
    <div class="card">
      <h2>💧 Humidity</h2>
      <div class="value">{}</div>
    </div>
    <div class="card">
      <h2>👤 Presence (IR)</h2>
      <div class="value {}">{}</div>
    </div>
    <div class="card">
      <h2>🔊 Noise</h2>
      <div class="value {}">{}</div>
    </div>
    <div class="card">
      <h2>☔ Rain</h2>
      <div class="value {}">{}</div>
    </div>
  </div>
</body>
</html>""".format(
        t,
        h,
        "alert" if not ir else "normal", "Yes" if not ir else "No",
        "alert" if sound else "normal", "Yes" if sound else "No",
        "alert" if not rain else "normal", "Yes" if not rain else "No"
    )

# ------------------------
# MAIN LOOP
# ------------------------
temperature, humidity = "Error", "Error"
last_dht = 0

while True:
    # Read DHT11 every 2s
    if time.ticks_diff(time.ticks_ms(), last_dht) > 2000:
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
        except Exception as e:
            print("DHT error:", e)
            temperature, humidity = "Error", "Error"
        last_dht = time.ticks_ms()

    # Read other sensors
    try:
        ir_status = ir_sensor.value()
        sound_status = sound_sensor.value()
        rain_status = rain_sensor.value()
    except Exception as e:
        print("Other sensor error:", e)
        ir_status, sound_status, rain_status = 0, 0, 1

    # Serve client
    conn = None
    try:
        conn, addr = s.accept()
        print("Client:", addr)
        _ = conn.recv(512)  # read request
        html = page_html(temperature, humidity, ir_status, sound_status, rain_status)
        resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(len(html), html)
        conn.sendall(resp.encode())
    except OSError:
        pass  # timeout, no client
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass