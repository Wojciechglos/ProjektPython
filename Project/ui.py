# Importowanie modułów
import tkinter as tk
from tkinter import ttk, messagebox
from tkhtmlview import HTMLLabel
from tkinterweb import HtmlFrame

import pandas as pd  # Moduł do pracy z danymi tabelarycznymi
import requests as requests  # Moduł do wykonywania zapytań HTTP
import map_generator
import webbrowser
import tempfile

from analysis import analyze_data, calculate_trends  # Importowanie funkcji do analizy danych
from database import create_database, save_data, \
    fetch_historical_data  # Importowanie funkcji związanych z obsługą bazy danych
# Importowanie funkcji z innych plików
from API import api_stations, api_sensors, api_sensor_data  # Importowanie funkcji do pobierania danych
from plot_data import plot_data  # Importowanie funkcji do tworzenia wykresów
##############################################################################################################
##############################################################################################################
##############################################################################################################

# Klasa głównego okna aplikacji
class Aplikacja_do_sprawdzania_jakosci_powietrza(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do sprawdzania jakości powietrza")
        self.geometry("600x400")
        self.frames = {}

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Tworzenie instancji każdej strony aplikacji i dodanie ich do słownika ram

        for F in (Menu, MapaStacji, StronaWyboruStacji, WyborSensora, DataAnalysisPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Menu")  # Wyświetlenie strony startowej

    # Metoda do wyśrodkowania okna na ekranie
    def center_window(self):
        # Pobranie wymiarów ekranu
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Pobranie wymiarów okna
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Obliczenie współrzędnych środka ekranu
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Ustawienie okna na środku ekranu
        self.geometry("+{}+{}".format(x, y))

    def centrowanie(self):
        for child in self.winfo_children():
            child.grid_configure(padx=200)

    # Metoda do wyświetlania danej strony aplikacji
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Wyświetlenie ramki

# Klasa reprezentująca stronę startową aplikacji
class Menu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Tworzenie etykiety i przycisku startu
        label = ttk.Label(self, text="Witamy w aplikacji do sprawdzania jakości powietrza")
        label.grid(row=0, column=0, pady=10)

        start_button1 = ttk.Button(self, text="Rozpocznij",
                                  command=lambda: controller.show_frame("StronaWyboruStacji"))
        start_button1.grid(row=1, column=0, pady=10)

        start_button_2 = ttk.Button(self, text="Wygeneruj mape stacji",
                                  command=lambda: controller.show_frame("MapaStacji"))
        start_button_2.grid(row=2, column=0, pady=10)

        exit_button = ttk.Button(self, text="Exit",
                                      command=self.exit_application)
        exit_button.grid(row=3, column=0, pady=10)

        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do obsługi zdarzenia kliknięcia przycisku Exit
    def exit_application(self):
        self.controller.quit()  # Zamknięcie aplikacji

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Klasa reprezentująca stronę Mapy stacji
class MapaStacji(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.create_widgets()

# Generowanie okna Wygeneruj mape stacji
    def create_widgets(self):
        ttk.Label(self, text="Adres:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_address = ttk.Entry(self)
        self.entry_address.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Promień (w km):").grid(row=1, column=0, padx=10, pady=10)
        self.entry_radius = ttk.Entry(self)
        self.entry_radius.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self, text="Generuj mapę", command=self.generate_map).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: self.controller.show_frame("Menu")).grid(row=3, column=0, columnspan=2, pady=10)

    def generate_map(self):
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
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Klasa reprezentująca stronę wyboru stacji pomiarowej
class StronaWyboruStacji(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Tworzenie etykiety, listy stacji oraz przycisków
        label = ttk.Label(self, text="Wybór Stacji Pomiarowej")
        label.grid(row=0, column=0, pady=10)

        # Okienko do sortowania
        self.sort_options = ttk.Combobox(self, values=["Nazwa", "ID"], state="readonly")
        self.sort_options.current(0)  # Ustawienie domyślnej opcji sortowania
        self.sort_options.grid(row=1, column=0, columnspan=2, pady=10)

        self.station_list = tk.Listbox(self, height=10, width=50)
        self.station_list.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(self, text="Pobierz wszystkie stacje", command=self.update_stations).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Dalej", command=self.go_to_next_page).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: controller.show_frame("Menu")).grid(row=5, column=0, columnspan=2, pady=10)
        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do aktualizacji listy stacji pomiarowych
    def update_stations(self):
        try:
            stations = api_stations()  # Pobranie stacji pomiarowych
            sort_option = self.sort_options.get()  # Pobranie opcji sortowania
            if sort_option == "Nazwa":
                stations.sort(key=lambda x: x['stationName'])  # Sortowanie po nazwie
            elif sort_option == "ID":
                stations.sort(key=lambda x: x['id'])  # Sortowanie po ID

            self.station_list.delete(0, tk.END)  # Wyczyszczenie listy
            for station in stations:
                station_info = " ".join([station['stationName'], '(', str(station['id']), ')'])
                self.station_list.insert(tk.END, station_info) # Dodanie informacji o stacji do listy
        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać stacji: {e}")  # Wyświetlenie błędu

    # Metoda do przejścia do kolejnej strony
    def go_to_next_page(self):
        selected_station = self.station_list.get(tk.ACTIVE)  # Pobranie zaznaczonej stacji
        if selected_station:
            station_id = selected_station.split('(')[-1].strip(')')  # Pobranie ID stacji
            self.controller.frames["WyborSensora"].set_station_id(
                station_id)  # Ustawienie ID stacji na następnej stronie
            self.controller.show_frame("WyborSensora")  # Przejście do kolejnej strony
        else:
            messagebox.showwarning("Uwaga", "Proszę wybrać stację pomiarową")  # Wyświetlenie ostrzeżenia

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Klasa reprezentująca stronę wyboru sensora
class WyborSensora(ttk.Frame):
    def __init__(self, parent, controller):
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

        ttk.Button(self, text="Pobierz sensory", command=self.show_sensors).grid(row=3, column=0, pady=10)
        ttk.Button(self, text="Dalej", command=self.go_to_next_page).grid(row=4, column=0, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: controller.show_frame("Menu")).grid(row=5, column=0, pady=10)

        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do ustawienia ID stacji
    def set_station_id(self, station_id):
        self.station_id = station_id

    # Metoda do pobrania sensorów dla wybranej stacji

    def show_sensors(self):
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
    def go_to_next_page(self):
        selected_sensor = self.sensor_list.get(tk.ACTIVE)  # Pobranie zaznaczonego sensora
        if selected_sensor:
            sensor_id = selected_sensor.split('(')[-1].strip(')')  # Pobranie ID sensora
            self.controller.frames["DataAnalysisPage"].set_sensor_id(
                sensor_id)  # Ustawienie ID sensora na następnej stronie
            self.controller.show_frame("DataAnalysisPage")  # Przejście do kolejnej strony
        else:
            messagebox.showwarning("Uwaga", "Proszę wybrać sensor")  # Wyświetlenie ostrzeżenia

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Klasa reprezentująca stronę analizy danych
class DataAnalysisPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sensor_id = None

        # Tworzenie etykiety i przycisków do analizy danych
        label = ttk.Label(self, text="Analiza Danych")
        label.grid(row=0, column=0, pady=10)

        ttk.Button(self, text="Pobierz i zapisz dane", command=self.fetch_and_save_sensor_data).grid(row=1, column=0,
                                                                                                     pady=10)
        ttk.Button(self, text="Pokaż dane na histogramie", command=self.show_historical_data).grid(row=2, column=0, pady=10)
        ttk.Button(self, text="Analizuj dane ", command=self.analyze_historical_data).grid(row=3, column=0, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: controller.show_frame("Menu")).grid(row=6, column=0, pady=10)

        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do ustawienia ID sensora
    def set_sensor_id(self, sensor_id):
        self.sensor_id = sensor_id

    # Metoda do pobrania i zapisania danych sensora

    def fetch_and_save_sensor_data(self):
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

    # # Metoda do wyświetlenia danych historycznych
    def show_historical_data(self):
        data = fetch_historical_data(self.sensor_id)  # Pobranie danych historycznych
        if data:
            plot_data(data)  # Wyświetlenie danych na wykresie
        else:
            messagebox.showerror("Błąd", "Brak danych historycznych dla podanej miejscowości.")  # Wyświetlenie błędu

    # Metoda do analizy danych historycznych
    def analyze_historical_data(self):
        data = fetch_historical_data(self.sensor_id)  # Pobranie danych historycznych
        if data:
            summary, correlation = analyze_data(data)  # Analiza danych
            trends = calculate_trends(data)  # Obliczanie trendów
            messagebox.showinfo("Analiza danych",
                                f"Podsumowanie:\n{summary}\n\nKorelacja:\n{correlation}\n\nTrendy:\n{trends}")  # Wyświetlenie wyników analizy
        else:
            messagebox.showerror("Błąd", "Brak danych historycznych dla podanej miejscowości.")  # Wyświetlenie błędu

    # Metoda do wyśrodkowania widżetów na stronie
    def centrowanie(self):
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Uruchomienie tworzenia bazy danych i głównej aplikacji
if __name__ == "__main__":
    create_database()  # Utworzenie bazy danych
    app = Aplikacja_do_sprawdzania_jakosci_powietrza()  # Utworzenie głównej aplikacji
    app.center_window()  # Wyśrodkowanie okna na ekranie
    app.mainloop()  # Uruchomienie pętli głównej aplikacji