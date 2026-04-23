from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('rail_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stations')
def stations():
    line_id = request.args.get('line')
    search_query = request.args.get('search')
    conn = get_db_connection()
    
    query = '''
        SELECT s.*, l.line_name, l.color_code, f.has_elevator, f.has_parking
        FROM stations s
        JOIN lines l ON s.line_id = l.line_id
        LEFT JOIN facilities f ON s.station_id = f.station_id
        WHERE 1=1
    '''
    params = []

    if line_id and line_id.strip():
        query += ' AND s.line_id = ?'
        params.append(line_id)

    if search_query and search_query.strip():
        query += ' AND s.station_name LIKE ?'
        params.append(f'%{search_query}%')
        
    stations_data = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('stations.html', stations=stations_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/station/<int:station_id>')
def station_details(station_id):
    conn = get_db_connection()
    station = conn.execute('''
        SELECT s.*, l.line_name, l.color_code, f.has_elevator, f.has_parking
        FROM stations s
        JOIN lines l ON s.line_id = l.line_id
        LEFT JOIN facilities f ON s.station_id = f.station_id
        WHERE s.station_id = ?
    ''', (station_id,)).fetchone()
    conn.close()
    return render_template('details.html', station=station)

if __name__ == '__main__':
    app.run(debug=True)