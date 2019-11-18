import time
while True:
	# try:
	#     r = requests.get(url, params={'s': thing})
	# except requests.exceptions.RequestException as e:  # This is the correct syntax
	#     print e
	#     sys.exit(1)
	try:
		time.sleep(5)
		1/0
	except:
		print ('ruim')
		time.sleep(0.1)
