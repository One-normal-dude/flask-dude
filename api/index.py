from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define PostgreSQL database credentials
POSTGRES_URL = "postgres://default:6gXQN7pPjAza@ep-lingering-wave-a2ip3srb-pooler.eu-central-1.aws.neon.tech:5432/verceldb?sslmode=require"

# Connect to PostgreSQL database
def connect_to_database():
    conn = psycopg2.connect(POSTGRES_URL)
    return conn

from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define PostgreSQL database credentials
POSTGRES_URL = "postgres://default:6gXQN7pPjAza@ep-lingering-wave-a2ip3srb-pooler.eu-central-1.aws.neon.tech:5432/verceldb?sslmode=require"

# Connect to PostgreSQL database

import psycopg2
from psycopg2 import Error


def get_notes_from_db(first_name):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port",
            database="notes_db"
        )

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Query to retrieve notes for the given first name
        query = "SELECT * FROM notes WHERE first_name = %s"
        cursor.execute(query, (first_name,))

        # Fetch all the rows from the result set
        notes = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return notes

    except (Exception, Error) as error:
        print("Error while fetching notes from the database:", error)
        return []


def connect_to_database():
    conn = psycopg2.connect(POSTGRES_URL)
    return conn

# Authentication function
def authenticate(username, password):
    # Your authentication logic here
    # Example: Query database to validate credentials
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Define routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = authenticate(username, password)

    if user:
        session['username'] = username
        session['access_level'] = user[2]  # Assuming access level is stored in the third column
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        access_level = session.get('access_level')
        if access_level == 'GREEN':
            return redirect(url_for('view_notes'))
        elif access_level == 'ORANGE':
            return render_template('orange_dashboard.html', username=session['username'])
        elif access_level == 'RED':
            return render_template('red_dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('access_level', None)
    return redirect(url_for('index'))

@app.route('/notes')
def view_notes():
    if 'username' in session and session['access_level'] == 'GREEN':
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM note')
        notes = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('notes.html', notes=notes)
    return redirect(url_for('index'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        first_name = request.form['first_name']
        type = request.form['type']
        description = request.form['description']

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO note (first_name, type, description) VALUES (%s, %s, %s)', (first_name, type, description))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))
    else:
        return render_template('add_note.html')

if __name__ == '__main__':
    app.run(debug=True)


# Authentication function
def authenticate(username, password):
    # Your authentication logic here
    # Example: Query database to validate credentials
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Define routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = authenticate(username, password)

    if user:
        session['username'] = username
        session['access_level'] = user[2]  # Assuming access level is stored in the third column
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        access_level = session.get('access_level')
        if access_level == 'GREEN':
            return redirect(url_for('view_notes'))
        elif access_level == 'ORANGE':
            return render_template('orange_dashboard.html', username=session['username'])
        elif access_level == 'RED':
            return render_template('red_dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('access_level', None)
    return redirect(url_for('index'))

@app.route('/notes')
def view_notes():
    if 'username' in session and session['access_level'] == 'GREEN':
        # Retrieve notes from the database for the current user
        first_name = session['first_name']
        notes = get_notes_from_db(first_name)
        return render_template('notes.html', notes=notes)
    else:
        return redirect(url_for('index'))


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        first_name = request.form['first_name']
        type = request.form['type']
        description = request.form['description']

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO note (first_name, type, description) VALUES (%s, %s, %s)', (first_name, type, description))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))
    else:
        return render_template('add_note.html')

if __name__ == '__main__':
    app.run(debug=True)










