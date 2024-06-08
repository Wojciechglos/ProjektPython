import sqlite3

def create_database():
    conn = sqlite3.connect('baza_gios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dane
                 (id INTEGER PRIMARY KEY, city TEXT, param_name TEXT, value REAL, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_data(city, param_name, value, timestamp):
    conn = sqlite3.connect('baza_gios.db')
    c = conn.cursor()
    c.execute("INSERT INTO dane (city, param_name, value, timestamp) VALUES (?, ?, ?, ?)", (city, param_name, value, timestamp))
    conn.commit()
    conn.close()

def Dane(city):
    conn = sqlite3.connect('baza_gios.db')
    c = conn.cursor()
    c.execute("SELECT * FROM dane WHERE city = ? ORDER BY timestamp DESC", (city,))
    rows = c.fetchall()
    conn.close()
    return rows
