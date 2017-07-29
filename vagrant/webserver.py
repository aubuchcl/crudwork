from BaseHTTPServer import BaseHTTPRequestHandler, BaseHTTPServer


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		# use a simpole pattern matching plan that only looks for the ending of our url path
		try:
			# look for the url that ends with /hello
			if self.path.endswith('/hello'):
				self.send_response(200)
				# responding with html to the client
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				# after the response we can create some content to send back to the client
				output = ""
				output += "<html><body>Hello!</body></html>"

				# use this function to send a message back to the client
				self.wfile.write(output)
				# the following is just for testing purpose in terminal
				print output
				# exit this block with a return
				return

			# have your exception look for an input output error
		except IOError:
			# notify the user of the error
			self.send_error(404, "File Not Found %s" % self.path)


def main():
	# tries to attempt the code inside the try block
	try:
		port = 8080
		# server_address is a tuple that holds the host and port number for our server -- made the server_address variable to reference the docs
		server_address = ('', port)
		# create an instance of my HTTPServer Class -- docs refers to this as httpd
		server = HTTPServer(server_address, webserverHandler)
		print "web server running on port %s" % port
		server.serve_forever()
	# if a defined event occurs we can exit with an exception
	# KeyboardInterrupt is a built in exception in Python that can be triggered when the user holds control + c on the keyboard
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()









# immediately run the main methond when the Python interpreter executes my script
if __name__ = '__main__'
	main()