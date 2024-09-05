import RPi.GPIO as GPIO
import time
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    cleanup()
    sys.exit(0)

def cleanup():
    print("Cleaning up GPIO...")
    GPIO.cleanup()
    print("GPIO cleanup complete")

# Set up signal handler
signal.signal(signal.SIGINT, signal_handler)

# Disable GPIO warnings
GPIO.setwarnings(False)

# GPIO pin setup
PUL = 17  # Pulse pin
DIR = 27  # Direction pin
BUTTON_PIN = 22  # Button pin

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Set direction
    GPIO.output(DIR, GPIO.HIGH)  # Change to GPIO.LOW for opposite direction
    print("Direction set to HIGH")

    # Number of steps
    steps = 1600

    print("Waiting for button press...")

    while True:
        # Wait for button press
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed! Starting motor...")
            
            # Run motor
            for i in range(steps):
                GPIO.output(PUL, GPIO.HIGH)
                time.sleep(0.01)  # Slower pulse for easier observation
                GPIO.output(PUL, GPIO.LOW)
                time.sleep(0.01)
            
            print("Motor sequence complete")
            
            # Wait for button release
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.01)
            
            print("Button released. Waiting for next press...")
        
        time.sleep(0.01)  # Small delay to reduce CPU usage

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cleanup()

print("Script ended normally")

