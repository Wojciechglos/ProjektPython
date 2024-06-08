import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def wykres_danych(data):
    # Konwersja dat z formatu tekstowego na obiekty datetime i umieszczenie ich w liście znaczników_czasu
    znaczniki_czasu = [datetime.strptime(wiersz[4], '%Y-%m-%d %H:%M:%S') for wiersz in data]

    # Umieszczenie wartości pomiarów w liście wartosci
    wartosci = [wiersz[3] for wiersz in data]

    # Utworzenie listy unikalnych nazw parametrów z trzeciej kolumny danych
    nazwy_parametrow = list(set(wiersz[2] for wiersz in data))

    # Utworzenie nowego wykresu
    plt.figure(figsize=(10, 5))

    # Iteracja po każdym unikalnym parametrze
    for nazwa_parametru in nazwy_parametrow:
        # Wybór wartości dla danego parametru
        wartosci_parametru = [wiersz[3] for wiersz in data if wiersz[2] == nazwa_parametru]
        wartosci_parametru = [wartosc for wartosc in wartosci_parametru if wartosc is not None]  # Filtruj wartości None

        # Wybór dat dla danego parametru
        znaczniki_czasu_parametru = [datetime.strptime(wiersz[4], '%Y-%m-%d %H:%M:%S') for wiersz in data if wiersz[2] == nazwa_parametru]

        # Upewnij się, że mamy tyle samo danych dla każdego parametru
        dlugosc_minimalna = min(len(wartosci_parametru), len(znaczniki_czasu_parametru))
        wartosci_parametru = wartosci_parametru[:dlugosc_minimalna]
        znaczniki_czasu_parametru = znaczniki_czasu_parametru[:dlugosc_minimalna]

        # Dodanie serii danych do wykresu dla danego parametru
        linia, = plt.plot(znaczniki_czasu_parametru, wartosci_parametru, label=nazwa_parametru)

        # Dodanie linii trendu
        if wartosci_parametru:  # Sprawdź, czy wartosci_parametru nie jest puste
            wspolczynniki_wielomianu = np.polyfit(range(len(wartosci_parametru)), wartosci_parametru, 1)
            linia_trendu = np.polyval(wspolczynniki_wielomianu, range(len(wartosci_parametru)))
            plt.plot(znaczniki_czasu_parametru, linia_trendu, linestyle='--', color='orange')

        # Analiza danych
        wartosc_minimalna = np.min(wartosci_parametru)
        wartosc_maksymalna = np.max(wartosci_parametru)
        wartosc_srednia = np.mean(wartosci_parametru)
        trend = "wzrost" if wspolczynniki_wielomianu[0] < 0 else "spadek"

        # Dodanie danych w legendzie
        plt.legend(handles=[linia], labels=[f'{nazwa_parametru} (min: {wartosc_minimalna:.1f}, śr: {wartosc_srednia:.1f}, max: {wartosc_maksymalna:.1f})'], loc='upper left')

    # Dodanie etykiet osi x i y
    plt.xlabel('Czas')
    plt.ylabel('Wartość')

    # Wyświetlenie wykresu
    plt.show()
