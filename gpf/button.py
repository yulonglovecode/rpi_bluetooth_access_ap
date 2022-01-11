from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
import time
import os
import httpserver_2 as web_server


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12,GPIO.OUT)
state = False

GPIO.output(12,GPIO.LOW)

time.sleep(5)


while True:
	input_state = GPIO.input(18)
	if input_state == False:
		if state == False:
			print('Turning on WIFI configurator')
			os.system('sudo cp -rf /etc/dhcpcd_nonwifi.ap /etc/dhcpcd.conf')
			os.system('sudo systemctl restart dhcpcd.service')
			os.system('sudo systemctl start dnsmasq.service')
			os.system('sudo systemctl start hostapd.service')
			GPIO.output(12,GPIO.HIGH)
			#os.system('sudo python3 /home/pi/gpf/httpserver_2.py')
			os.system('sudo cp -rf /etc/dhcpcd_wifi.ap /etc/dhcpcd.conf')
			server = HTTPServer(('', web_server.PORT_NUMBER), web_server.myHandler)
			try:
				server.serve_forever()
			except KeyboardInterrupt:
				pass


			server.socket.close()



			# while condition_server :
			# 	server= HTTPServer(('', web_server.PORT_NUMBER), web_server.myHandler)
			# 	print('Started httpserver on port ', web_server.PORT_NUMBER)
			# 	try:
			# 		# Create a web server and define the handler to manage the
			# 		# incoming request
			# 		# Wait forever for incoming http requests
			# 		server.serve_forever()
			#
			# 	except KeyboardInterrupt:
			# 		print('^C received, shutting down the web server')
			# 		server.socket.close()
			# 	finally:
			# 		condition_server = False
			state = True
			time.sleep(0.2)
