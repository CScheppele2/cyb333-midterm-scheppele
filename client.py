import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT}...")

        conn, addr = server_socket.accept()
        print(f"[SERVER] Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                print("[SERVER] Client disconnected.")
                break

            message = data.decode()
            print(f"[SERVER] Received: {message}")

            if message.lower() == "quit":
                conn.sendall("Goodbye from server.".encode())
                print("[SERVER] Closing connection.")
                break

            response = f"Server received: {message}"
            conn.sendall(response.encode())

        conn.close()

    except Exception as e:
        print(f"[SERVER ERROR] {e}")

    finally:
        server_socket.close()
        print("[SERVER] Server shut down cleanly.")

if __name__ == "__main__":
    main()
