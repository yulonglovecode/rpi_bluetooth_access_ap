#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
import os
import time


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)

PORT_NUMBER = 8080
abspath = '/home/pi/gpf'
# This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype = 'image/png'
                sendReply = True

            if sendReply == True:
                # Open the static file requested and send it
                f = open(abspath + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                text = f.read()
                self.wfile.write(str.encode(text))
                f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)



    # Handler for the POST requests
    def do_POST(self):
        print("POST received")
        if self.path == "/send":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })

            ssid = form["wifi_name"].value
            psk = form["wifi_pass"].value

            wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
            with open(wpa_supplicant_conf, 'a+') as f:
                config_lines = ['\n',
                            'network={',
                            '\tssid="{}"'.format(ssid),
                            '\tpsk="{}"'.format(psk),
                            '\tkey_mgmt=WPA-PSK', '}']
                config = '\n'.join(config_lines)
                print(config)
                f.write(config)
            self.send_response(200)
            self.end_headers()
            text2 = "Thanks! The device is reconfiguring itself with network:%s. You may close the browser " %form["wifi_name"].value
            self.wfile.write(str.encode(text2))
            # global condition_server
            # condition_server = True
            GPIO.output(12,GPIO.LOW)
            os.system('sudo cp -rf /etc/dhcpcd_wifi.ap /etc/dhcpcd.conf')
            os.system('sudo systemctl stop dnsmasq.service')
            os.system('sudo systemctl stop hostapd.service ')
            os.system('sudo systemctl restart dhcpcd.service')
            os.system('wpa_cli -i wlan0 reconfigure')
            #os.system('sudo reboot now')


# if __name__ == "__main__":
#     server = HTTPServer(('', PORT_NUMBER), myHandler)
#     print('Started httpserver on port ', PORT_NUMBER)
#     try:
#             # Create a web server and define the handler to manage the
#             # incoming request
#         # Wait forever for incoming http requests
#         server.serve_forever()
#         print('^C received, shutting down the web server')
#
#
#     except KeyboardInterrupt:
#         server.socket.close()
