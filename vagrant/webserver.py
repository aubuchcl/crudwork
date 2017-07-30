from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# common gateway interface used to decipher the message that was sent to the server with this module
import cgi

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
				output += "<html><body>"
				output += "Hello!"

				output += '''<form method='POST' enctype='multipart/form-data'
							 action='/hello'>
							 <h2>What would you like me to say?</h2>
							 <input name='message' type='text'>
							 <input type='submit' value='Submit'>
							 </form>'''
				output += "</body></html>"
				# use this function to send a message back to the client
				self.wfile.write(output)
				# the following is just for testing purpose in terminal
				print output
				# exit this block with a return
				return
			if self.path.endswith('/hola'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "!HOLA!<a href='/hello'>back to hello</a>"

				output += '''<form method='POST' enctype='multipart/form-data'
							 action='/hello'>
							 <h2>What would you like me to say?</h2>
							 <input name='message' type='text'>
							 <input type='submit' value='Submit'>
							 </form>'''

				output += "</body></html>"

				self.wfile.write(output)
				print output
				return

			# have your exception look for an input output error
		except IOError:
			# notify the user of the error
			self.send_error(404, "File Not Found %s" % self.path)


	def do_POST(self):
		try:
			# 301 signifies a successful post?  I think it redirects
			self.send_response(301)
			self.end_headers()

			# cgi.parser_header funciton parses an html form header such as content type, into a main value and dictionary of parameters.
			# ctype = main value and pdict is dictionary of parameters respectively
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

			# check and see if this is form data being received
			if ctype == 'multipart/form-data':
				# fields collects all the fields in a form
				fields = cgi.parse_multipart(self.rfile, pdict)
				# messagecontent gets out the value of a specific field or set of fields and stores them in an array
				messagecontent = fields.get('message')

			output = ""
			output += "<html><body>"
			output += "<h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]

			output += '''<form method='POST' enctype='multipart/form-data'
						 action='/hello'>
						 <h2>What would you like me to say?</h2>
						 <input name='message' type='text'>
						 <input type='submit' value='Submit'>
						 </form>'''

			output += "</body></html>"

			self.wfile.write(output)
			print output
			return
		except:
			pass

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
if __name__ == '__main__':
	main()