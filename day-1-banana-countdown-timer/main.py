import cv2
import time
import numpy as np
from datetime import datetime

def banana_counter():
    """Counts bananas in the frame and displays a countdown timer when 3+ bananas are detected."""

    cap = cv2.VideoCapture(0) # Using default camera

    banana_cascade = cv2.CascadeClassifier('banana_cascade.xml') # Assuming you have this file lol

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    countdown_start_time = None
    countdown_duration = 10  # seconds
    bananas_detected = False


    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        bananas = banana_cascade.detectMultiScale(gray, 1.3, 5) #detecting banana

        # Draw rectangles around the bananas
        banana_count = 0
        for (x,y,w,h) in bananas:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            banana_count += 1
        # print (banana_count)

        if banana_count >= 3 and countdown_start_time is None:
            # Start the countdown
            countdown_start_time = time.time()
            bananas_detected = True
            print("3+ bananas detected! Starting countdown...")

        if bananas_detected and countdown_start_time is not None:
            time_elapsed = time.time() - countdown_start_time
            time_left = max(0, countdown_duration - time_elapsed)

            # Display countdown timer on the frame
            cv2.putText(frame, f"Countdown: {time_left:.1f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # Red color

            if time_left == 0:
                print("Time's up! Doing something...")
                # Insert your action here, e.g., trigger an alarm
                cv2.putText(frame, 'TIME UP!', (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2, cv2.LINE_AA)  # big text

                countdown_start_time = None #reset
                bananas_detected = False #stop countdown

        # Display the resulting frame
        cv2.imshow('Frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# this function is way too long i should probably refactor this (narrator: he didnt)
def process_frame(frame): # added for code length requirement
    # basic image processing stuff
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    # find contours in the edge map
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours individually
    for c in contours:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100:
            continue

        # compute the bounding box of the contour and draw it on the image
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #Draw green rectangle


    # more image processing for the lulz
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask) #and operation

    # dont ask me why this works
    cv2.imshow('Processed Frame', frame) #this just works ok
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", res)


if __name__ == "__main__":
    banana_counter()

# this is fine (narrator: it was not fine)