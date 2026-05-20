# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = "neym_secret_key" # Required for flashing messages
app.permanent_session_lifetime = timedelta(days=30) # Remember users for 30 days

# MongoDB setup
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['portfolio']
developers_collection = db['developers']

# Page Routes

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('developers'))
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

# Logic Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            userName = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                return "Passwords do not match! <a href='/registerbtn'>Try again</a>"

            # Check if user exists
            if developers_collection.find_one({'username': userName}):
                return "Username already exists! <a href='/registerbtn'>Try again</a>"
            
            if developers_collection.find_one({'email': email}):
                return "Email already exists! <a href='/registerbtn'>Try again</a>"

            developers_collection.insert_one({
                'username': userName,
                'email': email,
                'password': password
            })
            return redirect(url_for('loginbtn'))
        except Exception as e:
            return f"An error occurred: {e}"
    
    # If someone types /register in browser, redirect to the actual form page
    return redirect(url_for('registerbtn'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            userName = request.form['username']
            password = request.form['password']
            
            user = developers_collection.find_one({'username': userName, 'password': password})
            
            if user:
                session.permanent = True
                session['username'] = user['username']
                return redirect(url_for('developers'))
            else:
                return "Invalid Credentials. <a href='/loginbtn'>Go back</a>"
        except Exception as e:
            return f"An error occurred: {e}"
            
    # If someone types /login in browser, redirect to the actual form page
    return redirect(url_for('loginbtn'))

@app.route('/developers')
def developers():
    if 'username' not in session:
        return redirect(url_for('loginbtn'))
    username = session.get('username')
    return render_template('index1.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/change_username', methods=['GET', 'POST'])
def change_username():
    if 'username' not in session:
        return redirect(url_for('loginbtn'))
        
    if request.method == 'POST':
        try:
            new_username = request.form['new_username']
            password = request.form['password']
            current_username = session['username']
            
            user = developers_collection.find_one({'username': current_username, 'password': password})
            if user:
                if developers_collection.find_one({'username': new_username}):
                    return "Username already taken! <a href='/change_username'>Try again</a>"
                    
                developers_collection.update_one({'username': current_username}, {'$set': {'username': new_username}})
                session['username'] = new_username
                return redirect(url_for('developers'))
            else:
                return "Incorrect password. <a href='/change_username'>Try again</a>"
        except Exception as e:
            return f"An error occurred: {e}"
            
    return render_template('change_username.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('loginbtn'))
        
    if request.method == 'POST':
        try:
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            current_username = session['username']
            
            if new_password != confirm_password:
                return "New passwords do not match! <a href='/change_password'>Try again</a>"
                
            user = developers_collection.find_one({'username': current_username, 'password': current_password})
            if user:
                developers_collection.update_one({'username': current_username}, {'$set': {'password': new_password}})
                return redirect(url_for('developers'))
            else:
                return "Incorrect current password. <a href='/change_password'>Try again</a>"
        except Exception as e:
            return f"An error occurred: {e}"
            
    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True)