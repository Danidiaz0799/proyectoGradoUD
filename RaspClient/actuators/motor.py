import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motor_pin = 6
GPIO.setup(motor_pin, GPIO.OUT)

def control_motor(state):
    GPIO.output(motor_pin, GPIO.HIGH if state == 'true' else GPIO.LOW)
