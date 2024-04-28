from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define users and their clearance levels
users = {
    "maksim.mohl@mik.hr": {"password": "cQ5YAj93", "access_level": "GREEN"},
    "filip.sutlar@mik.hr": {"password": "9W3GSe5n", "access_level": "GREEN"},
    # Add more users here
    "leon.antonio.knezevic@mik.hr": {"password": "cb4XPR6c", "access_level": "RED"},
    "marin.drabic@udruga-mis.hr": {"password": "ZG39b5Qo", "access_level": "RED"}
}

# Connect to the SQLite database
conn = sqlite3.connect('../../flask-dude/api/notes.db')
c = conn.cursor()

# Create the note table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS note
             (id INTEGER PRIMARY KEY,
              first_name TEXT,
              type TEXT,
              description TEXT)''')

# Commit changes and close the connection
conn.commit()
conn.close()


# Define routes
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['access_level'] = users[username]['access_level']
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid username or password")


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        access_level = session['access_level']
        if access_level == 'GREEN':
            # Redirect to the 'view_notes' endpoint instead of 'notes'
            return redirect(url_for('view_notes'))
        elif access_level == 'ORANGE':
            # Render dashboard for ORANGE access level
            return render_template('orange_dashboard.html', username=session['username'])
        elif access_level == 'RED':
            # Render dashboard for RED access level
            return render_template('red_dashboard.html', username=session['username'])
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('access_level', None)
    return redirect(url_for('index'))


@app.route('/notes')
def view_notes():
    if 'username' in session and session['access_level'] == 'GREEN':
        # Retrieve notes from the database
        conn = sqlite3.connect('../../flask-dude/api/notes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM note')
        notes = c.fetchall()
        conn.close()
        return render_template('notes.html', notes=notes)
    else:
        return redirect(url_for('index'))


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        first_name = request.form['first_name']
        type = request.form['type']
        description = request.form['description']

        # Connect to the SQLite database
        conn = sqlite3.connect('../../flask-dude/api/notes.db')
        c = conn.cursor()

        # Insert a new note into the database
        c.execute('INSERT INTO note (first_name, type, description) VALUES (?, ?, ?)', (first_name, type, description))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))
    else:
        # Render the form to add a new note
        return render_template('add_note.html')




