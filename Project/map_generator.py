import tkinter as tk
from tkinter import messagebox
import requests
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import tempfile

def generate_map_and_return_html(address, radius_km):
    """
     Generuje mapę z lokalizacjami stacji pomiarowych w określonym promieniu od podanego adresu i zwraca ją jako kod HTML.

     Argumenty:
     - address : str
         Adres centralny, od którego mierzymy odległości.
     - radius_km : float
         Promień w kilometrach, w którym wyszukujemy stacje pomiarowe.

     Zwraca:
     - str
         Kod HTML zawierający mapę, jeśli wszystko przebiegnie pomyślnie.
     - None
         W przypadku wystąpienia błędu związanego z przetwarzaniem adresu lub promienia.

     W przypadku błędnego formatu adresu lub promienia, wyświetla komunikat o błędzie w oknie dialogowym.

     """
    try:

        # Używamy geocoder Nominatim do znalezienia współrzędnych (geokodowania) dla podanego adresu.
        geolocator = Nominatim(user_agent="my_application")
        location = geolocator.geocode(address)

        # Jeśli nie udało się znaleźć lokalizacji, podnosimy błąd.
        if not location:
            raise AttributeError("Geocoding failed")

        # Współrzędne centralnej lokalizacji (adresu).
        central_location = (location.latitude, location.longitude)

        # URL API do pobrania danych o stacjach pomiarowych
        api_url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"

        # Pobieramy dane o stacjach pomiarowych
        response = requests.get(api_url)
        stations = response.json()

        # Tworzymy obiekt mapy folium centrowany na podanej lokalizacji, z zoomem 10.
        map = folium.Map(location=central_location, zoom_start=10)

        # Iterujemy przez listę stacji pomiarowych
        for station in stations:
            station_name = station['stationName']
            lat = float(station['gegrLat'])
            lon = float(station['gegrLon'])
            id_stacji = station['id']
            city_name = station['city']['name']
            commune_name = station['city']['commune']['communeName']
            district_name = station['city']['commune']['districtName']
            province_name = station['city']['commune']['provinceName']

            station_location = (lat, lon)
            distance = geodesic(central_location, station_location).kilometers

            # Dodajemy marker tylko dla stacji znajdujących się w określonym promieniu od centralnej lokalizacji.
            if distance <= float(radius_km):
                popup_text = f"id Stacji:{id_stacji}<br>Miasto:{city_name}<br>Gmina:{commune_name}<br>Powiat:{district_name}<br>Woj:{province_name}<br>Odległość: {distance:.2f} km"
                folium.Marker(
                    [lat, lon],
                    popup=popup_text
                ).add_to(map)

        # Dodajemy marker dla centralnej lokalizacji z czerwoną ikoną.
        folium.Marker(
            central_location,
            popup="Lokalizacja centralna",
            icon=folium.Icon(color="red")
        ).add_to(map)

        # Dodajemy okrąg reprezentujący promień wokół centralnej lokalizacji.
        folium.Circle(
            central_location,
            radius=float(radius_km) * 1000,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.1
        ).add_to(map)

        # Generujemy kod HTML mapy
        html_content = map._repr_html_()
        return html_content

    except ValueError:
        # Obsługa błędu przy nieprawidłowej wartości promienia
        messagebox.showerror("Błąd", "Wprowadź prawidłową liczbę dla promienia.")
        return None
    except AttributeError:
        # Obsługa błędu przy niepowodzeniu geokodowania
        messagebox.showerror("Błąd", "Nie można znaleźć lokalizacji dla podanego adresu.")
        return None
