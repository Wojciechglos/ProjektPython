import requests

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"

def api_stations():
    url = f"{BASE_URL}/station/findAll"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def api_sensors(station_id):
    url = f"{BASE_URL}/station/sensors/{station_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def api_sensor_data(sensor_id):
    url = f"{BASE_URL}/data/getData/{sensor_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def api_index_powietrza(sensor_id):
    url = f"{BASE_URL}/aqindex/getIndex/{sensor_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
