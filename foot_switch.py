import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
FOOT_SWITCH_PIN = 17  # Change to GPIO 22

# Set up the pin as an input with a pull-down resistor
GPIO.setup(FOOT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def foot_switch_callback(channel):
    print("Foot switch pressed!")

try:
    # Set up an event detection on the foot switch pin
    GPIO.add_event_detect(FOOT_SWITCH_PIN, GPIO.RISING, callback=foot_switch_callback, bouncetime=200)
    print("Edge detection added successfully")

    print("Waiting for foot switch press...")
    while True:
        if GPIO.input(FOOT_SWITCH_PIN) == GPIO.HIGH:
            print("Foot switch pressed! (while loop detection)")
        time.sleep(0.1)  # Main loop doing nothing, just waiting for the interrupt

except RuntimeError as e:
    print(f"RuntimeError: {e}")

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
