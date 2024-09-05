import time
import RPi.GPIO as GPIO

# GPIO pin setup for the first motor (M1)
DIR_PIN_M1 = 13   # Direction pin
STEP_PIN_M1 = 19  # Step pin
ENABLE_PIN = 12   # Enable pin

# GPIO pin setup for the second motor (M2)
DIR_PIN_M2 = 24   # Direction pin
STEP_PIN_M2 = 18  # Step pin

# GPIO pin setup for start button
START_BUTTON = 5  # Start button

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN_M1, GPIO.OUT)
GPIO.setup(STEP_PIN_M1, GPIO.OUT)
GPIO.setup(DIR_PIN_M2, GPIO.OUT)
GPIO.setup(STEP_PIN_M2, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)
GPIO.setup(START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to move the motor one step
def move_motor_step(direction, step_pin, dir_pin, delay):
    GPIO.output(dir_pin, direction)
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(delay)

# Function to move the motor a specific number of steps
def move_motor_steps(steps, direction, step_pin, dir_pin, delay):
    for _ in range(steps):
        move_motor_step(direction, step_pin, dir_pin, delay)

try:
    print("Press the start button (GPIO 5) to begin the sequence.")
    print("Press Ctrl+C to exit.")

    # Enable the motors
    GPIO.output(ENABLE_PIN, GPIO.HIGH)
    print("Motors enabled.")

    while True:
        # Run M2 backwards until the start button is pressed
        print("Running M2 backwards. Press the start button to stop and begin the sequence.")
        while GPIO.input(START_BUTTON) == GPIO.HIGH:
            move_motor_step(GPIO.LOW, STEP_PIN_M2, DIR_PIN_M2, 0.005)

        print("Start button pressed. Stopping M2 and moving forward 100 steps.")
        
        # Move M2 forward 100 steps
        move_motor_steps(100, GPIO.HIGH, STEP_PIN_M2, DIR_PIN_M2, 0.005)
        
        print("Sequence completed. Press the start button again to repeat.")
        
        # Wait for button release to avoid immediate repeat
        while GPIO.input(START_BUTTON) == GPIO.LOW:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    # Disable the motors
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    print("Motors disabled.")
    GPIO.cleanup()
    print("GPIO cleanup done.")
