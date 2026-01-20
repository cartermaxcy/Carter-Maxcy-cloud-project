from flask import Flask, request
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return f"Response from Server 2 (Hostname: {socket.gethostname()})"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)