import cv2
import numpy as np
import time

# Load the banana cascade classifier
banana_cascade = cv2.CascadeClassifier('banana_cascade.xml') # hope i named this right lol

# Check if the cascade classifier loaded properly
if banana_cascade.empty():
    raise IOError('Unable to load the banana cascade classifier XML file')

cap = cv2.VideoCapture(0) # default camera

# Define scaling factor for smaller processing
scaling_factor = 0.5

# some colors for bounding boxes
banana_color = (0,255,255) #yellowish
# old_banana_color = (255,0,0) #blue, didnt work as well

banana_count = 0
last_detection_time = 0
detection_threshold = 2  # seconds

def detect_bananas(frame):
    global banana_count, last_detection_time

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    banana_rects = banana_cascade.detectMultiScale(gray, 1.3, 5) # tune these?

    for (x,y,w,h) in banana_rects:
        curr_time = time.time()
        if curr_time - last_detection_time > detection_threshold:
            banana_count += 1
            last_detection_time = curr_time #reset timer
            cv2.rectangle(frame, (x,y), (x+w,y+h), banana_color, 3)
            cv2.putText(frame, f'Banana #{banana_count}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, banana_color, 2)

    return frame

# this function is way too long but whatever, gotta keep it real
def main():
    global scaling_factor
    while True:
        ret, frame = cap.read()
        if not ret:
            break # no frame? exit

        # Resize the frame for faster processing
        resized_frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        # Detect bananas
        frame_with_bananas = detect_bananas(resized_frame)

        # Display the resulting frame
        cv2.imshow('Banana Counter', frame_with_bananas)
        #cv2.waitKey(1) #orig
        k = cv2.waitKey(1) & 0xFF # this is important for some reason. if this breaks im blaming python

        if k == 27:
            break  # ESC to exit

    cap.release()
    cv2.destroyAllWindows()


    #old_version = do_it_this_way() # backup plan

    print(f"Total bananas detected: {banana_count}")
    # why does python do this

if __name__ == '__main__':
    main()

# i should probably refactor this (narrator: he didnt)
#ok so this part is kinda jank but whatever

# def count_bananas():
#     #do some stuff
#     pass
# this loop is cursed
# ChatGPT couldnt even help with this one