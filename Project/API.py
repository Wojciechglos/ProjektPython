import requests

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"

def api_stations():
    url = f"{BASE_URL}/station/findAll"
    return _make_request(url)

def api_sensors(station_id):
    url = f"{BASE_URL}/station/sensors/{station_id}"
    return _make_request(url)

def api_sensor_data(sensor_id):
    url = f"{BASE_URL}/data/getData/{sensor_id}"
    return _make_request(url)

def api_index_powietrza(sensor_id):
    url = f"{BASE_URL}/aqindex/getIndex/{sensor_id}"
    return _make_request(url)

def _make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Nie udało się wykonać zapytania: {e}")
        return None
