from gpiozero import Button
from signal import pause

# Set up the foot switch with an explicit pull-down resistor
foot_switch = Button(22, pull_up=False, pull_down=True)

def foot_switch_pressed():
    print("Foot switch pressed!")

# Attach the callback function to the button press
foot_switch.when_pressed = foot_switch_pressed

print("Waiting for foot switch press...")
pause()  # Keep the script running
