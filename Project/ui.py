# Importowanie modułów do interfejsu użytkownika Tkinter
import tkinter as tk  # Tkinter jest biblioteką do tworzenia GUI w Pythonie
from tkinter import ttk, messagebox  # ttk zawiera zaawansowane widżety Tkinter, a messagebox to moduł do wyświetlania okienek dialogowych

import requests as requests  # Moduł requests służy do wykonywania zapytań HTTP

import map_generator  # Prawdopodobnie moduł zawierający funkcje lub klasy do generowania map

import webbrowser  # Webbrowser umożliwia otwieranie stron internetowych w domyślnej przeglądarce

import tempfile  # Tempfile zapewnia interfejs do zarządzania tymczasowymi plikami i katalogami

from database import create_database, save_data, Dane  # Importowanie funkcji związanych z obsługą bazy danych
# create_database: Tworzy nową bazę danych lub łączy się z istniejącą
# save_data: Zapisuje dane do bazy danych
# Dane: Prawdopodobnie funkcja do pobierania danych z bazy danych

from API import api_stations, api_sensors, api_sensor_data, api_index_powietrza  # Importowanie funkcji do pobierania danych z API
# api_stations: Pobiera listę stacji z API
# api_sensors: Pobiera listę sensorów dla danej stacji z API
# api_sensor_data: Pobiera dane z sensora z API
# api_index_powietrza: Pobiera indeks jakości powietrza dla danego sensora z API

from wykres import wykres_danych  # Importowanie funkcji do tworzenia wykresów danych
# wykres_danych: Funkcja do generowania wykresów na podstawie danych
"""
Importowanie niezbędnych modułów i definicja głównych klas aplikacji do sprawdzania jakości powietrza.

Imports:
- tkinter as tk: Biblioteka do tworzenia GUI w Pythonie.
- ttk, messagebox from tkinter: ttk zawiera zaawansowane widżety Tkinter, a messagebox to moduł do wyświetlania okienek dialogowych.
- requests as requests: Moduł do wykonywania zapytań HTTP.
- map_generator: Prawdopodobnie moduł zawierający funkcje lub klasy do generowania map.
- webbrowser: Umożliwia otwieranie stron internetowych w domyślnej przeglądarce.
- tempfile: Zapewnia interfejs do zarządzania tymczasowymi plikami i katalogami.
- create_database, save_data, Dane from database: Funkcje związane z obsługą bazy danych.
- api_stations, api_sensors, api_sensor_data, api_index_powietrza from API: Funkcje do pobierania danych z API.
- wykres_danych from wykres: Funkcja do tworzenia wykresów na podstawie danych.

Klasy:
- Aplikacja_do_sprawdzania_jakosci_powietrza(tk.Tk): Główne okno aplikacji.
- Menu(ttk.Frame): Strona startowa aplikacji.
- MapaStacji(ttk.Frame): Strona mapy stacji.
- StronaWyboruStacji(ttk.Frame): Strona wyboru stacji pomiarowej.
- WyborSensora(ttk.Frame): Strona wyboru sensora.
- AnalizaDanych(ttk.Frame): Strona analizy danych.

Metody:
- Aplikacja_do_sprawdzania_jakosci_powietrza.center_window(): Metoda do wyśrodkowania okna aplikacji na ekranie.
- Aplikacja_do_sprawdzania_jakosci_powietrza.centrowanie(): Metoda do wyśrodkowania widżetów na stronie aplikacji.
- Aplikacja_do_sprawdzania_jakosci_powietrza.wyświetlenie_ramki(page_name): Metoda do wyświetlenia danej strony aplikacji.
- Menu.centrowanie(): Metoda do wyśrodkowania widżetów na stronie Menu.
- Menu.wyjscie_z_aplikacji(): Metoda do obsługi zdarzenia kliknięcia przycisku Exit.
- MapaStacji.generowanie_pol_mapy(): Metoda do generowania pól i obsługi mapy stacji.
- MapaStacji.generowanie_mapy(): Metoda do generowania mapy stacji na podstawie podanych danych.
- StronaWyboruStacji.aktualizuj_stacje(): Metoda do aktualizacji listy stacji pomiarowych na podstawie wprowadzonych danych.
- StronaWyboruStacji.idz_do_nastepnej_strony(): Metoda do przejścia do strony wyboru sensora po wybraniu stacji pomiarowej.
- WyborSensora.ustaw_id_stacji(station_id): Metoda do ustawienia ID wybranej stacji na stronie wyboru sensora.
- WyborSensora.aktualizuj_sensory(): Metoda do aktualizacji listy sensorów na podstawie wybranej stacji.
- WyborSensora.idz_do_nastepnej_strony(): Metoda do przejścia do strony analizy danych po wybraniu sensora.
- AnalizaDanych.ustaw_id_sensora(sensor_id): Metoda do ustawienia ID wybranego sensora na stronie analizy danych.
- AnalizaDanych.pobranie_danych_sensora(): Metoda do pobrania i zapisania danych sensora do bazy danych.
- AnalizaDanych.rysowanie_wykresu(): Metoda do wyświetlenia danych historycznych sensora na wykresie.

"""

# Klasa głównego okna aplikacji
class Aplikacja_do_sprawdzania_jakosci_powietrza(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do sprawdzania jakości powietrza")
        self.geometry("650x450")
        self.frames = {}

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Tworzenie instancji każdej strony aplikacji i dodanie ich do słownika ram

        for F in (Menu, MapaStacji, StronaWyboruStacji, WyborSensora, AnalizaDanych):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.wyświetlenie_ramki("Menu")  # Wyświetlenie strony startowej

    # Metoda do wyśrodkowania okna na ekranie
    def center_window(self):
        # Pobranie wymiarów ekranu
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Pobranie wymiarów okna
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Obliczenie współrzędnych środka ekranu
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Ustawienie okna na środku ekranu
        self.geometry("+{}+{}".format(x, y))

    def centrowanie(self):
        for child in self.winfo_children():
            child.grid_configure(padx=200)

    # Metoda do wyświetlania danej strony aplikacji
    def wyświetlenie_ramki(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Wyświetlenie ramki

# Klasa reprezentująca stronę startową aplikacji
class Menu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Tworzenie etykiety i przycisków startu
        label = ttk.Label(self, text="Witamy w aplikacji do sprawdzania jakości powietrza")
        label.grid(row=0, column=0, pady=10)

        start_button1 = ttk.Button(self, text="Rozpocznij z danymi online",
                                  command=lambda: controller.wyświetlenie_ramki("StronaWyboruStacji"))
        start_button1.grid(row=1, column=0, pady=10)

        start_button2 = ttk.Button(self, text="Rozpocznij z danymi offline ",
                                   command=lambda: controller.wyświetlenie_ramki("StronaWyboruStacji"))
        start_button2.grid(row=2, column=0, pady=10)

        start_button3 = ttk.Button(self, text="Wygeneruj mape stacji",
                                  command=lambda: controller.wyświetlenie_ramki("MapaStacji"))
        start_button3.grid(row=3, column=0, pady=10)

        exit_button = ttk.Button(self, text="Exit",
                                      command=self.wyjscie_z_aplikacji)
        exit_button.grid(row=4, column=0, pady=10)

        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    def centrowanie(self):
        for child in self.winfo_children():
            child.grid_configure(padx=200)

    # Metoda do obsługi zdarzenia kliknięcia przycisku Exit
    def wyjscie_z_aplikacji(self):
        self.controller.quit()  # Zamknięcie aplikacji

# Klasa reprezentująca stronę Mapy stacji
class MapaStacji(ttk.Frame):

    def __init__(self, parent, controller):
        """
                Inicjalizacja ekranu Mapy stacji.

                Metoda __init__ jest konstruktorem klasy MapaStacji, dziedziczącej po ttk.Frame,
                czyli ramce interfejsu tkinterowego.

                Parametry:
                - parent: rodzic ramki, zazwyczaj główne okno aplikacji.
                - controller: obiekt kontrolera aplikacji, który zarządza przełączaniem między stronami.

                Inicjalizuje ekran Mapy stacji, zawierający pola do wprowadzenia adresu i promienia,
                przycisk do generowania mapy oraz przycisk powrotu do MENU.
                """
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.generowanie_pol_mapy()

# Generowanie okna Wygeneruj mape stacji
    def generowanie_pol_mapy(self):
        """
                Generuje pola formularza dla generowania mapy stacji.

                Tworzy etykiety i pola do wprowadzenia adresu oraz promienia, przyciski do generowania mapy
                i powrotu do MENU oraz przypisuje im odpowiednie funkcje.

                Wykorzystuje:
                - ttk.Label: Etykiety do opisania pól formularza.
                - ttk.Entry: Pola do wprowadzania tekstu.
                - ttk.Button: Przyciski do wywoływania funkcji.
                """
        ttk.Label(self, text="Adres:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_address = ttk.Entry(self)
        self.entry_address.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Promień (w km):").grid(row=1, column=0, padx=10, pady=10)
        self.entry_radius = ttk.Entry(self)
        self.entry_radius.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self, text="Generuj mapę", command=self.generowanie_mapy).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: self.controller.wyświetlenie_ramki("Menu")).grid(row=3, column=0, columnspan=2, pady=10)

    def generowanie_mapy(self):
        """
                Generuje mapę stacji na podstawie wprowadzonych danych i otwiera ją w przeglądarce.

                Pobiera adres i promień z pól formularza, generuje mapę przy użyciu funkcji map_generator.generate_map_and_return_html,
                tworzy tymczasowy plik HTML, zapisuje w nim wygenerowany kod HTML i otwiera ten plik w przeglądarce.
                """
        address = self.entry_address.get()
        radius_km = self.entry_radius.get()
        html_content = map_generator.generate_map_and_return_html(address, radius_km)

        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            tmpfile.write(html_content.encode("utf-8"))
            tmpfile_path = tmpfile.name

        # Open the temporary HTML file in the default web browser
        webbrowser.open('file://' + tmpfile_path)

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        """
        Metoda do wyśrodkowania wszystkich widżetów na stronie Mapy stacji.

        Iteruje przez wszystkie dzieci ramki (self.winfo_children()) i konfiguruje
        odstępy w poziomie (padx) dla każdego z nich, aby wyśrodkować je na stronie.
        """
        for child in self.winfo_children():
            child.grid_configure(padx=200)

def api_stations():
    """
    Funkcja pobierająca stacje pomiarowe z API GIOŚ (Główny Inspektorat Ochrony Środowiska).

    Zwraca:
    - dict lub list: Lista stacji pomiarowych w formacie JSON lub None, jeśli nie udało się pobrać danych.
    """
    # Funkcja pobierająca stacje pomiarowe z API
    try:
        response = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/findAll")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Błąd", f"Nie udało się pobrać stacji: {e}")
        return None

class StronaWyboruStacji(ttk.Frame):
    """
            Inicjalizacja strony wyboru stacji pomiarowych.

            Metoda __init__ jest konstruktorem klasy StronaWyboruStacji, dziedziczącej po ttk.Frame,
            czyli ramce interfejsu tkinterowego.

            Parametry:
            - parent: rodzic ramki, zazwyczaj główne okno aplikacji.
            - controller: obiekt kontrolera aplikacji, który zarządza przełączaniem między stronami.

            Inicjalizuje stronę zawierającą etykietę, pole do wprowadzenia nazwy miejscowości,
            rozwijane menu do sortowania, listę stacji pomiarowych oraz przyciski do interakcji.
            """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Tworzenie etykiety, listy stacji oraz przycisków
        label = ttk.Label(self, text="Wybór Stacji Pomiarowej")
        label.grid(row=0, column=0, pady=10)

        # Pole do wpisania nazwy miejscowości
        self.city_name_var = tk.StringVar()
        self.city_name_entry = ttk.Entry(self, textvariable=self.city_name_var)
        self.city_name_entry.grid(row=1, column=0, columnspan=2, pady=10)

        # Okienko do sortowania
        self.sort_options = ttk.Combobox(self, values=["Nazwa", "ID"], state="readonly")
        self.sort_options.current(0)  # Ustawienie domyślnej opcji sortowania
        self.sort_options.grid(row=2, column=0, columnspan=2, pady=10)

        self.station_list = tk.Listbox(self, height=10, width=50)
        self.station_list.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(self, text="Odśwież okno stacji", command=self.aktualizuj_stacje).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Wybierz stacje i przejdź dalej", command=self.idz_do_nastepnej_strony).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: controller.wyświetlenie_ramki("Menu")).grid(row=6, column=0, columnspan=2, pady=10)
        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do aktualizacji listy stacji pomiarowych
    def aktualizuj_stacje(self):
        """
                Aktualizuje listę stacji pomiarowych na podstawie wprowadzonych filtrów.

                Pobiera stacje pomiarowe z API używając funkcji api_stations(),
                sortuje je według wybranej opcji (Nazwa lub ID), filtrowanej przez wprowadzoną nazwę miejscowości.
                Wyświetla listę stacji w oknie.
                """
        try:
            stations = api_stations()  # Pobranie stacji pomiarowych
            if stations is None:
                return  # Przerwij, jeśli nie udało się pobrać danych

            sort_option = self.sort_options.get()  # Pobranie opcji sortowania
            if sort_option == "Nazwa":
                stations.sort(key=lambda x: x['stationName'])  # Sortowanie po nazwie
            elif sort_option == "ID":
                stations.sort(key=lambda x: x['id'])  # Sortowanie po ID

            city_name = self.city_name_var.get().strip().lower()
            if city_name:
                stations = [station for station in stations if city_name in station['stationName'].lower()]

            self.station_list.delete(0, tk.END)  # Wyczyszczenie listy
            for station in stations:
                station_info = f"{station['stationName']} ({station['id']})"
                self.station_list.insert(tk.END, station_info)  # Dodanie informacji o stacji do listy
        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać stacji: {e}")  # Wyświetlenie błędu
        except AttributeError:
            messagebox.showerror("Błąd", "Dane stacji są niepoprawne.")

    # Metoda do przejścia do kolejnej strony
    def idz_do_nastepnej_strony(self):
        """
               Przechodzi do kolejnej strony aplikacji po wybraniu stacji pomiarowej.

               Pobiera zaznaczoną stację z listy, wydobywa jej ID i przekazuje je do następnej strony
               do wyboru sensora na tej stacji, ustawiając odpowiednie ID stacji na następnej stronie
               i wywołując funkcję wyświetlenia tej strony.
               """
        selected_station = self.station_list.get(tk.ACTIVE)  # Pobranie zaznaczonej stacji
        if selected_station:
            station_id = selected_station.split('(')[-1].strip(')')  # Pobranie ID stacji
            self.controller.frames["WyborSensora"].ustaw_id_stacji(
                station_id)  # Ustawienie ID stacji na następnej stronie
            self.controller.wyświetlenie_ramki("WyborSensora")  # Przejście do kolejnej strony
        else:
            messagebox.showwarning("Uwaga", "Proszę wybrać stację pomiarową")  # Wyświetlenie ostrzeżenia

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        """
        Metoda do wyśrodkowania wszystkich widżetów na stronie StronyWyboruStacji.

        Iteruje przez wszystkie dzieci ramki (self.winfo_children()) i konfiguruje
        odstępy w poziomie (padx) dla każdego z nich, aby wyśrodkować je na stronie.
        """
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Klasa reprezentująca stronę wyboru sensora
class WyborSensora(ttk.Frame):
    def __init__(self, parent, controller):
        """
        Inicjalizacja strony wyboru sensora.

        Metoda __init__ jest konstruktorem klasy WyborSensora, dziedziczącej po ttk.Frame,
        czyli ramce interfejsu tkinterowego.

        Parametry:
        - parent: rodzic ramki, zazwyczaj główne okno aplikacji.
        - controller: obiekt kontrolera aplikacji, który zarządza przełączaniem między stronami.

        Inicjalizuje stronę zawierającą etykietę, rozwijane menu do sortowania, listę sensorów oraz przyciski do interakcji.
        """
        super().__init__(parent)
        self.controller = controller
        self.station_id = None

        # Tworzenie etykiety, listy sensorów oraz przycisków
        label = ttk.Label(self, text="Wybór Sensora")
        label.grid(row=0, column=0, pady=10)

        # Okienko do sortowania
        self.sort_options = ttk.Combobox(self, values=["Nazwa", "ID"], state="readonly")
        self.sort_options.current(0)  # Ustawienie domyślnej opcji sortowania
        self.sort_options.grid(row=1, column=0, columnspan=2, pady=10)

        self.sensor_list = tk.Listbox(self, height=10, width=50)
        self.sensor_list.grid(row=2, column=0, pady=5)

        ttk.Button(self, text="Odśwież okno sensorów", command=self.aktualizuj_sensory).grid(row=3, column=0, pady=10)
        ttk.Button(self, text="Wybierz sensor i przejdź dalej", command=self.idz_do_nastepnej_strony).grid(row=4, column=0, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: controller.wyświetlenie_ramki("Menu")).grid(row=5, column=0, pady=10)

        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do ustawienia ID stacji
    def ustaw_id_stacji(self, station_id):
        """
        Ustawia ID wybranej stacji na stronie WyborSensora.

        Parametry:
        - station_id: ID wybranej stacji pomiarowej.
        """
        self.station_id = station_id

    # Metoda do pobrania sensorów dla wybranej stacji

    def aktualizuj_sensory(self):
        """
        Aktualizuje listę sensorów na podstawie wybranej stacji.

        Pobiera sensory dla wybranej stacji używając funkcji api_sensors(self.station_id),
        sortuje je według wybranej opcji (Nazwa lub ID) i wyświetla listę sensorów w oknie.
        """
        if not self.station_id:
            return
        try:
            sensors = api_sensors(self.station_id)  # Pobranie sensorów
            sort_option = self.sort_options.get()  # Pobranie opcji sortowania
            if sort_option == "Nazwa":
                sensors.sort(key=lambda x: x['param']['paramName'])  # Sortowanie po nazwie
            elif sort_option == "ID":
                sensors.sort(key=lambda x: x['id'])  # Sortowanie po ID
            self.sensor_list.delete(0, tk.END)  # Wyczyszczenie listy sensorów
            for sensor in sensors:
                self.sensor_list.insert(tk.END,
                                        f"{sensor['param']['paramName']} ({sensor['id']})")  # Dodanie sensorów do listy
        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać sensorów: {e}")  # Wyświetlenie błędu

    # Metoda do przejścia do kolejnej strony
    def idz_do_nastepnej_strony(self):
        """
             Przechodzi do kolejnej strony aplikacji po wybraniu sensora.

             Pobiera zaznaczony sensor z listy, wydobywa jego ID i przekazuje je do strony
             AnalizaDanych, ustawiając odpowiednie ID sensora na tej stronie i wywołując funkcję
             wyświetlenia tej strony.
             """
        selected_sensor = self.sensor_list.get(tk.ACTIVE)  # Pobranie zaznaczonego sensora
        if selected_sensor:
            sensor_id = selected_sensor.split('(')[-1].strip(')')  # Pobranie ID sensora
            self.controller.frames["AnalizaDanych"].ustaw_id_sensora(
                sensor_id)  # Ustawienie ID sensora na następnej stronie
            self.controller.wyświetlenie_ramki("AnalizaDanych")  # Przejście do kolejnej strony
        else:
            messagebox.showwarning("Uwaga", "Proszę wybrać sensor")  # Wyświetlenie ostrzeżenia

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        """
        Metoda do wyśrodkowania wszystkich widżetów na stronie WyborSensora.

        Iteruje przez wszystkie dzieci ramki (self.winfo_children()) i konfiguruje
        odstępy w poziomie (padx) dla każdego z nich, aby wyśrodkować je na stronie.
        """
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Klasa reprezentująca stronę analizy danych
class AnalizaDanych(ttk.Frame):
    """
    Inicjalizacja strony analizy danych.

    Metoda __init__ jest konstruktorem klasy AnalizaDanych, dziedziczącej po ttk.Frame,
    czyli ramce interfejsu tkinterowego.

    Parametry:
    - parent: rodzic ramki, zazwyczaj główne okno aplikacji.
    - controller: obiekt kontrolera aplikacji, który zarządza przełączaniem między stronami.

    Inicjalizuje stronę zawierającą etykietę "Analiza Danych", przyciski do pobierania i zapisywania danych,
    oraz przycisk do wyjścia do MENU.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sensor_id = None

        # Tworzenie etykiety i przycisków do analizy danych
        label = ttk.Label(self, text="Analiza Danych")
        label.grid(row=0, column=0, pady=10)
        ttk.Button(self, text="Pobierz i zapisz dane", command=self.pobranie_danych_sensora).grid(row=1, column=0, pady=10)
        ttk.Button(self, text="Pokaż dane na histogramie", command=self.rysowanie_wykresu).grid(row=2, column=0, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: controller.wyświetlenie_ramki("Menu")).grid(row=6, column=0, pady=10)

        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        """
        Metoda do wyśrodkowania wszystkich widżetów na stronie AnalizaDanych.

        Iteruje przez wszystkie dzieci ramki (self.winfo_children()) i konfiguruje
        odstępy w poziomie (padx) dla każdego z nich, aby wyśrodkować je na stronie.
        """
        for child in self.winfo_children():
            child.grid_configure(padx=200)

    # Metoda do ustawienia ID sensora
    def ustaw_id_sensora(self, sensor_id):
        """
        Ustawia ID wybranego sensora na stronie AnalizaDanych.

        Parametry:
        - sensor_id: ID wybranego sensora.
        """
        self.sensor_id = sensor_id

    # Metoda do pobrania i zapisania danych sensora
    def pobranie_danych_sensora(self):
        """
        Pobiera i zapisuje dane sensora do bazy danych.

        Sprawdza, czy został wybrany sensor (self.sensor_id != None).
        Wywołuje funkcję api_sensor_data(self.sensor_id) do pobrania danych sensora.
        Zapisuje dane do bazy danych wywołując funkcję save_data().
        Wyświetla informacje o sukcesie lub błędzie za pomocą messagebox.
        """
        if not self.sensor_id:
            return
        try:
            data = api_sensor_data(self.sensor_id)  # Pobranie danych sensora
            if 'values' in data:
                for value in data['values']:
                    save_data(self.sensor_id, data['key'], value['value'],
                              value['date'])  # Zapisanie danych do bazy danych
                messagebox.showinfo("Sukces",
                                    "Dane zostały zapisane w bazie danych.")  # Wyświetlenie informacji o sukcesie
            else:
                messagebox.showerror("Błąd", "Brak danych pomiarowych dla wybranego sensora.")  # Wyświetlenie błędu
        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać danych sensora: {e}")  # Wyświetlenie błędu

    #  Metoda do rysowania wykresu
    def rysowanie_wykresu(self):
        """
        Metoda do rysowania wykresu danych dla wybranego sensora.

        Pobiera dane z wybranego sensora używając klasy Dane(sensor_id).
        Jeśli dane są dostępne, wywołuje funkcję wykres_danych(data) do wyświetlenia danych na wykresie.
        W przeciwnym razie wyświetla błąd, że brak danych historycznych dla podanej miejscowości.
        """
        data = Dane(self.sensor_id)  # Pobranie danych
        if data:
            wykres_danych(data)  # Wyświetlenie danych na wykresie
        else:
            messagebox.showerror("Błąd", "Brak danych historycznych dla podanej miejscowości.")  # Wyświetlenie błędu


# Uruchomienie tworzenia bazy danych i głównej aplikacji
if __name__ == "__main__":
    create_database()  # Utworzenie bazy danych
    app = Aplikacja_do_sprawdzania_jakosci_powietrza()  # Utworzenie głównej aplikacji
    app.center_window()  # Wyśrodkowanie okna na ekranie
    app.mainloop()  # Uruchomienie pętli głównej aplikacji