from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from database import init_db, add_user, get_user, update_active_status, count_active_users

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key for session handling

# Initialize the database
init_db()

# Homepage route
@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', username=session['username'], active_users=count_active_users())
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Get user from DB
        user = get_user(username)
        if user and user[2] == password:  # user[2] is the password field in DB
            session['username'] = username
            update_active_status(username, 1)  # Set active status to 1 (logged in)
            return redirect(url_for('index'))
        else:
            return "Invalid credentials, please try again."

    return render_template('index.html')

# Logout route
@app.route('/logout')
def logout():
    if 'username' in session:
        update_active_status(session['username'], 0)  # Set active status to 0 (logged out)
        session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
