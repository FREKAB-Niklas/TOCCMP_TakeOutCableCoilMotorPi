import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO 17 as an output
relay_pin = 17
GPIO.setup(relay_pin, GPIO.OUT)

# Function to turn on the relay
def turn_on_relay():
    GPIO.output(relay_pin, GPIO.HIGH)
    print("Relay is ON")

# Function to turn off the relay
def turn_off_relay():
    GPIO.output(relay_pin, GPIO.LOW)
    print("Relay is OFF")

# Main function
if __name__ == "__main__":
    try:
        # Turn on the relay
        turn_on_relay()
        
        # Keep the relay on for 5 seconds
        time.sleep(20)
        
        # Turn off the relay
        turn_off_relay()
        
    except KeyboardInterrupt:
        print("Exiting gracefully")
        
    finally:
        # Cleanup the GPIO settings before exiting
        GPIO.cleanup()

