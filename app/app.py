import os
import psycopg2
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Database connection setup
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mysecretpassword')
DB_NAME = os.environ.get('DB_NAME', 'votingapp')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    return conn

# HTML template for the voting page
VOTE_TEMPLATE = """
<!doctype html>
<html>
<head><title>Oylama Uygulaması</title></head>
<body>
    <h1>Cats vs. Dogs</h1>
    <form method="post" action="{{ url_for('vote') }}">
        <button type="submit" name="vote" value="cats">Cats</button>
        <button type="submit" name="vote" value="dogs">Dogs</button>
    </form>
    <h2>Results:</h2>
    <ul>
        <li>Cats: {{ cat_votes }}</li>
        <li>Dogs: {{ dog_votes }}</li>
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS votes (id serial PRIMARY KEY, choice VARCHAR(50));")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM votes WHERE choice = 'cats';")
    cat_votes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM votes WHERE choice = 'dogs';")
    dog_votes = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template_string(VOTE_TEMPLATE, cat_votes=cat_votes, dog_votes=dog_votes)

@app.route('/vote', methods=['POST'])
def vote():
    vote_choice = request.form['vote']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO votes (choice) VALUES (%s);", (vote_choice,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)