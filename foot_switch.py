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

def check_long_press(button_pin, duration=3):
    start_time = time.time()
    while GPIO.input(button_pin) == GPIO.LOW:
        if time.time() - start_time >= duration:
            return True
        time.sleep(0.1)
    return False

try:
    print("Press the start button (GPIO 5) briefly to run Motor 2 for 1000 steps forward.")
    print("Hold the start button for 3 seconds to trigger the reset function.")
    print("Press the stop button (GPIO 6) at any time to stop Motor 2 during reset.")
    print("Press Ctrl+C to exit.")

    # Enable the motor driver
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    print("Motor driver enabled.")

    while True:
        print("Waiting for button press...")
        while GPIO.input(START_BUTTON) == GPIO.HIGH:
            time.sleep(0.01)
        
        print("Start button pressed. Checking for long press...")
        if check_long_press(START_BUTTON):
            print("Long press detected. Performing reset sequence.")
            
            # Move M2 backward until stop button is pressed
            print("Moving M2 backward until stop button is pressed.")
            while GPIO.input(STOP_BUTTON) == GPIO.HIGH:
                move_motor_step(GPIO.LOW, STEP_PIN_M2, DIR_PIN_M2, 0.001)
            
            print("Stop button pressed. Moving M2 forward 100 steps.")
            move_motor_steps(100, GPIO.HIGH, STEP_PIN_M2, DIR_PIN_M2, 0.001)
            
        else:
            print("Short press detected. Moving Motor 2 forward 1000 steps.")
            move_motor_steps(1000, GPIO.HIGH, STEP_PIN_M2, DIR_PIN_M2, 0.001)
        
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
