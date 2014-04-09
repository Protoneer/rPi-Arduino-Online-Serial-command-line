import cgi
import serial

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class MyHandler(SimpleHTTPRequestHandler):
  def do_POST(self):
    print self.path 
    if self.path == '/arduino':
      form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD':'POST'})
      code = form['code'].value
      addReturnChar = form['addReturnChar'].value
      
      print 'Sent To Serial:', code

      if addReturnChar == 'true' :
        arduino.write( code + '\r')
      else :
        arduino.write(code)
      
      from time import sleep
      sleep(0.02)
      # write to file
      f = open('history.txt','a')
      
      out = ''
      while arduino.inWaiting() > 0:
        out = out + arduino.readline()
        sleep(0.02)

        #f.write(arduino.readline())
        #if addReturnChar == 'on' :
          #f.write('\r\n')
      f.write(out)
      f.close()

      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.send_header('Access-Control-Allow-Origin', '*')
      return
    return self.do_GET()

print "starting up...."
arduino = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
server = HTTPServer(('', 91), MyHandler).serve_forever()
