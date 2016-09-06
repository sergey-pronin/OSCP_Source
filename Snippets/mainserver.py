#!/usr/bin/python
import select 
import socket 
import sys 
import threading
import logging 
import traceback
import gc
import nmb.NetBIOS
import os
import glob
import json

HOST=HOST
PORT=int(PORT)

class Server: 
	def __init__(self): 
		self.host = HOST 
		self.port = PORT 
		#self.backlog = 5 
		self.size = 1024 
		self.server = None 
		self.threads = []
		self.first = True

	def open_socket(self):
		try: 
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.settimeout(3)
			self.server.bind((self.host,self.port)) 
			self.server.listen(5) 
		except socket.error, (value,message): 
			if self.server: 
				self.server.close()
			print message		
			sys.exit(1) 

	def run(self):
		self.open_socket()
		
		input = [self.server,sys.stdin] 
		running = 1 
		while running:
			#Check if thread isAlive, else remove if queue > 100 threads			
			if len(self.threads) > 100:
				for t in self.threads:
					if not t.isAlive():
						self.threads.remove(t)
						 
			inputready,outputready,exceptready = select.select(input,[],[])
			for s in inputready: 
				json_check = glob.glob("json/*.json")
				if json_check != json_files:
					for json_file in json_check:
						if json_file not in json_files:
							with open(json_file) as f:
								try:
									malware_list += json.load(f)
								except Exception, e:
									print str(e)
									print "Incorrect json format!"
							json_files.append(json_file)
				if s == self.server: 
					# handle the server socket
					c = Client(self.server.accept(), malware_list) 
					c.start() 
					self.threads.append(c) 
				elif s == sys.stdin: 
					# handle standard input 
					junk = sys.stdin.readline() 
					if junk == 'q\n':
						running = 0

		# close all threads 

		self.server.close() 
		for c in self.threads: 
			c.join()

	
class Client(threading.Thread): 
	def __init__(self,(client,address), malware_list): 
		threading.Thread.__init__(self) 
		self.client = client
		self.address = address
		self.revip=""
		self.nmbname = ""
		self.nmb = nmb.NetBIOS.NetBIOS()
		self.malware_list = malware_list 
 
		src=self.address[0]
		try:
				self.revip = str(socket.gethostbyaddr(src)[0])
				logging.debug("Reversed IP:"+str(src))
		except:
				logging.debug("Reverse IP exception for "+str(src))
				self.revip = ""
				pass 
		#try:
	#			self.nmbname= self.nmb.queryIPForName(str(src).strip(),timeout=2)[0]
#				logging.debug("NMB lookup:"+str(self.nmbname))
#		except Exception,e:
#				logging.debug("NMB lookup exception for "+str(src)+"-"+str(e))
#				self.nmbname = "" 
#				pass
		self.size = 2048
		self.data = "" 

	def run(self): 
		running = 1 
		logging.debug("Creating DetectVariant class")
		detect = DetectVariant(self.client, self.malware_list)
		while running:
			data = None
			ready = select.select([self.client], [], [], 5)
			try:
				if ready[0]:
					#if True:
					try:
						self.data = self.client.recv(self.size)
						#self.data = repr(myself.data)
						logging.debug("Received "+str(self.data))
					except Exception, e:
						logging.debug("Exception on recv from "+self.address[0])
						print str(e)
						print traceback.format_exc()
						self.client.close()
						running=0
					
				if self.data:
					store = DBStore()
					try:
						# Detect malware variant
						detected = detect.fingerprint(self.data)
						logging.debug("Detected:" + detected)
						logging.debug("Values "+self.address[0]+" :" + str(detect.values))
						# Store parsed malware values in database
						logging.debug("Storing session in database")
						store.insert(self,detect)
						self.data=None
						del store
					except Exception, e:
						logging.error("Error in detection code")
						logging.error(traceback.format_exc())
						print str(e)
						print traceback.format_exc()
						del store
						pass
					
				
					# Check if client is scheduled for cleanup and send cleanup command
					if detect.cleanup == 1 or AUTOCLEANUP == "1":
						logging.info("Cleaning up, sending: "+str(detect.cleanupcommand))
						self.client.send(detect.cleanupcommand)
					else:
						self.client.send(detect.normalcommand)
								
					self.client.close()
					running = 0
				else: 
					self.client.close() 
					running = 0 
			except Exception, e:
					print str(e)
					print traceback.format_exc()
					self.client.close()
					logging.warning(str(e))
					logging.error(traceback.format_exc())
					del detect
					running=0

if __name__ == "__main__": 
	s = Server() 
	s.run()
