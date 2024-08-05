import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
FOOT_SWITCH_PIN = 27

# Set up the pin as an input with a pull-down resistor
GPIO.setup(FOOT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def foot_switch_callback(channel):
    print("Foot switch pressed!")

# Set up an event detection on the foot switch pin
GPIO.add_event_detect(FOOT_SWITCH_PIN, GPIO.RISING, callback=foot_switch_callback, bouncetime=200)

try:
    while True:
        time.sleep(0.1)  # Main loop doing nothing, just waiting for the interrupt

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()
