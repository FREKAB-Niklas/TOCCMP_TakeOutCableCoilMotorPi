import time
import RPi.GPIO as GPIO

# GPIO pin setup
DIR_PIN_M1 = 13   # Direction pin for Motor 1
STEP_PIN_M1 = 19  # Step pin for Motor 1
DIR_PIN_M2 = 24   # Direction pin for Motor 2
STEP_PIN_M2 = 18  # Step pin for Motor 2
ENABLE_PIN = 12   # Enable pin

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

def move_motor_step(direction, step_pin, dir_pin, delay):
    GPIO.output(dir_pin, direction)
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(delay)
    print(f"Motor step: DIR={'Forward' if direction else 'Backward'}, STEP={step_pin}")

def move_motor_steps(steps, direction, step_pin, dir_pin, delay):
    for _ in range(steps):
        move_motor_step(direction, step_pin, dir_pin, delay)

def check_double_press(button_pin, max_time=0.5):
    first_press = time.time()
    while time.time() - first_press < max_time:
        if GPIO.input(button_pin) == GPIO.LOW:
            return True
    return False

try:
    print("Press the start button (GPIO 5) once to run Motor 1 for 1000 steps forward.")
    print("Double press the start button for reset (Motor 2 backward until stop, then 100 steps forward).")
    print("Press the stop button (GPIO 6) at any time to stop Motor 2 during reset.")
    print("Press Ctrl+C to exit.")

    # Enable the motor driver
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    print("Motor driver enabled.")

    while True:
        print("Waiting for button press...")
        while GPIO.input(START_BUTTON) == GPIO.HIGH:
            time.sleep(0.01)
        
        if check_double_press(START_BUTTON):
            print("Double press detected. Performing reset sequence.")
            
            # Move M2 backward until stop button is pressed
            print("Moving M2 backward until stop button is pressed.")
            while GPIO.input(STOP_BUTTON) == GPIO.HIGH:
                move_motor_step(GPIO.LOW, STEP_PIN_M2, DIR_PIN_M2, 0.001)
            
            print("Stop button pressed. Moving M2 forward 100 steps.")
            move_motor_steps(100, GPIO.HIGH, STEP_PIN_M2, DIR_PIN_M2, 0.001)
            
        else:
            print("Single press detected. Moving Motor 1 forward 1000 steps.")
            move_motor_steps(1000, GPIO.HIGH, STEP_PIN_M1, DIR_PIN_M1, 0.001)
        
        print("Sequence completed. Waiting for next button press.")
        
        # Wait for button release
        while GPIO.input(START_BUTTON) == GPIO.LOW:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable the motor driver
    print("Motor driver disabled.")
    GPIO.cleanup()
    print("GPIO cleanup done.")
