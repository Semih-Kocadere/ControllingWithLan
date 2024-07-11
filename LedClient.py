from socket import *
import json

HOST = "{your_server_ip_address}"
PORT = 8080
BUFSIZE = 1024
server_address = (HOST,PORT)
pin = 11

def authenticate():
    user = input("Enter your username: ")
    passw = input("Enter your password: ")
    # Data to be sent
    data = {
        "username": user,
        "password": passw
    }
    # Convert data to JSON string and encode to bytes
    json_data = json.dumps(data).encode()

    client_socket.send(json_data)

    # Receive response from the server
    response = client_socket.recv(1024).decode()
    print(f"Received: {response}")

    # Process the response
    response_json = json.loads(response)
    if response_json['authenticated']:
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed:", response_json['message'])
        return False
def loop():
    while True:
        cmd = input("Input ON or OFF:")
        client_socket.send(cmd.encode())
try:
    # Create a TCP/IP socket
    client_socket = socket(AF_INET,SOCK_STREAM)

    # Connect the socket to the server
    client_socket.connect(server_address)

    if authenticate():
        loop()
except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up the connection
    if 'client_socket' in locals():
        client_socket.close()