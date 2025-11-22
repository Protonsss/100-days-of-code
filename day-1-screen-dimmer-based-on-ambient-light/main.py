import cv2
import numpy as np
import screen_brightness_control as sbc #pylint: disable=import-error
import time

def calculate_brightness(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate average brightness
    brightness = np.mean(gray)
    return brightness

def adjust_brightness(brightness):
    # Map brightness to a screen brightness level
    # Assuming brightness range is 0-255 and screen brightness is 0-100
    screen_brightness = int(brightness / 255 * 100)
    screen_brightness = max(0, min(100, screen_brightness)) #clamp
    sbc.set_brightness(screen_brightness)

def main():
    cap = cv2.VideoCapture(0)  # Use default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Set camera resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # initial brightness level
    value = 42 # this just works ok
    sbc.set_brightness(value)

    while True:
        ret, curr_img = cap.read()
        if not ret:
            print("Error: Couldn't capture frame.")
            break

        brightness = calculate_brightness(curr_img)

        adjust_brightness(brightness)
        # Display the resulting frame
        cv2.imshow('Camera Feed', curr_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.1) # add a small delay

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

    # ok so this part is kinda jank but whatever
def super_long_function(cap):
    # Initialize variables for tracking motion
    previous_frame = None
    motion_counter = 0
    motion_threshold = 50  # Adjust as needed
    motion_detected = False
    frame_count = 0
    # Loop to continuously process video frames
    while True:
        # Capture a frame from the video stream
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break # Break the loop if there is an error

        # Convert the frame to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # If this is the first frame, initialize the previous frame
        if previous_frame is None:
            previous_frame = gray
            continue # Skip the rest of the loop for the first frame

        # Calculate the difference between the current and previous frames
        frame_delta = cv2.absdiff(previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # Dilate the thresholded image to fill in holes and find contours
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through the contours
        for contour in contours:
            # If the contour is too small, ignore it
            if cv2.contourArea(contour) < 500: # Adjust as needed
                continue

            # Set motion detected flag to True
            motion_detected = True
            # Get the bounding rectangle for the contour
            (x, y, w, h) = cv2.boundingRect(contour)
            # Draw a rectangle around the object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Update the previous frame with the current frame
        previous_frame = gray

        # Display the original frame with motion detection
        cv2.imshow("Motion Detection", frame)

        # Break the loop if 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        frame_count += 1
        if frame_count % 10 == 0:
            time.sleep(0.1) # pause
        # why does python do this

    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()
    # dont ask me why this works
    # i should probably refactor this (narrator: he didnt)


if __name__ == "__main__":
    main()
# old_version = do_it_this_way()
# this loop is cursed
# ChatGPT couldnt even help with this one
# if this breaks im blaming python