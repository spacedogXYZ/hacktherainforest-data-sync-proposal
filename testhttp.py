#!/usr/bin/python

import threading #Know Whats going on in the server
import random #generate some pseudo randoms
import hashlib #hash the randoms for directories and security
import sys #pass the file

import BaseHTTPServer #Server
import SocketServer #Server


#Generating random path for showing hashes
def getrandompath():
	strings = "abcdefghijklmnopqrtuvwxyz"
	nums = "1234567890"
	alts = "!\"#$%&/()=?@"
	s1 = random.choice(strings)
	s2 = random.choice(strings)
	s3 = random.choice(strings)
	s4 = random.choice(strings)
	s5 = random.choice(strings)
	s6 = random.choice(strings)
	s7 = random.choice(strings)
	s8 = random.choice(strings)
	s9 = random.choice(strings)
	s10 = random.choice(strings)
	n1 = random.choice(nums)
	n2 = random.choice(nums)
	n3 = random.choice(nums)
	n4 = random.choice(nums)
	n5 = random.choice(nums)
	a1 = random.choice(alts)
	a2 = random.choice(alts)
	a3 = random.choice(alts)
	a4 = random.choice(alts)
	a5 = random.choice(alts)
	
	tohash = s1 + n1 + s2 + s3 + a1 + s4 + s5 + a2 + s6 + s7 + a3 + s8 + n2 + a4 + n3 + s9 + n4 + s10 + a5 + n5
	return hashlib.sha256(tohash).hexdigest()

localhashdir = sys.argv[1]

randomize = "/" + getrandompath() #Adding the / to make it path


#Define HTTPSERVER Class
class HTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	def __init__(self, server_address):
		SocketServer.TCPServer.__init__(self, server_address, HTTPHandler)

#Define HTTP Handler    
class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self): 
		if self.path == "/":
			response = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hey!</title>
</head>
<body>
<center><h1>This Works</h1></center><br /><a href="
""" + randomize + "\">Hashes</a></body></html>"
   
			self.send_response(200)
			self.send_header("Content-Length", str(len(response)))
			self.send_header("Cache-Control", "no-store")
			self.end_headers()
			self.wfile.write(response)

		elif self.path[:65] == randomize:
			count = 0
			with open(localhashdir) as hashfile:
				hashlines = []
				for line in hashfile:
					count = count + len(line)
					hashlines.append(line)
			response = hashlines
			self.send_response(200)
			self.send_header("Content-Length", str(count))
			self.send_header("Cache-Control", "no-store")
			self.end_headers()
			self.wfile.write(response)    

		else:
			self.send_error(404, "What Are you trying?")
			self.end_headers()


#When Running the script
if __name__ == '__main__':
  
	print "HackTheRainforest"

	def quit(signum, frame):
		print "Quitting..."
		sys.exit(0)

	http_server = HTTPServer(server_address=("",1337)) #Define where the http server will be
  	http_server_thread = threading.Thread(target=
                                       http_server.serve_forever()) #Show server events
	http_server_thread.setDaemon(true) #Start Daemon Eventshowing
	http_server_thread.start() #Start the event showing
  
	try:
		while True:
			http_server_thread.join(60)
	except KeyboardInterrupt:
		quit()
