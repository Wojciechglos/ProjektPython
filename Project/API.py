import requests

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"

def api_stations():
    """
        Pobiera listę wszystkich stacji pomiarowych z API GIOŚ.

        Zwraca:
        - list
            Lista stacji pomiarowych w formie słowników.

        W przypadku błędu podczas wykonywania zapytania, zwraca None.
        """
    url = f"{BASE_URL}/station/findAll"
    return _make_request(url)

def api_sensors(station_id):
    """
    Pobiera listę sensorów dla danej stacji pomiarowej z API GIOŚ.

    Argumenty:
    - station_id : int
        Identyfikator stacji pomiarowej.

    Zwraca:
    - list
        Lista sensorów w formie słowników dla danej stacji pomiarowej.

    W przypadku błędu podczas wykonywania zapytania, zwraca None.
    """
    url = f"{BASE_URL}/station/sensors/{station_id}"
    return _make_request(url)

def api_sensor_data(sensor_id):
    """
        Pobiera dane pomiarowe dla danego sensora z API GIOŚ.

        Argumenty:
        - sensor_id : int
            Identyfikator sensora.

        Zwraca:
        - dict
            Dane pomiarowe w formie słownika dla danego sensora.

        W przypadku błędu podczas wykonywania zapytania, zwraca None.
        """
    url = f"{BASE_URL}/data/getData/{sensor_id}"
    return _make_request(url)

def api_index_powietrza(sensor_id):
    """
        Pobiera indeks jakości powietrza dla danej stacji pomiarowej z API GIOŚ.

        Argumenty:
        - sensor_id : int
            Identyfikator sensora.

        Zwraca:
        - dict
            Indeks jakości powietrza w formie słownika dla danej stacji pomiarowej.

        W przypadku błędu podczas wykonywania zapytania, zwraca None.
        """
    url = f"{BASE_URL}/aqindex/getIndex/{sensor_id}"
    return _make_request(url)

def _make_request(url):
    """
       Wykonuje zapytanie HTTP GET do podanego URL i zwraca odpowiedź w formie JSON.

       Argumenty:
       - url : str
           URL do którego ma zostać wykonane zapytanie.

       Zwraca:
       - dict or list
           Odpowiedź w formie JSON w zależności od struktury danych zwróconych przez API.

       W przypadku błędu podczas wykonywania zapytania, zwraca None.
       """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Nie udało się wykonać zapytania: {e}")
        return None
