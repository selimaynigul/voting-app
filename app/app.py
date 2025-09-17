import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Database connection setup
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    return conn

def get_votes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM votes WHERE choice = 'messi';")
    messi_votes = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM votes WHERE choice = 'ronaldo';")
    ronaldo_votes = cur.fetchone()[0]
    cur.close()
    conn.close()
    return messi_votes, ronaldo_votes

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS votes (id serial PRIMARY KEY, choice VARCHAR(50));")
    conn.commit()
    cur.close()
    conn.close()
    messi_votes, ronaldo_votes = get_votes()
    return render_template('index.html', messi_votes=messi_votes, ronaldo_votes=ronaldo_votes)

@app.route('/vote', methods=['POST'])
def vote():
    vote_choice = request.json.get('vote')
    
    if vote_choice not in ['messi', 'ronaldo']:
        return jsonify({'status': 'error', 'message': 'Invalid vote'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO votes (choice) VALUES (%s);", (vote_choice,))
    conn.commit()
    cur.close()
    conn.close()
    
    # after voting, return the updated vote counts
    messi_votes, ronaldo_votes = get_votes()
    return jsonify({'status': 'success', 'messi_votes': messi_votes, 'ronaldo_votes': ronaldo_votes})

@app.route('/healthz')
def healthz():
    try:
        conn = get_db_connection()
        conn.close()
        return "OK", 200
    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return "Not OK", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)