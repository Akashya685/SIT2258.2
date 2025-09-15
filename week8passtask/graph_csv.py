import pandas as pd
import plotly.express as px
import glob
import os
DATA_DIR = "week8_data"
files = sorted(glob.glob(os.path.join(DATA_DIR, "100Sample*.csv")))

if not files:
    print("No CSV files found in week8_data/")
else:
    print("Found CSVs", files)
    for f in files:
        df = pd.read_csv(f)
        print(f"Plotting {f} with {len(df)} samples")

        fig = px.line(df, x="timestamp", y=["x", "y", "z"],
                      title=f"Accelerometer data from {os.path.basename(f)}")
        out_png = f.replace(".csv", ".png")
        fig.write_image(out_png)
        print(f"Saved {out_png}")

        fig.show()
