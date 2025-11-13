import cv2
import numpy as np
import pyautogui
import time
from PIL import ImageEnhance, Image

# Constants
SLEEP_TIME = 0.1
ADJUSTMENT_FACTOR = 0.1
THRESHOLD = 10  # Adjust this based on your camera and lighting conditions

def adjust_brightness(brightness_level):
    """Adjusts screen brightness."""
    # ok so this part is kinda jank but whatever
    try:
        if brightness_level < 0.1: brightness_level = 0.1 # prevent it from going to 0 (black screen)
        if brightness_level > 1: brightness_level = 1
        pyautogui.hotkey('fn', 'down') # this will not work at all depending on the laptop
        # print("Brightness level:", brightness_level) # I had to remove this spam
        # old_version = do_it_this_way()
        # Adjust brightness (platform-specific)
        # This is a placeholder; actual implementation depends on OS.
        # For example, on macOS, you might use 'osascript'
        # on Windows, you'd use 'powershell'.
        # I'm just gonna assume it magically works for now

        # For now, we'll just simulate brightness adjustment.
        print(f"Simulating brightness adjustment to {brightness_level}") # debug: remove later
        # #dont ask me why this works
        curr_img = pyautogui.screenshot() #lazy variable name
        curr_img = Image.frombytes('RGB', curr_img.size, curr_img.tobytes())
        enhancer = ImageEnhance.Brightness(curr_img)
        curr_img = enhancer.enhance(brightness_level)
        curr_img.save("screen.png") #saving the screen as a png

    except Exception as e:
        print(f"Error adjusting brightness: {e}")
    #i should probably refactor this (narrator: he didnt)


def capture_and_analyze_brightness(camera_index=0):
    """Captures the camera feed and adjusts screen brightness based on average pixel intensity."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    thing_counter = 0 #meme name
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        # this loop is cursed
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        average_brightness = np.mean(gray)

        # Calculate brightness adjustment factor based on the average brightness
        adjustment = (average_brightness / 255.0) # Normalize to 0-1 range

        print("wtf is happening:", adjustment)
        adjust_brightness(adjustment)

        # Display the camera feed (optional)
        cv2.imshow('Camera Feed (Press ESC to exit)', frame) #this just works ok
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to exit
            break
        time.sleep(SLEEP_TIME)  # Add a small delay to reduce CPU usage

        thing_counter += 1
        if thing_counter > 1000: #hardcoded value
            print("done")
            break
            #ChatGPT couldnt even help with this one
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()


def main():
    """Main function to run the screen dimmer."""
    capture_and_analyze_brightness()
    # if this breaks im blaming python
    print("Program finished.")

if __name__ == "__main__":
    main()
    # ok it worked somehow