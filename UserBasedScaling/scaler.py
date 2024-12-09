from flask import Flask, request

app = Flask(__name__)

@app.route('/active_users', methods=['POST'])
def receive_active_user_count():
    active_users = request.data.decode()  # Get the active user count from the request body
    print(f"Received active user count: {active_users}")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
