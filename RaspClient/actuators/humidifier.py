import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
humidifier_pin = 13
GPIO.setup(humidifier_pin, GPIO.OUT)

def control_humidifier(state):
    GPIO.output(humidifier_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
