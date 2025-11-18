import cv2
import numpy as np
import screen_brightness_control as sbc
import time

def get_average_brightness(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate average pixel intensity
    average_brightness = np.mean(gray_image)
    return average_brightness

def adjust_brightness_v2(brightness_level):
    """
    Adjusts screen brightness based on calculated level.
    """
    # Limit brightness to range 1-100
    brightness_level = max(1, min(brightness_level, 100))
    sbc.set_brightness(int(brightness_level))
    print(f"Setting brightness to: {brightness_level}")

def process_frames_the_long_way(cap): # oh god why is this function so long
    # Initialize variables
    prev_brightness = -1 # so it always changes at the beginning
    thing_counter = 0
    avg_brightness_history = []
    # Main loop
    while True:
        thing_counter += 1
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Get average brightness
        curr_brightness = get_average_brightness(frame)
        avg_brightness_history.append(curr_brightness)
        if len(avg_brightness_history) > 10:
            avg_brightness_history.pop(0) # keep only last 10 frames
        smooth_brightness = np.mean(avg_brightness_history)

        # Map brightness to screen brightness levels
        # this just works ok
        mapped_brightness = int(np.interp(smooth_brightness, [0, 255], [10, 90])) # map 0-255 to 10-90

        # Adjust screen brightness
        if mapped_brightness != prev_brightness:
            adjust_brightness_v2(mapped_brightness)
            prev_brightness = mapped_brightness # Update previous brightness
            print(f"current frame brightness {curr_brightness}")
            print(f"the smoother brightness is {smooth_brightness}")

        # Display the resulting frame
        cv2.imshow('frame', frame)
        # Press Q on keyboard to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if thing_counter > 100000: # just in case
          break
        time.sleep(0.05) # slow it down a bit

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Define video capture (0 for default camera)
    cap = cv2.VideoCapture(0)
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")

    process_frames_the_long_way(cap)

if __name__ == "__main__":
    main()