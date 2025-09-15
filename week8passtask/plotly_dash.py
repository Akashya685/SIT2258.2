import os, time, threading
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Output, Input, State

from arduino_iot_cloud import ArduinoCloudClient
from my_secrets import DEVICE_ID, SECRET_KEY

N = 100
SAVE_DIR = "week8_data"
os.makedirs(SAVE_DIR, exist_ok=True)

latest = {"x": None, "y": None, "z": None}
T, X, Y, Z = [], [], [], []

def now_iso(): return datetime.now(timezone.utc).isoformat()

def on_py_x(c, v): latest["x"] = float(v)
def on_py_y(c, v): latest["y"] = float(v)
def on_py_z(c, v): latest["z"] = float(v)

def cloud_loop():
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY, sync_mode=True)
    client.register("py_x", value=None, on_write=on_py_x)
    client.register("py_y", value=None, on_write=on_py_y)
    client.register("py_z", value=None, on_write=on_py_z)
    client.start()
    while True:
        client.update()
        time.sleep(0.05)

threading.Thread(target=cloud_loop, daemon=True).start()

app = Dash(__name__)
app.layout = html.Div([
    html.H3("Smartphone Accelerometer - X/Y/ and Z )"),
    dcc.Graph(id="accel-graph"),
    html.Div(id="status"),
    dcc.Store(id="cursor", data={"idx": 0, "saved": 0}),
    dcc.Interval(id="tick", interval=1000, n_intervals=0)
])

@app.callback(
    Output("accel-graph", "figure"),
    Output("cursor", "data"),
    Output("status", "children"),
    Input("tick", "n_intervals"),
    State("cursor", "data"),
    prevent_initial_call=False
)
def refresh(_n, cur):
    idx, saved = cur["idx"], cur["saved"]
    if None not in latest.values():
        T.append(now_iso()); X.append(latest["x"]); Y.append(latest["y"]); Z.append(latest["z"])
    total = len(T)
    available = total - idx
    if available >= N:
        df = pd.DataFrame({"timestamp": T[idx:idx+N], "x": X[idx:idx+N], "y": Y[idx:idx+N], "z": Z[idx:idx+N]})
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(SAVE_DIR, f"100Sample{ts}.csv")
        df.to_csv(csv_path, index=False)
        saved += 1
        idx += N
    df_live = pd.DataFrame({"t": T[-N:], "x": X[-N:], "y": Y[-N:], "z": Z[-N:]})
    fig = px.line(df_live, x="t", y=["x", "y", "z"], title="Accelerometer - last N samples")
    status = f"Total samples is {total} | Saved  {saved}"
    return fig, {"idx": idx, "saved": saved}, status

if __name__ == "__main__":
    app.run(debug=False)
