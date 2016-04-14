import RPi.GPIO as GPIO
import time
import requests

# ***** Functions *****

def setupGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(17, GPIO.IN)
	
	print("GPIO setup")
	return

def isDryerRunning():
	isRunning = False
	t0 = time.time()
	# Check once a second for 10 seconds
	while((time.time() - t0) < 10):
		if(not GPIO.input(17)):
			print("Dryer is running")
			return True
		time.sleep(1)
	
	print("Dryer has stopped")
	return isRunning
	
def main():
	print("Begin")

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
			print("Green button - Branden")
			number = ""
		else:
			print("Blue button - Franco")
			number = ""

		# Give you some time to start the dryer
		print ("Sleeping for 5 seconds")
		time.sleep(5)
		print("Wake and shake!")

		t0 = time.time()
		isRunning = True

		while(((time.time()-t0) < 30) and isRunning):
			isRunning = isDryerRunning()
			time.sleep(10)

		print("Dryer is done or time ran out")

		# Alert the person who started the dryer
		r = requests.get(baseURL + token + "&numberToDial=" + number)
		
	print("Message sent")
	return

# ***** Script *****

main()