from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__, static_folder='static')

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registerbtn')
def registerbtn():
    return render_template('register.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
             conn = sqlite3.connect('developers.db')
             c = conn.cursor()
             
             userName = request.form['username']
             email = request.form['email']
             password: str = request.form['password']
             
             c.execute("INSERT INTO developers (username, email, password) VALUES (?, ?, ?)", (userName, email, password))
             conn.commit()
             conn.close()
             return (f"Registration successful for user: {userName}, email: {email}")
    return redirect(url_for('registerbtn'))

@app.route('/developers')
def developers():
    conn = sqlite3.connect('developers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM developers")
    developers = c.fetchall()
    conn.close()
    return render_template('index1.html', developers=developers)
if __name__ == '__main__':
    app.run(debug=True)