import time
import RPi.GPIO as GPIO

# GPIO pin setup
DIR_PIN_M1 = 13   # Direction pin for Motor 1
STEP_PIN_M1 = 19  # Step pin for Motor 1
DIR_PIN_M2 = 24   # Direction pin for Motor 2
STEP_PIN_M2 = 18  # Step pin for Motor 2
ENABLE_PIN_M2 = 12   # Enable pin
ENABLE_PIN_M1 = 4   # Enable pin

START_BUTTON = 5  # Start button
STOP_BUTTON = 6   # Stop button

# Motor-specific delays (in seconds)
DELAY_M1 = 0.005  # Adjust this value for Motor 1 speed
DELAY_M2 = 0.001   # Adjust this value for Motor 2 speed

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN_M1, GPIO.OUT)
GPIO.setup(STEP_PIN_M1, GPIO.OUT)
GPIO.setup(DIR_PIN_M2, GPIO.OUT)
GPIO.setup(STEP_PIN_M2, GPIO.OUT)
GPIO.setup(ENABLE_PIN_M2, GPIO.OUT)
GPIO.setup(ENABLE_PIN_M1, GPIO.OUT)
GPIO.setup(START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def reset_motor_driver():
    print("Resetting motor driver...")
    GPIO.output(ENABLE_PIN_M2, GPIO.LOW)
    GPIO.output(ENABLE_PIN_M1, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(ENABLE_PIN_M2, GPIO.HIGH)
    GPIO.output(ENABLE_PIN_M1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(ENABLE_PIN_M2, GPIO.LOW)
    GPIO.output(ENABLE_PIN_M1, GPIO.LOW)
    time.sleep(0.1) 
    print("Motor driverS reset complete.")

def move_motor_steps(steps, direction, step_pin, dir_pin, delay):
    try:
        GPIO.output(ENABLE_PIN_M2, GPIO.HIGH)  # Enable the motor (LOW is enable for most drivers)
        GPIO.output(ENABLE_PIN_M1, GPIO.LOW)  # Disable the motor (LOW is enable for most drivers)
        print(f"Motor enabled. Moving {'forward' if direction == GPIO.HIGH else 'backward'} for {steps} steps.")
        
        GPIO.output(dir_pin, direction)
        for _ in range(steps):
            GPIO.output(step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(step_pin, GPIO.LOW)
            time.sleep(delay)
        
        print("Movement completed.")
    except Exception as e:
        print(f"Error during motor movement: {e}")
        reset_motor_driver()
    finally:
        GPIO.output(ENABLE_PIN_M2, GPIO.LOW)  # Disable the motor
        print("Motor disabled.")

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

    reset_motor_driver()  # Reset the motor driver at the start

    while True:
        print("Waiting for button press...")
        while GPIO.input(START_BUTTON) == GPIO.HIGH:
            time.sleep(0.01)
        
        print("Start button pressed. Checking for long press...")
        if check_long_press(START_BUTTON):
            print("Long press detected. Running Motor 2 until stop button is pressed.")
            GPIO.output(ENABLE_PIN_M2, GPIO.HIGH)  # Enable the motor
            try:
                while GPIO.input(STOP_BUTTON) == GPIO.HIGH:
                    move_motor_steps(1, GPIO.HIGH, STEP_PIN_M2, DIR_PIN_M2, DELAY_M2)

                print("Stop button pressed. Moving M2 backward 1000 steps.")
                move_motor_steps(1000, GPIO.LOW, STEP_PIN_M2, DIR_PIN_M2, DELAY_M2)
            except Exception as e:
                print(f"Error during M2 operation: {e}")
                reset_motor_driver()
            finally:
                GPIO.output(ENABLE_PIN_M2, GPIO.LOW)  # Disable the motor
            
        else:
            print("Short press detected. Moving Motor 1 forward 1000 steps.")
            move_motor_steps(1000, GPIO.HIGH, STEP_PIN_M1, DIR_PIN_M1, DELAY_M1)
        
        print("Sequence completed. Waiting for next button press.")
        
        # Wait for button release
        while GPIO.input(START_BUTTON) == GPIO.LOW:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    GPIO.output(ENABLE_PIN_M2, GPIO.LOW)  # Ensure motor is disabled
    GPIO.cleanup()
    print("GPIO cleanup done.")
