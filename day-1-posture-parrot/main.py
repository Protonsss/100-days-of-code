import cv2
import time
import numpy as np

# Posture Parrot - Roasts your posture in real-time!

def posture_check(image):
    # face detection because why not
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        return "Where's your FACE?! Stop hiding!"

    for (x, y, w, h) in faces:
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # approximate shoulder positions (lol)
        left_shoulder_x = face_center_x - w * 1.2
        right_shoulder_x = face_center_x + w * 1.2
        shoulder_y = face_center_y + h * 1.5

        # draw circles to visualize shoulder position estimation
        cv2.circle(image, (int(left_shoulder_x), int(shoulder_y)), 15, (255, 0, 0), 2)
        cv2.circle(image, (int(right_shoulder_x), int(shoulder_y)), 15, (0, 0, 255), 2)

        # determine screen midpoint
        screen_midpoint = image.shape[1] // 2

        # calculate the amount of lean
        lean_amount = face_center_x - screen_midpoint
        lean_percentage = (lean_amount / screen_midpoint) * 100 # percentage lean

        print("wtf is happening:", lean_percentage)

        # roast level selection
        if abs(lean_percentage) > 15:  # 15% lean is considered bad
            if lean_percentage > 0:
                return "Dude, are you TRYING to become the Leaning Tower of Pisa? Sit up straight!"
            else:
                return "You're leaning so far left you're practically communist! Fix your posture!"
        elif abs(lean_percentage) > 5: # moderate lean
            if lean_percentage > 0:
                return "A little to the right. You look like you're about to fall asleep."
            else:
                return "Little to the left. Stop slouching!"
        else:
            return "Posture's looking decent. Keep it up (literally)!"
        
        # print(lean_percentage) # DEBUG - REMOVE LATER

def main():
    cap = cv2.VideoCapture(0) # default camera

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50) #text position
    fontScale = 1
    color = (255, 255, 255)
    thickness = 2

    # # old_version = cv2.FONT_HERSHEY_SIMPLEX #backup plan

    while(True):
        ret, frame = cap.read() # capture frame-by-frame
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # flip image horizontally
        frame = cv2.flip(frame, 1)

        # posture checking logic
        roast = posture_check(frame)
        # if this breaks im blaming python
        # Display the resulting frame
        curr_img = cv2.putText(frame, roast, org, font,
                           fontScale, color, thickness, cv2.LINE_AA)

        cv2.imshow('Posture Parrot', curr_img) #lazy name

        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# why does python do this
if __name__ == "__main__":
    main()