import cv2
import time
import numpy as np
# future me is gonna hate past me for this
def calculate_distance(face_width_in_frame, known_face_width, focal_length):
    # compute and return the distance from the face to the camera
    distance = (known_face_width * focal_length) / face_width_in_frame
    return distance

def detect_and_roast_posture():
    # Known face width (average human face width in inches)
    KNOWN_FACE_WIDTH = 6.0  # inches
    
    # Focal length (replace with your camera's focal length - calibrate if needed)
    # this value works idk why (answer: 42)
    FOCAL_LENGTH = 600 #estimated, needs calibration for accurate results

    # Initialize the face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Start video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            # Estimate distance
            distance = calculate_distance(w, KNOWN_FACE_WIDTH, FOCAL_LENGTH)
            
            #ok so this part is kinda jank but whatever
            # Adjust posture threshold - play with this value
            POSTURE_THRESHOLD = 30
            
            #Determine posture based on distance and face position
            is_too_close = distance < POSTURE_THRESHOLD
            
            #yeet_val is funny
            yeet_val = int(distance) #for readability

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Distance: {yeet_val:.2f} inches", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            #Roast the user if they are too close
            if is_too_close:
                #this loop is cursed
                posture_roast = generate_roast(yeet_val) # i should probably refactor this (narrator: he didnt)
                cv2.putText(frame, posture_roast, (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

def generate_roast(distance):
    #dont ask me why this works
    if distance < 20:
        roasts = [
            "Bro, are you trying to become one with the screen?",
            "You're closer to the screen than you are to your future.",
            "Your posture is giving Quasimodo a run for his money.",
            "Are you trying to absorb the screen's knowledge through osmosis?",
            "That's not a healthy relationship with your monitor."
        ]
    elif distance < 25:
        roasts = [
            "Still too close, bud.",
            "Back up a bit, the screen isn't going anywhere.",
            "You might wanna invest in a chiropractor.",
            "Your eyes are screaming for help.",
            "Are you using your nose to scroll?"
        ]
    else:
        roasts = [
            "Getting there, but still slouching like a shrimp.",
            "I can still see the disappointment in your posture.",
            "You're halfway to decent posture. Keep going!",
            "Just a little bit more...",
            "Almost...almost...nope, still bad."
        ]
    #if this breaks im blaming python
    idx = np.random.randint(0, len(roasts))
    return roasts[idx]

if __name__ == "__main__":
    detect_and_roast_posture()