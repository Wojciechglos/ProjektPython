import matplotlib.pyplot as plt
from datetime import datetime


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
        # Wybór dat dla danego parametru
        param_timestamps = [datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S') for row in data if row[2] == param_name]

        # Dodanie serii danych do wykresu dla danego parametru
        plt.plot(param_timestamps, param_values, label=param_name)

    # Dodanie etykiet osi x i y
    plt.xlabel('Time')
    plt.ylabel('Value')

    # Dodanie legendy z nazwami parametrów
    plt.legend()

    # Wyświetlenie wykresu
    plt.show()
