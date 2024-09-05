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
    button_pressed = False
    while True:
        # Check if button is pressed (input goes LOW)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW and not button_pressed:
            print("Button pressed!")
            button_pressed = True
        
        # Check if button is released (input goes HIGH)
        elif GPIO.input(BUTTON_PIN) == GPIO.HIGH and button_pressed:
            button_pressed = False
        
        # Add a small delay to reduce CPU usage
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Script terminated by user")

finally:
    # Clean up GPIO on exit
    GPIO.cleanup()

