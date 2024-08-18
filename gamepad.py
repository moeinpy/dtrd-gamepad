import pygame
import json
import time

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check for connected gamepads
if pygame.joystick.get_count() == 0:
    print("No gamepad connected.")
    exit()

# Initialize the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Gamepad initialized: {joystick.get_name()}")

num_axes = joystick.get_numaxes()
num_buttons = joystick.get_numbuttons()
num_hats = joystick.get_numhats()

# Initialize the gamepad data
gamepad_data = {
    "axes": [0] * num_axes,
    "buttons": [0] * num_buttons,
    "hats": [0] * num_hats,
    "inCalibration": False,
    "outputs": [],
}

button_map = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "LB",
    5: "RB",
    6: "Back",
    7: "Start",
    8: "Guide",
    9: "Left Stick",
    10: "Right Stick"
}

outputs = [{"value": 0, "amp": 1000, "offset": 0, "freq": 0, "isToggle": False} for _ in range(10)]
inCalibration = False
selectedOutput = 0

# File path to save the data
file_path = "gamepad_data.json"

def getJsonData():
    return {
        "axes": gamepad_data["axes"],
        "buttons": gamepad_data["buttons"],
        "hats": gamepad_data["hats"],
        "inCalibration": inCalibration,
        "outputs": outputs,
        "selectedOutput": selectedOutput,
    }

try:
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                gamepad_data["axes"][event.axis] = event.value

                if (inCalibration):
                    if (event.axis == 0):
                        if (event.value > 0.5):
                            outputs[selectedOutput]["offset"] += 1
                        elif (event.value < -0.5):
                            outputs[selectedOutput]["offset"] -= 1
                    elif (event.axis == 1):
                        if (event.value > 0.5):
                            outputs[selectedOutput]["amp"] -= 1
                        elif (event.value < -0.5):
                            outputs[selectedOutput]["amp"] += 1
                    elif (event.axis == 2):
                        if (event.value > 0.5):
                            outputs[selectedOutput]["freq"] += 1
                        elif (event.value < -0.5):
                            outputs[selectedOutput]["freq"] -= 1

            elif event.type == pygame.JOYBUTTONDOWN:
                gamepad_data["buttons"][event.button] = 1

                if (button_map[event.button] == "Start"):
                    inCalibration = not inCalibration
                    print(f"Calibration: {inCalibration}")

                elif (button_map[event.button] == "A"):
                    if (inCalibration):
                        outputs[selectedOutput]["isToggle"] = not outputs[selectedOutput]["isToggle"]
                    else:
                        if (outputs[selectedOutput]["isToggle"] and outputs[selectedOutput]["value"] != 0):
                            outputs[selectedOutput]["value"] = 0
                        else:
                            outputs[selectedOutput]["value"] = outputs[selectedOutput]["amp"]

            elif event.type == pygame.JOYBUTTONUP:
                gamepad_data["buttons"][event.button] = 0
                
                if (button_map[event.button] == "A"):
                    if (not inCalibration):
                        if (not outputs[selectedOutput]["isToggle"]):
                            outputs[selectedOutput]["value"] = 0

            elif event.type == pygame.JOYHATMOTION:
                gamepad_data["hats"][event.hat] = event.value
                if (event.hat == 0):
                    if (event.value == (0, 1)):
                        selectedOutput = (selectedOutput - 1) % len(outputs)
                    elif (event.value == (0, -1)):
                        selectedOutput = (selectedOutput + 1) % len(outputs)
                    # elif (inCalibration and event.value == (0, 1)):
                    #     outputs[selectedOutput]["min"] = gamepad_data["axes"][0]
                    # elif (inCalibration and event.value == (0, -1)):
                    #     outputs[selectedOutput]["max"] = gamepad_data["axes"][0]
            
            print(getJsonData())

        # Write the gamepad data to a JSON file
        with open(file_path, 'w') as f:
            json.dump(getJsonData(), f)

        # Sleep for a short while to avoid excessive writes
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
