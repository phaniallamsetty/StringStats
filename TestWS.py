#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import urlparse
import sys

PORT_NUMBER = 8080

def CharCount(a):
  k = len(a)
  return k

def SpaceCount(a):
  k = a.count(' ')
  return k

def UpperCount(a):
  k = sum(1 for c in a if c.isupper())
  return k

def LowerCount(a):
  k = sum(1 for c in a if c.islower())
  return k

  
#This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):

#Handler for the GET requests
  def do_GET(self):
    if self.path.startswith("/TextStats"):
      o = urlparse.urlparse(self.path)
      getvars = urlparse.parse_qs(o.query)
      try:
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        a = getvars['intext'][0]
        self.wfile.write("{")
        self.wfile.write("NumberOfCharacters : ")
        self.wfile.write(json.dumps(CharCount(a)))
        self.wfile.write(", ")
        self.wfile.write("NumberOfSpaces : ")
        self.wfile.write(json.dumps(SpaceCount(a)))
        self.wfile.write(", ")
        self.wfile.write("NumberOfUpperCaseChars : ")
        self.wfile.write(json.dumps(UpperCount(a)))
        self.wfile.write(", ")
        self.wfile.write("NumberOfLowerCaseChars : ")
        self.wfile.write(json.dumps(LowerCount(a)))
        self.wfile.write("}")
        return
      except:
        e = sys.exc_info()[0]
        self.send_error(404,'Error, provide a and b parameters' + str(e) + str(getvars.keys()))
        return
    self.send_error(404,'Resource Not Found')

if __name__ == "__main__":
  try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

#Wait forever for incoming http requests
    server.serve_forever()

  except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
