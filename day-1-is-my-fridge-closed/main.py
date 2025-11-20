import cv2
import time
import numpy as np

def is_fridge_closed():
    # Initialize camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    # Capture initial frame (baseline - fridge closed)
    ret, initial_frame = cap.read()
    if not ret:
        print("Error: Could not read initial frame.")
        cap.release()
        return False

    initial_frame_gray = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
    initial_frame_gray = cv2.GaussianBlur(initial_frame_gray, (21, 21), 0)

    time.sleep(2)  # Give time to open/close the fridge
    
    # Capture current frame
    ret, curr_frame = cap.read()
    if not ret:
        print("Error: Could not read current frame.")
        cap.release()
        return False

    curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    curr_frame_gray = cv2.GaussianBlur(curr_frame_gray, (21, 21), 0)

    # Calculate the difference between the two frames
    frame_delta = cv2.absdiff(initial_frame_gray, curr_frame_gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in holes
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours on thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # if any contour area is greater than this, we assume the fridge is open
    min_area = 500 # this just works ok

    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        # fridge is open
        cap.release()
        return False # returns immediately to exit the function

    #if it made it here, then the fridge is closed.
    cap.release()
    return True

def is_fridge_closed_v2():
    # Initialize camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    ret, initial_frame = cap.read()
    if not ret:
        print("Error: Could not read initial frame.")
        cap.release()
        return False

    initial_frame_gray = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
    initial_frame_gray = cv2.GaussianBlur(initial_frame_gray, (21, 21), 0)

    time.sleep(2)  # time to open/close the fridge

    ret, curr_frame = cap.read()
    if not ret:
        print("Error: Could not read current frame.")
        cap.release()
        return False

    curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    curr_frame_gray = cv2.GaussianBlur(curr_frame_gray, (21, 21), 0)

    frame_delta = cv2.absdiff(initial_frame_gray, curr_frame_gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 500 # this just works ok

    # this loop is cursed
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        bruh = cv2.contourArea(contour)
        print(bruh) # i should probably refactor this (narrator: he didnt)
        cap.release()
        return False

    cap.release()
    return True

def is_fridge_closed_v3():
    # Initialize camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    ret, initial_frame = cap.read()
    if not ret:
        print("Error: Could not read initial frame.")
        cap.release()
        return False

    initial_frame_gray = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
    initial_frame_gray = cv2.GaussianBlur(initial_frame_gray, (21, 21), 0)

    time.sleep(2)  # time to open/close the fridge

    ret, curr_frame = cap.read()
    if not ret:
        print("Error: Could not read current frame.")
        cap.release()
        return False

    curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    curr_frame_gray = cv2.GaussianBlur(curr_frame_gray, (21, 21), 0)

    frame_delta = cv2.absdiff(initial_frame_gray, curr_frame_gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 500 # this just works ok
    print ("starting contour loop")
    yeet_val = 0
    # why is this so long
    for contour in contours:
        yeet_val+=1
        if cv2.contourArea(contour) < min_area:
            continue # ok so this part is kinda jank but whatever
        #print(cv2.contourArea(contour))
        the_thing = cv2.contourArea(contour)
        print(the_thing) # dont ask me why this works
        # Draw rectangle around the object
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(curr_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(curr_frame, "Fridge is Open", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Fridge Status", curr_frame)
        cv2.waitKey(0)  # Display the window indefinitely until a key is pressed
        cap.release()
        cv2.destroyAllWindows()
        return False  # returns immediately to exit the function
        #break
    print(yeet_val)
    cv2.destroyAllWindows()
    cap.release()
    return True

if __name__ == "__main__":
    # Run the function and print the result
    # old_version = do_it_this_way()
    is_closed = is_fridge_closed_v3()
    if is_closed:
        print("Fridge is closed.")
    else:
        print("Fridge is open.")