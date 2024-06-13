import sqlite3

def create_database():
    """
    Tworzy bazę danych SQLite i tabelę 'dane', jeśli nie istnieje.

    Tabela 'dane' ma następującą strukturę:
    - id: INTEGER PRIMARY KEY
    - city: TEXT
    - param_name: TEXT
    - value: REAL
    - timestamp: TEXT
    """
    conn = sqlite3.connect('baza_gios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dane
                 (id INTEGER PRIMARY KEY, city TEXT, param_name TEXT, value REAL, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_data(city, param_name, value, timestamp):
    """
      Zapisuje dane do tabeli 'dane' w bazie danych SQLite.

      Argumenty:
      - city : str
          Nazwa miasta.
      - param_name : str
          Nazwa parametru.
      - value : float
          Wartość parametru.
      - timestamp : str
          Znacznik czasu w formacie tekstowym.
      """
    conn = sqlite3.connect('baza_gios.db')
    c = conn.cursor()
    c.execute("INSERT INTO dane (city, param_name, value, timestamp) VALUES (?, ?, ?, ?)", (city, param_name, value, timestamp))
    conn.commit()
    conn.close()

def Dane(city):
    """
       Pobiera wszystkie dane z tabeli 'dane' dla danego miasta i zwraca je jako listę wierszy.

       Argumenty:
       - city : str
           Nazwa miasta, dla którego mają być pobrane dane.

       Zwraca:
       - list
           Lista wierszy z tabeli 'dane' posortowanych malejąco według znacznika czasu.
       """
    conn = sqlite3.connect('baza_gios.db')
    c = conn.cursor()
    c.execute("SELECT * FROM dane WHERE city = ? ORDER BY timestamp DESC", (city,))
    rows = c.fetchall()
    conn.close()
    return rows
