from socket import *
from time import ctime
import RPi.GPIO as GPIO
import json

HOST = ""
PORT = 8080
BUFSIZE = 1024
server_address = (HOST, PORT)
Username = "admin"
Password = "12345"
# IPV4 ailesi ve TCP tipinde bir soket olusturur.
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

pin = 11


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def Led():
    while True:
        data = client_socket.recv(BUFSIZE).decode("utf-8").strip()
        if not data:
            break
        if data == "ON":
            GPIO.output(pin, GPIO.LOW)
            print("Led on")
        elif data == "OFF":
            GPIO.output(pin, GPIO.HIGH)
            print("Led off")
        else:
            print("error!")
    server_socket.close()


# Define a function to handle client connections
def handle_client_connection(client_socket):
    # Receive data from the client
    data = client_socket.recv(1024).decode()
    try:
        json_data = json.loads(data)
        username = json_data.get('username')
        password = json_data.get('password')

        # Example password check
        if username == Username and password == Password:
            response = {'authenticated': True, 'message': 'Authentication successful!'}
        else:
            response = {'authenticated': False, 'message': 'Invalid authorization!'}

        # Send response back to client
        client_socket.sendall(json.dumps(response).encode())

        if response['authenticated']:
            print("Successfully connected.")
            setup()
            Led()


    except json.JSONDecodeError:
        response = {'authenticated': False, 'message': 'Invalid JSON format.'}
        client_socket.sendall(json.dumps(response).encode())

    finally:
        # Clean up the connection
        client_socket.close()


while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Handle client connection in a separate thread or function
    handle_client_connection(client_socket)