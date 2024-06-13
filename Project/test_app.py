import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk
from ui import Aplikacja_do_sprawdzania_jakosci_powietrza, api_stations, api_sensors, api_sensor_data  # Importowanie Twojego kodu

class TestApp(unittest.TestCase):

    def setUp(self):
        self.ui = Aplikacja_do_sprawdzania_jakosci_powietrza()

    def tearDown(self):
        self.ui.destroy()

    def test_initialization(self):
        self.assertIsInstance(self.ui, tk.Tk)
        self.assertEqual(self.ui.title(), "Aplikacja do sprawdzania jakości powietrza")
        self.assertEqual(self.ui.geometry(), "650x450")



    @patch('ui.api_stations')
    def test_api_stations_success(self, mock_api_stations):
        mock_response = [
            {"stationName": "Station 1", "id": 1},
            {"stationName": "Station 2", "id": 2}
        ]
        mock_api_stations.return_value = mock_response
        result = api_stations()
        self.assertEqual(result, mock_response)

    @patch('ui.api_stations')
    def test_api_stations_failure(self, mock_api_stations):
        mock_api_stations.side_effect = requests.RequestException("Error")
        result = api_stations()
        self.assertIsNone(result)

    @patch('ui.api_sensors')
    def test_api_sensors_success(self, mock_api_sensors):
        mock_response = [
            {"param": {"paramName": "PM10"}, "id": 1},
            {"param": {"paramName": "PM2.5"}, "id": 2}
        ]
        mock_api_sensors.return_value = mock_response
        result = api_sensors(1)
        self.assertEqual(result, mock_response)

    @patch('ui.api_sensors')
    def test_api_sensors_failure(self, mock_api_sensors):
        mock_api_sensors.side_effect = requests.RequestException("Error")
        result = api_sensors(1)
        self.assertIsNone(result)

    @patch('ui.api_sensor_data')
    def test_api_sensor_data_success(self, mock_api_sensor_data):
        mock_response = {
            "key": "PM10",
            "values": [{"value": 50, "date": "2024-01-01 00:00:00"}]
        }
        mock_api_sensor_data.return_value = mock_response
        result = api_sensor_data(1)
        self.assertEqual(result, mock_response)

    @patch('ui.api_sensor_data')
    def test_api_sensor_data_failure(self, mock_api_sensor_data):
        mock_api_sensor_data.side_effect = requests.RequestException("Error")
        result = api_sensor_data(1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
