import unittest
import sqlite3
from datetime import datetime

# Importy funkcji do testowania
from database import create_database, save_data, Dane

# Klasa zawierająca testy jednostkowe dla funkcji obsługi bazy danych
class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """
        Metoda setUp jest wywoływana przed każdym testem.
        Tutaj wykonujemy operacje inicjalizacyjne, takie jak utworzenie bazy danych,
        aby zapewnić, że każdy test będzie działał na czystej bazie danych.
        """
        create_database()  # Utworzenie bazy danych, jeśli nie istnieje

    def tearDown(self):
        """
        Metoda tearDown jest wywoływana po każdym teście.
        Celem tej metody jest wykonanie operacji sprzątających, takich jak usunięcie
        tymczasowej tabeli 'dane' z bazy danych, aby nie pozostawały po niej śmieci po teście.
        """
        conn = sqlite3.connect('baza_gios.db')
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS dane1")  # Usunięcie tabeli po zakończeniu testu
        conn.commit()
        conn.close()

    def test_save_and_retrieve_data(self):
        """
        Metoda testowa sprawdzająca funkcjonalność zapisu i odczytu danych z bazy danych.
        Testuje funkcje save_data() oraz Dane(), aby upewnić się, że zapisane dane
        mogą być później poprawnie odczytane zgodnie z oczekiwaniami.
        """
        # Przygotowanie danych testowych
        city = "Warszawa"
        param_name = "PM10"
        value = 25.6
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Zapisanie danych do bazy danych
        save_data(city, param_name, value, timestamp)

        # Pobranie danych dla danego miasta z bazy danych
        result = Dane(city)

        # Sprawdzenie, czy dane zostały poprawnie zapisane i odczytane
        self.assertIsInstance(result, list)  # Czy wynik jest listą
        self.assertEqual(len(result), 1)  # Czy jest dokładnie jeden wynik
        self.assertEqual(result[0][1], city)  # Czy miasto się zgadza
        self.assertEqual(result[0][2], param_name)  # Czy nazwa parametru się zgadza
        self.assertEqual(result[0][3], value)  # Czy wartość parametru się zgadza
        self.assertEqual(result[0][4], timestamp)  # Czy znacznik czasu się zgadza

if __name__ == '__main__':
    unittest.main()
