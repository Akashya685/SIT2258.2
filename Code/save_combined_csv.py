import time, logging
from datetime import datetime, timezone
from arduino_iot_cloud import ArduinoCloudClient
from secrets import DEVICE_ID, SECRET_KEY

logging.basicConfig(level=logging.INFO)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

class Combiner:
    def __init__(self, out_path="accel_xyz.csv"):
        self.out_path = out_path
        self.buf = {"py_x": None, "py_y": None, "py_z": None}

    def ready(self):
        return all(v is not None for v in self.buf.values())

    def write(self):
        line = f'{now_iso()},{self.buf["py_x"]},{self.buf["py_y"]},{self.buf["py_z"]}'
        with open(self.out_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def update(self, key, value):
        self.buf[key] = value
        if self.ready():
            self.write()

comb = Combiner()
def on_py_x(c, v): comb.update("py_x", v)
def on_py_y(c, v): comb.update("py_y", v)
def on_py_z(c, v): comb.update("py_z", v)

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
print("Connected. Logging to accel_xyz.csv, Ctrl+C to stop.")

try:
    while True:
        client.update()  
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped.")
