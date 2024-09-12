import time
import RPi.GPIO as GPIO
import threading

# GPIO pin setup
DIR_PIN = 13   # Direction pin for Motor
STEP_PIN = 19  # Step pin for Motor
ENABLE_PIN = 12   # Enable pin

START_BUTTON = 5  # Start button
STOP_BUTTON = 6   # Stop button

# Motor delay (in seconds)
DELAY = 0.0001  # Adjust this value for Motor speed

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)
GPIO.setup(START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables
motor_running = False

def reset_motor_driver():
    print("Resetting motor driver...")
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Disable
    time.sleep(0.1)
    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Enable
    time.sleep(0.1)
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Disable
    print("Motor driver reset complete.")

def run_motor(direction):
    global motor_running
    GPIO.output(DIR_PIN, direction)
    while motor_running and GPIO.input(START_BUTTON) == GPIO.LOW:
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(DELAY)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(DELAY)

def stop_motor():
    global motor_running
    motor_running = False
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Disable the motor
    print("Motor stopped")

def check_buttons():
    global motor_running
    while True:
        if GPIO.input(START_BUTTON) == GPIO.LOW and not motor_running:
            print("Start button pressed. Running motor forward.")
            motor_running = True
            GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Enable the motor
            run_motor(GPIO.HIGH)  # Run forward
            GPIO.output(ENABLE_PIN, GPIO.LOW)  # Disable the motor when button is released
            motor_running = False
            print("Start button released. Motor stopped.")
        elif GPIO.input(STOP_BUTTON) == GPIO.LOW:
            stop_motor()
        time.sleep(0.01)  # Small delay to prevent excessive CPU usage

try:
    print("Press the start button (GPIO 5) to run the motor forward.")
    print("Press the stop button (GPIO 6) to stop the motor.")
    print("Press Ctrl+C to exit.")

    reset_motor_driver()  # Reset the motor driver at the start

    # Start button checking in a separate thread
    button_thread = threading.Thread(target=check_buttons)
    button_thread.daemon = True
    button_thread.start()

    # Main loop
    while True:
        time.sleep(0.1)  # Keep the main thread alive

except KeyboardInterrupt:
    print("Program interrupted by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Ensure motor is disabled on program exit
    GPIO.cleanup()
    print("GPIO cleanup done.")
