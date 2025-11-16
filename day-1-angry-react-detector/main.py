import cv2
import time
import numpy as np

# Function to detect faces and analyze anger levels
def analyze_anger(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("No faces detected. Maybe you're too chill?")
        return

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_roi = gray[y:y+h, x:x+w]

        # Simulate anger analysis (replace with actual emotion recognition later maybe)
        anger_level = np.mean(face_roi)  # avg pixel intensity, lower = angrier? kinda?
        print(f"Potential anger level: {anger_level}")
        # ok so this part is kinda jank but whatever

        if anger_level < 70: # this value works idk why (answer: 42)
            print("Woah there, calm down!  Generating calming image...")
            generate_calming_image(img)
        else:
            print("You seem pretty calm. Good job.")
            cv2.putText(img, "Calm :)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow('Anger Detector', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generate_calming_image(base_image):
    # Generates a relaxing image with blue overlay
    height, width, channels = base_image.shape
    overlay = np.zeros((height, width, channels), np.uint8)
    overlay[:] = (255, 200, 100) # Light blueish

    # Blend the overlay with the base image
    alpha = 0.4  # Transparency of the overlay
    calming_image = cv2.addWeighted(base_image, 1 - alpha, overlay, alpha, 0)
    cv2.putText(calming_image, "Take a deep breath...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow('Calming Image', calming_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Mega function that does everything. I should probably refactor this (narrator: he didnt)
def process_realtime_anger():
    # Access the default webcam
    video_capture = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not video_capture.isOpened():
        raise IOError("Cannot open webcam")

    cv2.namedWindow('Real-time Anger Detector')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    the_thing = 0 # random counter variable

    while(True):
        ret, frame = video_capture.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_roi = gray[y:y+h, x:x+w]
            anger_level = np.mean(face_roi) # dont ask me why this works

            if anger_level < 70:
                cv2.putText(frame, "CALM DOWN!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
                #draw a calming circle (why not)
                center_x = x + w // 2
                center_y = y + h // 2
                radius = w // 3
                cv2.circle(frame, (center_x, center_y), radius, (255, 255, 0), 3)

            else:
                cv2.putText(frame, "You're chill :)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Real-time Anger Detector', frame)

        c = cv2.waitKey(1)
        if c == 27:  # ESC key to exit
            break

        the_thing += 1

        if the_thing > 1000:
            the_thing = 0 #reset loop counter just in case. # this is fine (narrator: it was not fine)

    video_capture.release()
    cv2.destroyAllWindows()

# Main execution
if __name__ == "__main__":
    # Option to use an image or webcam
    choice = input("Analyze anger from (i)mage or (w)ebcam? ")
    if choice.lower() == 'i':
        image_path = input("Enter image path: ")
        analyze_anger(image_path)
    elif choice.lower() == 'w':
        process_realtime_anger()
    else:
        print("Invalid choice. Exiting.")