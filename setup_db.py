import sqlite3

def init_db():
    conn = sqlite3.connect('rail_data.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS facilities')
    cursor.execute('DROP TABLE IF EXISTS stations')
    cursor.execute('DROP TABLE IF EXISTS lines')

    cursor.execute('''
        CREATE TABLE lines (
            line_id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_name TEXT NOT NULL,
            color_code TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE stations (
            station_id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_id INTEGER,
            station_name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (line_id) REFERENCES lines (line_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE facilities (
            facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id INTEGER,
            has_elevator INTEGER DEFAULT 0,
            has_parking INTEGER DEFAULT 0,
            FOREIGN KEY (station_id) REFERENCES stations (station_id)
        )
    ''')

    lines = [('Eastern Line', '#FDB913'), ('Western Line', '#97C93D'), ('Southern Line', '#EE2E27'),('Onehunga Line', '#00AEEF')]
    cursor.executemany('INSERT INTO lines (line_name, color_code) VALUES (?, ?)', lines)

    stations = [
        (1, 'Britomart', 'Central transport hub in Auckland CBD.'),
        (2, 'Newmarket', 'Key junction for western and southern routes.'),
        (1, 'Panmure', 'Major interchange for bus and train services.'),
        (3, 'Manukau', 'Key station for Southern line passengers.')
    ]
    cursor.executemany('INSERT INTO stations (line_id, station_name, description) VALUES (?, ?, ?)', stations)

    facilities = [
        (1, 1, 0),
        (2, 1, 0),
        (3, 1, 1),
        (4, 1, 1)
    ]
    cursor.executemany('INSERT INTO facilities (station_id, has_elevator, has_parking) VALUES (?, ?, ?)', facilities)

    conn.commit()
    conn.close()
    print("Database 'rail_data.db' created successfully!")

if __name__ == '__main__':
    init_db()