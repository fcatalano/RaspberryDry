import RPi.GPIO as GPIO
import time
import requests

# ***** Functions *****

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(17, GPIO.IN)
	
	return

def isDryerRunning():
	isRunning = False
	t0 = time.time()
	# Check once every 50ms for 30 seconds
	while((time.time() - t0) < 30):
		if(not GPIO.input(17)):
			return True
		time.sleep(0.05)
	
	return isRunning
	
def main():
	setupGPIO()
	baseURL = "https://api.tropo.com/1.0/sessions?action=create&token="
	token = ""
	number = ""
	
	while True:
	    bm_input = not GPIO.input(27)
	    fc_input = not GPIO.input(22)
	    if(bm_input or fc_input):
		# Button pressed
		if(bm_input):
			number = ""
		else:
			number = ""
		# Give you some time to start the dryer
		time.sleep(10)
	
		t0 = time.time()
		isRunning = True
		# Run for no longer than 2 hours
		while(((time.time()-t0) < 7200) and isRunning):
			isRunning = isDryerRunning()
			time.sleep(30)

		# Alert the person who started the dryer
		r = requests.get(baseURL + token + "&numberToDial=" + number)
	return

# ***** Script *****

main()
