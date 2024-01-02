import socket
from PIL import Image
import io

# Function to send image data to the client
def send_image_data(conn, image_path):
    # Load the image
    image = Image.open(image_path)

    # Convert image to bytes
    image_bytes = image.tobytes()

    # Send the size of the image data first
    conn.sendall(len(image_bytes).to_bytes(4, byteorder='big'))

    # Send image bytes to the client
    conn.sendall(image_bytes)

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 4455))
server_socket.listen(1)

print("Server listening on port 12345")

while True:
    # Accept a connection
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Send image data to the client
    send_image_data(conn, "/storage/emulated/0/Log.jpg")

    # Close the connection
    conn.close()
