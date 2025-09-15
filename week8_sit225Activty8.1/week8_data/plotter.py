import pandas as pd
import matplotlib.pyplot as plt

x = pd.read_csv("accelerometer_x.csv")
y = pd.read_csv("accelerometer_y.csv")
z = pd.read_csv("accelerometer_z.csv")

x['time'] = pd.to_datetime(x['time'])
y['time'] = pd.to_datetime(y['time'])
z['time'] = pd.to_datetime(z['time'])

plt.plot(x['time'], x['value'])
plt.title("Accelerometer X")
plt.xlabel("Time")
plt.ylabel("Value")
plt.xticks(pd.date_range(start=x['time'].min(), end=x['time'].max(), freq="5min"), rotation=45)
plt.show()

plt.plot(y['time'], y['value'])
plt.title("Accelerometer Y")
plt.xlabel("Time")
plt.ylabel("Value")
plt.xticks(pd.date_range(start=y['time'].min(), end=y['time'].max(), freq="5min"), rotation=45)
plt.show()

plt.plot(z['time'], z['value'])
plt.title("Accelerometer Z")
plt.xlabel("Time")
plt.ylabel("Value")
plt.xticks(pd.date_range(start=z['time'].min(), end=z['time'].max(), freq="5min"), rotation=45)
plt.show()

plt.plot(x['time'], x['value'], label='X')
plt.plot(y['time'], y['value'], label='Y')
plt.plot(z['time'], z['value'], label='Z')
plt.legend()
plt.title("Accelerometer X, Y, Z")
plt.xlabel("Time")
plt.ylabel("Value")
plt.xticks(pd.date_range(start=x['time'].min(), end=x['time'].max(), freq="5min"), rotation=45)
plt.show()
