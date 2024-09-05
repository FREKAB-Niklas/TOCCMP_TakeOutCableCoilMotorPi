import time
import RPi.GPIO as GPIO

# GPIO pin setup for the first motor (M1)
DIR_PIN_M1 = 13   # Direction pin
STEP_PIN_M1 = 19  # Step pin
ENABLE_PIN = 12   # Enable pin

# GPIO pin setup for the second motor (M2)
DIR_PIN_M2 = 24   # Direction pin
STEP_PIN_M2 = 18  # Step pin

# GPIO pin setup for buttons
START_BUTTON = 5  # Start button
STOP_BUTTON = 6   # Stop button

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN_M1, GPIO.OUT)
GPIO.setup(STEP_PIN_M1, GPIO.OUT)
GPIO.setup(DIR_PIN_M2, GPIO.OUT)
GPIO.setup(STEP_PIN_M2, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)
GPIO.setup(START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to move the motor one step
def move_motor_step(direction, step_pin, dir_pin, delay):
    GPIO.output(dir_pin, direction)
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(delay)
    print(f"Motor step: DIR={direction}, STEP={step_pin}")  # Debug print

try:
    print("Press the start button (GPIO 5) to begin the sequence.")
    print("Press the stop button (GPIO 6) at any time to stop the motor.")
    print("Press Ctrl+C to exit.")

    # Enable the motors
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Changed to LOW to enable
    print("Motors enabled.")

    while True:
        # Wait for start button press
        print("Waiting for start button press...")
        while GPIO.input(START_BUTTON) == GPIO.HIGH:
            time.sleep(0.01)
        
        print("Start button pressed. Moving M2 forward until stop button is pressed.")
        
        # Move M2 forward until stop button is pressed
        step_count = 0
        while GPIO.input(STOP_BUTTON) == GPIO.HIGH:
            move_motor_step(GPIO.HIGH, STEP_PIN_M2, DIR_PIN_M2, 0.005)
            step_count += 1
            if step_count % 100 == 0:
                print(f"Forward steps: {step_count}")
        
        print("Stop button pressed. Moving M2 backward 100 steps.")
        
        # Move M2 backward 100 steps
        for i in range(100):
            move_motor_step(GPIO.LOW, STEP_PIN_M2, DIR_PIN_M2, 0.005)
            if i % 10 == 0:
                print(f"Backward steps: {i+1}")
        
        print("Sequence completed. Press the start button again to repeat.")
        
        # Wait for both buttons to be released
        while GPIO.input(START_BUTTON) == GPIO.LOW or GPIO.input(STOP_BUTTON) == GPIO.LOW:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    # Disable the motors
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Changed to HIGH to disable
    print("Motors disabled.")
    GPIO.cleanup()
    print("GPIO cleanup done.")
