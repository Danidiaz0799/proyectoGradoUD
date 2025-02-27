import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
light_pin = 26
GPIO.setup(light_pin, GPIO.OUT)

def control_light(state):
    GPIO.output(light_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
