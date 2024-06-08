import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def plot_data(data):
    # Konwersja dat z formatu tekstowego na obiekty datetime i umieszczenie ich w liście timestamps
    timestamps = [datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S') for row in data]

    # Umieszczenie wartości pomiarów w liście values
    values = [row[3] for row in data]

    # Utworzenie listy unikalnych nazw parametrów z trzeciej kolumny danych
    param_names = list(set(row[2] for row in data))

    # Utworzenie nowego wykresu
    plt.figure(figsize=(10, 5))

    # Iteracja po każdym unikalnym parametrze
    for param_name in param_names:
        # Wybór wartości dla danego parametru
        param_values = [row[3] for row in data if row[2] == param_name]
        param_values = [value for value in param_values if value is not None]  # Filtruj wartości None
        print("param_values:", param_values)  # Dodatkowy wiersz do debugowania
        # Wybór dat dla danego parametru
        param_timestamps = [datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S') for row in data if row[2] == param_name]

        # Upewnij się, że mamy tyle samo danych dla każdego parametru
        min_length = min(len(param_values), len(param_timestamps))
        param_values = param_values[:min_length]
        param_timestamps = param_timestamps[:min_length]

        # Dodanie serii danych do wykresu dla danego parametru
        plt.plot(param_timestamps, param_values, label=param_name)

        # Dodanie linii trendu
        if param_values:  # Sprawdź, czy param_values nie jest puste
            poly_coeffs = np.polyfit(range(len(param_values)), param_values, 1)
            print("poly_coeffs:", poly_coeffs)  # Dodatkowy wiersz do debugowania
            trend_line = np.polyval(poly_coeffs, range(len(param_values)))
            plt.plot(param_timestamps, trend_line, linestyle='--', color='orange')

    # Dodanie etykiet osi x i y
    plt.xlabel('Czas')
    plt.ylabel('Wartość')

    # Dodanie legendy z nazwami parametrów
    plt.legend()

    # Wyświetlenie wykresu
    plt.show()
