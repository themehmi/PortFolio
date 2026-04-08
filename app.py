from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__, static_folder='static')
app.secret_key = "neym_secret_key" # Required for flashing messages

def init_db():
    conn = sqlite3.connect('developers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS developers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  email TEXT NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# --- Page Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/registerbtn')
def registerbtn():
    return render_template('register.html')

@app.route('/loginbtn')
def loginbtn():
    return render_template('login.html')

# --- Logic Routes ---

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        userName = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match! <a href='/registerbtn'>Try again</a>"

        conn = sqlite3.connect('developers.db')
        c = conn.cursor()
        c.execute("INSERT INTO developers (username, email, password) VALUES (?, ?, ?)", 
                  (userName, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('loginbtn'))
    
    return redirect(url_for('registerbtn'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('developers.db')
        c = conn.cursor()
        c.execute("SELECT * FROM developers WHERE username = ? AND password = ?", (userName, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            # Successful login - redirect to developers list
            return redirect(url_for('developers'))
        else:
            return "Invalid Credentials. <a href='/loginbtn'>Go back</a>"
            
    return redirect(url_for('loginbtn'))

@app.route('/developers')
def developers():
    conn = sqlite3.connect('developers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM developers")
    dev_list = c.fetchall()
    conn.close()
    return render_template('index1.html', developers=dev_list)

if __name__ == '__main__':
    app.run(debug=True)
