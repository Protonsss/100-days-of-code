import cv2
import time
import numpy as np
#from playsound import playsound #old version

def calculate_aspect_ratio(bbox):
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1
    if height == 0:
        return 0 # Avoid division by zero
    return width / height

def analyze_posture():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    bad_posture_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        #print(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_bbox = (x, y, x+w, y+h)
            aspect_ratio = calculate_aspect_ratio(face_bbox)
            print(aspect_ratio)

            if aspect_ratio > 1.2:  # Adjust this value based on testing
                #bad_posture_counter += 1
                bad_posture_counter = bad_posture_counter + 1
                cv2.putText(frame, 'STRAIGHTEN UP', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            else:
                bruh = "good" #very good name
                #print("good")

            #why does python do this

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    # i should probably refactor this (narrator: he didnt)
    print(f"Number of times you were slouching: {bad_posture_counter}")
    #return bad_posture_counter

def main():
    analyze_posture()
    #ok so this part is kinda jank but whatever

if __name__ == "__main__":
    main()