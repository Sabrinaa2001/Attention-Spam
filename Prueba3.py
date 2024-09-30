import socket

# Configuración del servidor
server_ip = '127.0.0.1'  # Cambia esto a la dirección IP del servidor
server_port = 12345
# Crear un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectar al servidor
client_socket.connect((server_ip, server_port))
# Enviar datos al servidor
message = "Hola desde Python"
client_socket.sendall(message.encode())
# Recibir datos del servidor
data = client_socket.recv(1024)
print('Mensaje del servidor:', data.decode())
# Cerrar el socket
client_socket.close()
