import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
fan_pin = 19
GPIO.setup(fan_pin, GPIO.OUT)

def control_fan(state):
    GPIO.output(fan_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
