import socket
import random

HOST = '127.0.0.1'
PORT = 65432

# Create the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is waiting for a client to connect...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        # Generate a random number between 1 and 10
        target = random.randint(1, 10)
        attempts = 3

        for i in range(attempts):
            conn.sendall(f"Attempt {i+1}: Guess a number between 1 and 10\n".encode())
            data = conn.recv(1024).decode().strip()

            if not data:
                break

            try:
                guess = int(data)
            except ValueError:
                conn.sendall("Invalid input. Please send a number.\n".encode())
                continue

            if guess == target:
                conn.sendall("🎉 Correct! You guessed the number!\n".encode())
                break
            elif guess < target:
                conn.sendall("Too low.\n".encode())
            else:
                conn.sendall("Too high.\n".encode())

        else:
            # If all attempts used and no correct guess
            conn.sendall(f"❌ Game over. The correct number was {target}.\n".encode())

        print("Game ended with client.")
