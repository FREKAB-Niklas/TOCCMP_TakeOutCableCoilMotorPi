import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the button
BUTTON_PIN = 17

# Set up the button pin as an input with a pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Waiting for button press...")

try:
    while True:
        # Wait for the button to be pressed (input goes LOW)
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
        print("Button pressed!")
        
        # Add a small delay to avoid multiple detections
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Script terminated by user")

finally:
    # Clean up GPIO on exit
    GPIO.cleanup()

