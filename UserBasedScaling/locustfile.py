import random
import sqlite3
import requests
from locust import HttpUser, task, between, events

# Database connection (change this based on your database)
def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Fetch a random user credential from the database
def get_random_user_credentials():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users LIMIT 1000")  # Adjust the query as per your schema
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return random.choice(users)

# Send active user count via HTTP POST
def send_active_user_count(active_users):
    response = requests.post("http://localhost:5001/active_users", data=str(active_users))
    print(f"Sent active user count: {active_users}, Response: {response.status_code}")

class UserBehavior(HttpUser):
    wait_time = between(1, 20)  # Random wait time between tasks (1-20 seconds)

    # On start, get a random user credential
    def on_start(self):
        self.username, self.password = get_random_user_credentials()

    @task
    def login(self):
        response = self.client.post(
            "http://localhost:5000/login",  # Replace with your login endpoint
            data={"username": self.username, "password": self.password}
        )
        if response.status_code == 200 and "Welcome" in response.text:
            print(f"User {self.username} logged in successfully.")
        else:
            print(f"Login failed for {self.username}.")
    
    @task(3)  # Simulating browsing after login with a weight of 3
    def browse_dashboard(self):
        self.client.get("http://localhost:5000")  # Replace with a page your users would access after logging in

    def on_stop(self):
        pass

# Track active users programmatically and send data via HTTP
@events.tick.add_listener
def on_tick():
    active_users = len(events._active_users)  # List of active users
    print(f"Active users: {active_users}")
    send_active_user_count(active_users)
