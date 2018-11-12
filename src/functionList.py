def vibrate: 
	# Vibrate the motors specified
	
def readSeatForce:
	# Reads sensor values from seat, and put them in an array
	curr_SF = 0
	return curr_SF
	
def readBackForce: 
	# Reads sensor values from back, and put them in an array
	curr_BF = 0
	return curr_BF
	
def isSitting:
	# Checks if user is sitting or not
	# Calls readSeatForce, and compare to value if user is considered sitting
	sitting = 1
	return sitting
	
def isLeaning:
	# Checks if user is leaning or not
	# Calls readBackForce and compare to value if user is considered leaning
	leaning = 1
	return leaning
	
def checkGS:
	# Checks if user is sitting properly (not tilted forward/backward or sideways)
	# Vibrates motor accordingly if bad sitting
	
def checkGL:
	# Checks if user is leaning properly (not leaning top/bottom or sideways)
	# Vibrates motor accordinglly if bad leaning
	
def shutDown(cmd):
	# Receives cmd from phone app to shutdown
	#Turn off motors
	# HX711 shutdown
	# Send confirmation message to phone app
	
def listen2App:
	# Reads message from app and returns it
	cmd = 0
	return cmd
	
def send2App: 
	# Sends message to app
	loop = 1
	while (loop):
		# send message
		#delay time
		confirm = listen2App
		if (confirm):
			break
	return		