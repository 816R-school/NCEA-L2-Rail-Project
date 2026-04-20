import sqlite3

def init_db():
    conn = sqlite3.connect('rail_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lines (
            line_id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_name TEXT NOT NULL,
            color_code TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            station_id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_id INTEGER,
            station_name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (line_id) REFERENCES lines (line_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facilities (
            facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id INTEGER,
            facility_type TEXT NOT NULL,
            is_operational INTEGER DEFAULT 1,
            FOREIGN KEY (station_id) REFERENCES stations (station_id)
        )
    ''')

    lines = [('Eastern Line', '#FFD700'), ('Western Line', '#008000')]
    cursor.executemany('INSERT INTO lines (line_name, color_code) VALUES (?, ?)', lines)

    stations = [
        (1, 'Britomart', 'Central transport hub in Auckland CBD.'),
        (2, 'Newmarket', 'Key junction for western and southern routes.')
    ]
    cursor.executemany('INSERT INTO stations (line_id, station_name, description) VALUES (?, ?, ?)', stations)

    facilities = [
        (1, 'Elevator', 1),
        (1, 'Ticket Machine', 1),
        (2, 'Elevator', 1),
        (2, 'Parking', 0)
    ]
    cursor.executemany('INSERT INTO facilities (station_id, facility_type, is_operational) VALUES (?, ?, ?)', facilities)

    conn.commit()
    conn.close()
    print("Database created.")

if __name__ == '__main__':
    init_db()