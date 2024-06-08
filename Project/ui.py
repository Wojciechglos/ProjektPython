# Importowanie modułów
import tkinter as tk
from tkinter import ttk, messagebox
import requests as requests  # Moduł do wykonywania zapytań HTTP
import map_generator
import webbrowser
import tempfile
from database import create_database, save_data, Dane  # Importowanie funkcji związanych z obsługą bazy danych
# Importowanie funkcji z innych plików
from API import api_stations, api_sensors, api_sensor_data, api_index_powietrza  # Importowanie funkcji do pobierania danych
from wykres import wykres_danych  # Importowanie funkcji do tworzenia wykresów


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
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.generowanie_pol_mapy()

# Generowanie okna Wygeneruj mape stacji
    def generowanie_pol_mapy(self):
        ttk.Label(self, text="Adres:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_address = ttk.Entry(self)
        self.entry_address.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Promień (w km):").grid(row=1, column=0, padx=10, pady=10)
        self.entry_radius = ttk.Entry(self)
        self.entry_radius.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self, text="Generuj mapę", command=self.generowanie_mapy).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: self.controller.wyświetlenie_ramki("Menu")).grid(row=3, column=0, columnspan=2, pady=10)

    def generowanie_mapy(self):
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

def api_stations():
    # Funkcja pobierająca stacje pomiarowe z API
    try:
        response = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/findAll")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        messagebox.showerror("Błąd", f"Nie udało się pobrać stacji: {e}")
        return None

class StronaWyboruStacji(ttk.Frame):
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

        ttk.Button(self, text="Odśwież okno sensorów", command=self.aktualizuj_sensory).grid(row=3, column=0, pady=10)
        ttk.Button(self, text="Wybierz sensor i przejdź dalej", command=self.idz_do_nastepnej_strony).grid(row=4, column=0, pady=10)
        ttk.Button(self, text="Wyjście do MENU", command=lambda: controller.wyświetlenie_ramki("Menu")).grid(row=5, column=0, pady=10)

        self.centrowanie()  # Wyśrodkowanie widżetów na stronie

    # Metoda do ustawienia ID stacji
    def ustaw_id_stacji(self, station_id):
        self.station_id = station_id

    # Metoda do pobrania sensorów dla wybranej stacji

    def aktualizuj_sensory(self):
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
        for child in self.winfo_children():
            child.grid_configure(padx=200)

# Klasa reprezentująca stronę analizy danych
class AnalizaDanych(ttk.Frame):
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
        for child in self.winfo_children():
            child.grid_configure(padx=200)

    # Metoda do ustawienia ID sensora
    def ustaw_id_sensora(self, sensor_id):
        self.sensor_id = sensor_id

    # Metoda do pobrania i zapisania danych sensora
    def pobranie_danych_sensora(self):
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
    def rysowanie_wykresu(self):
        data = Dane(self.sensor_id)  # Pobranie danych historycznych
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