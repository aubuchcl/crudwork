from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1 ##
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB ##
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Objective 3 Step 2 - Create /restaurants/new page
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></html></body>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                # Objective 3 Step 1 - Create a Link to create a new menu item
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    # Objective 4 -- Replace Edit href

                    output += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
                    output += "</br>"
                    # Objective 5 -- Replace Delete href
                    output += "<a href ='/restaurants/%s/delete'> Delete </a>" % restaurant.id
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print 'Web server running...open localhost:8080/restaurants in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()


if __name__ == '__main__':
    main()

































# EVERYTHING BELOW THIS LINE IS THE CONTENT THAT WAS FROM THE CLASS lectures
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# # common gateway interface used to decipher the message that was sent to the server with this module
# import cgi

# class webserverHandler(BaseHTTPRequestHandler):
#   def do_GET(self):
#       # use a simpole pattern matching plan that only looks for the ending of our url path
#       try:
#           # look for the url that ends with /hello
#           if self.path.endswith('/hello'):
#               self.send_response(200)
#               # responding with html to the client
#               self.send_header('Content-type', 'text/html')
#               self.end_headers()

#               # after the response we can create some content to send back to the client
#               output = ""
#               output += "<html><body>"
#               output += "Hello!"

#               output += '''<form method='POST' enctype='multipart/form-data'
#                            action='/hello'>
#                            <h2>What would you like me to say?</h2>
#                            <input name='message' type='text'>
#                            <input type='submit' value='Submit'>
#                            </form>'''
#               output += "</body></html>"
#               # use this function to send a message back to the client
#               self.wfile.write(output)
#               # the following is just for testing purpose in terminal
#               print output
#               # exit this block with a return
#               return
#           if self.path.endswith('/hola'):
#               self.send_response(200)
#               self.send_header('Content-type', 'text/html')
#               self.end_headers()

#               output = ""
#               output += "<html><body>"
#               output += "!HOLA!<a href='/hello'>back to hello</a>"

#               output += '''<form method='POST' enctype='multipart/form-data'
#                            action='/hello'>
#                            <h2>What would you like me to say?</h2>
#                            <input name='message' type='text'>
#                            <input type='submit' value='Submit'>
#                            </form>'''

#               output += "</body></html>"

#               self.wfile.write(output)
#               print output
#               return

#           # have your exception look for an input output error
#       except IOError:
#           # notify the user of the error
#           self.send_error(404, "File Not Found %s" % self.path)


#   def do_POST(self):
#       try:
#           # 301 signifies a successful post?  I think it redirects
#           self.send_response(301)
#           self.end_headers()

#           # cgi.parser_header funciton parses an html form header such as content type, into a main value and dictionary of parameters.
#           # ctype = main value and pdict is dictionary of parameters respectively
#           ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

#           # check and see if this is form data being received
#           if ctype == 'multipart/form-data':
#               # fields collects all the fields in a form
#               fields = cgi.parse_multipart(self.rfile, pdict)
#               # messagecontent gets out the value of a specific field or set of fields and stores them in an array
#               messagecontent = fields.get('message')

#           output = ""
#           output += "<html><body>"
#           output += "<h2> Okay, how about this: </h2>"
#           output += "<h1> %s </h1>" % messagecontent[0]

#           output += '''<form method='POST' enctype='multipart/form-data'
#                        action='/hello'>
#                        <h2>What would you like me to say?</h2>
#                        <input name='message' type='text'>
#                        <input type='submit' value='Submit'>
#                        </form>'''

#           output += "</body></html>"

#           self.wfile.write(output)
#           print output
#           return
#       except:
#           pass

# def main():
#   # tries to attempt the code inside the try block
#   try:
#       port = 8080
#       # server_address is a tuple that holds the host and port number for our server -- made the server_address variable to reference the docs
#       server_address = ('', port)
#       # create an instance of my HTTPServer Class -- docs refers to this as httpd
#       server = HTTPServer(server_address, webserverHandler)
#       print "web server running on port %s" % port
#       server.serve_forever()
#   # if a defined event occurs we can exit with an exception
#   # KeyboardInterrupt is a built in exception in Python that can be triggered when the user holds control + c on the keyboard
#   except KeyboardInterrupt:
#       print "^C entered, stopping web server..."
#       server.socket.close()









# # immediately run the main methond when the Python interpreter executes my script
# if __name__ == '__main__':
#   main()