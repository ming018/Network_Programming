import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 10000))
s.listen(1)

client, addr = s.accept()
print(client.recv(1024).decode())
