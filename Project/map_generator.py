import tkinter as tk
from tkinter import messagebox
import requests
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import tempfile

def generate_map_and_return_html(address, radius_km):
    try:
        geolocator = Nominatim(user_agent="my_application")
        location = geolocator.geocode(address)
        if not location:
            raise AttributeError("Geocoding failed")

        central_location = (location.latitude, location.longitude)

        api_url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"

        response = requests.get(api_url)
        stations = response.json()

        map = folium.Map(location=central_location, zoom_start=10)

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

            if distance <= float(radius_km):
                popup_text = f"id Stacji:{id_stacji}<br>Miasto:{city_name}<br>Gmina:{commune_name}<br>Powiat:{district_name}<br>Woj:{province_name}<br>Odległość: {distance:.2f} km"
                folium.Marker(
                    [lat, lon],
                    popup=popup_text
                ).add_to(map)

        folium.Marker(
            central_location,
            popup="Lokalizacja centralna",
            icon=folium.Icon(color="red")
        ).add_to(map)

        folium.Circle(
            central_location,
            radius=float(radius_km) * 1000,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.1
        ).add_to(map)

        html_content = map._repr_html_()
        return html_content

    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź prawidłową liczbę dla promienia.")
        return None
    except AttributeError:
        messagebox.showerror("Błąd", "Nie można znaleźć lokalizacji dla podanego adresu.")
        return None
