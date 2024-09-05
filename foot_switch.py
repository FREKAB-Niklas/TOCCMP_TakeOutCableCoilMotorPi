import RPi.GPIO as GPIO
import time

# Disable GPIO warnings
GPIO.setwarnings(False)

# GPIO pin setup
PUL = 17  # Pulse pin
DIR = 27  # Direction pin
BUTTON_PIN = 22  # New pin for the button

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

try:
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

except KeyboardInterrupt:
    print("Script interrupted by user")
finally:
    GPIO.cleanup()
    print("GPIO cleanup complete")

