
import time, logging
from datetime import datetime, timezone
from arduino_iot_cloud import ArduinoCloudClient
from secrets import DEVICE_ID, SECRET_KEY

logging.basicConfig(level=logging.INFO) 

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def append_line(path, line):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def on_py_x(client, value):
    append_line("py_x.csv", f"{now_iso()},{value}")

def on_py_y(client, value):
    append_line("py_y.csv", f"{now_iso()},{value}")

def on_py_z(client, value):
    append_line("py_z.csv", f"{now_iso()},{value}")

client = ArduinoCloudClient(
    device_id=DEVICE_ID,
    username=DEVICE_ID,
    password=SECRET_KEY,
    sync_mode=True
)

client.register("py_x", value=None, on_write=on_py_x)
client.register("py_y", value=None, on_write=on_py_y)
client.register("py_z", value=None, on_write=on_py_z)

print("Connecting...")
client.start()
print("Connected. Logging to py_x.csv, py_y.csv, py_z.csv, Ctrl+C to stop.")

try:
    while True:
        client.update() 
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped.")
