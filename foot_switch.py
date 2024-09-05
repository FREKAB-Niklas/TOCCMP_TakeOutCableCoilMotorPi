import time
import RPi.GPIO as GPIO

# GPIO pin setup for the first motor
DIR_PIN_M1 = 13   # Direction pin
STEP_PIN_M1 = 19  # Step pin
ENABLE_PIN = 12   # Enable pin

# GPIO pin setup for the second motor
DIR_PIN_M2 = 24   # Direction pin
STEP_PIN_M2 = 18  # Step pin

# GPIO pin setup for buttons
BUTTON_FORWARD = 5  # Button for forward movement
BUTTON_REVERSE = 6  # Button for reverse movement

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN_M1, GPIO.OUT)
GPIO.setup(STEP_PIN_M1, GPIO.OUT)
GPIO.setup(DIR_PIN_M2, GPIO.OUT)
GPIO.setup(STEP_PIN_M2, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)
GPIO.setup(BUTTON_FORWARD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_REVERSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to move the motor
def move_motor(steps, direction, step_pin, dir_pin, delay):
    # Enable the motor
    GPIO.output(ENABLE_PIN, GPIO.HIGH)
    print(f"Motor enabled. Moving {'forward' if direction == GPIO.HIGH else 'backward'} for {steps} steps.")

    # Set the direction
    GPIO.output(dir_pin, direction)
    
    # Move the motor
    for i in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(delay)
        
        if i % 100 == 0:  # Print every 100 steps for more concise output
            print(f"Step {i+1}/{steps}")

    print("Movement completed.")
    
    # Disable the motor after moving
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    print("Motor disabled.")

try:
    print("Press the forward button (GPIO 5) to move M1 forward.")
    print("Press the reverse button (GPIO 6) to move M1 backward.")
    print("Press Ctrl+C to exit.")

    while True:
        if GPIO.input(BUTTON_FORWARD) == GPIO.LOW:
            print("Forward button pressed. Moving M1 forward...")
            move_motor(steps=1000, direction=GPIO.HIGH, step_pin=STEP_PIN_M1, dir_pin=DIR_PIN_M1, delay=0.005)
            time.sleep(0.5)  # Debounce delay
        
        if GPIO.input(BUTTON_REVERSE) == GPIO.LOW:
            print("Reverse button pressed. Moving M1 backward...")
            move_motor(steps=1000, direction=GPIO.LOW, step_pin=STEP_PIN_M1, dir_pin=DIR_PIN_M1, delay=0.005)
            time.sleep(0.5)  # Debounce delay

        time.sleep(0.1)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    GPIO.cleanup()
    print("GPIO cleanup done.")