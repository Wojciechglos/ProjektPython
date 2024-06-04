import matplotlib.pyplot as plt
from datetime import datetime

def plot_data(data):
    timestamps = [datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S') for row in data]
    values = [row[3] for row in data]
    param_names = list(set(row[2] for row in data))

    plt.figure(figsize=(10, 5))
    for param_name in param_names:
        param_values = [row[3] for row in data if row[2] == param_name]
        param_timestamps = [datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S') for row in data if row[2] == param_name]
        plt.plot(param_timestamps, param_values, label=param_name)

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
