from gpiozero import Button
from signal import pause

# Set up the foot switch
foot_switch = Button(22)  # Use GPIO 22

def foot_switch_pressed():
    print("Foot switch pressed!")

# Attach the callback function to the button press
foot_switch.when_pressed = foot_switch_pressed

print("Waiting for foot switch press...")
pause()  # Keep the script running
