import sys
import os
import pytest
from tkinter import Tk
from unittest.mock import patch, MagicMock

# Dodanie ścieżki do katalogu nadrzędnego, aby można było zaimportować ui
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui import Aplikacja_do_sprawdzania_jakosci_powietrza, Menu, MapaStacji, StronaWyboruStacji, WyborSensora, AnalizaDanych

@pytest.fixture
def app():
    root = Tk()
    app = Aplikacja_do_sprawdzania_jakosci_powietrza()
    yield app
    root.destroy()

def test_center_window(app):
    app.center_window()
    # Testujemy, czy okno jest wyśrodkowane
    assert app.geometry() == '+0+0'

def test_show_frame(app):
    app.show_frame("Menu")
    frame = app.frames["Menu"]
    assert frame.winfo_viewable()

@patch('ui.api_stations')
def test_update_stations(mock_api_stations, app):
    mock_api_stations.return_value = [
        {'stationName': 'Station1', 'id': 114},
        {'stationName': 'Station2', 'id': 117}
    ]
    frame = app.frames["StronaWyboruStacji"]
    frame.update_stations()
    assert frame.station_list.size() == 2

@patch('ui.api_sensors')
def test_show_sensors(mock_api_sensors, app):
    mock_api_sensors.return_value = [
        {'param': {'paramName': 'Sensor1'}, 'id': 642},
        {'param': {'paramName': 'Sensor2'}, 'id': 644}
    ]
    frame = app.frames["WyborSensora"]
    frame.set_station_id(1)
    frame.show_sensors()
    assert frame.sensor_list.size() == 2

@patch('ui.fetch_historical_data')
@patch('ui.analyze_data')
@patch('ui.calculate_trends')
def test_analyze_historical_data(mock_calculate_trends, mock_analyze_data, mock_fetch_historical_data, app):
    mock_fetch_historical_data.return_value = 'some data'
    mock_analyze_data.return_value = ('summary', 'correlation')
    mock_calculate_trends.return_value = 'trends'
    frame = app.frames["AnalizaDanych"]
    frame.set_sensor_id(1)
    frame.analyze_historical_data()
    mock_fetch_historical_data.assert_called_once_with(1)
    mock_analyze_data.assert_called_once_with('some data')
    mock_calculate_trends.assert_called_once_with('some data')

