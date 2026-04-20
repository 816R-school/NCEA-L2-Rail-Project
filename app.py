from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('rail_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    query = '''
        SELECT stations.station_name, stations.description, lines.line_name, lines.color_code
        FROM stations
        JOIN lines ON stations.line_id = lines.line_id
    '''
    stations = conn.execute(query).fetchall()
    conn.close()
    return render_template('index.html', stations=stations)

if __name__ == '__main__':
    app.run(debug=True)