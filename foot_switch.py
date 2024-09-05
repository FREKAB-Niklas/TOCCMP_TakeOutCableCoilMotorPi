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

def move_motor(motor, direction, steps):
    print(f"Moving Motor {motor} {direction} for {steps} steps")
    dir_pin = M1_DIR if motor == 1 else M2_DIR
    step_pin = M1_STEP if motor == 1 else M2_STEP
    
    GPIO.output(dir_pin, GPIO.HIGH if direction == "forward" else GPIO.LOW)
    for _ in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(0.001)  # Adjust this delay if needed
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(0.001)  # Adjust this delay if needed
        print(f"Motor {motor} step: DIR={'Forward' if direction == 'forward' else 'Backward'}, STEP={step_pin}")

def check_long_press(button_pin, duration=3):
    start_time = time.time()
    while GPIO.input(button_pin) == GPIO.LOW:
        if time.time() - start_time >= duration:
            return True
        time.sleep(0.1)
    return False

try:
    print("Press the start button (GPIO 5) briefly to run Motor 1 for 1000 steps forward.")
    print("Hold the start button for 3 seconds to trigger Motor 2 reset function.")
    print("Press the stop button (GPIO 6) to stop Motor 2 during long press function.")
    print("Press Ctrl+C to exit.")

    # Enable the motor driver
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    print("Motor driver enabled.")

    while True:
        print("Waiting for button press...")
        GPIO.wait_for_edge(START_BUTTON, GPIO.FALLING)
        print("Start button pressed. Checking for long press...")
        
        start_time = time.time()
        while GPIO.input(START_BUTTON) == GPIO.LOW:
            time.sleep(0.01)
        
        press_duration = time.time() - start_time
        
        if press_duration < 3:
            print("Short press detected. Moving Motor 1 forward 1000 steps.")
            move_motor(1, "forward", 1000)
        else:
            print("Long press detected. Moving Motor 2 forward until stop button is pressed.")
            while GPIO.input(STOP_BUTTON) == GPIO.HIGH:
                move_motor(2, "forward", 1)
                time.sleep(0.01)
            
            print("Stop button pressed. Moving Motor 2 backward 1000 steps.")
            move_motor(2, "backward", 1000)
        
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
