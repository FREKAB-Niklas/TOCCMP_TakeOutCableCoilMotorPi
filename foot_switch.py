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
def move_motor(direction, step_pin, dir_pin, delay):
    # Set the direction
    GPIO.output(dir_pin, direction)
    
    # Move the motor one step
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(delay)

try:
    print("Press and hold the forward button (GPIO 5) to move M1 forward.")
    print("Press and hold the reverse button (GPIO 6) to move M1 backward.")
    print("Press Ctrl+C to exit.")

    # Enable the motor
    GPIO.output(ENABLE_PIN, GPIO.HIGH)
    print("Motor enabled.")

    step_count = 0
    while True:
        if GPIO.input(BUTTON_FORWARD) == GPIO.LOW:
            move_motor(GPIO.HIGH, STEP_PIN_M1, DIR_PIN_M1, 0.005)
            step_count += 1
            if step_count % 100 == 0:
                print(f"Moving forward: Step {step_count}")
        elif GPIO.input(BUTTON_REVERSE) == GPIO.LOW:
            move_motor(GPIO.LOW, STEP_PIN_M1, DIR_PIN_M1, 0.005)
            step_count += 1
            if step_count % 100 == 0:
                print(f"Moving backward: Step {step_count}")
        else:
            step_count = 0
            time.sleep(0.01)  # Small delay to reduce CPU usage when no button is pressed

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    # Disable the motor
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    print("Motor disabled.")
    GPIO.cleanup()
    print("GPIO cleanup done.")
