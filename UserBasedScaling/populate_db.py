import sqlite3
import random
import string

# Function to generate a random username
def generate_username(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Function to generate a random password
def generate_password(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

def populate_db(num_users=1000):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Insert users into the database with active status set to 0 (False)
    for _ in range(num_users):
        username = generate_username()
        password = generate_password()

        cursor.execute('''
        INSERT INTO users (username, password, active) VALUES (?, ?, ?)
        ''', (username, password, 0))  # 0 for False (not logged in)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print(f"{num_users} users populated successfully.")

if __name__ == "__main__":
    populate_db(1000)
