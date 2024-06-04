import pandas as pd
import numpy as np

def analyze_data(data):
    df = pd.DataFrame(data, columns=['id', 'city', 'parameter', 'value', 'date'])
    summary = df.groupby('parameter')['value'].describe()
    correlation = df.pivot(index='date', columns='parameter', values='value').corr()
    return summary, correlation

def calculate_trends(data):
    df = pd.DataFrame(data, columns=['id', 'city', 'parameter', 'value', 'date'])
    trends = df.groupby('parameter').apply(lambda x: np.polyfit(range(len(x)), x['value'], 1)[0])
    return trends.to_dict()
