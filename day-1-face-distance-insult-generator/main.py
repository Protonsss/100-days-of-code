import cv2
import time
import random

# hahahahaha i tried to use haarcascades at first but it was a disaster
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# # this was my first attempt
# def detect_face(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#     return img
#
# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     frame = detect_face(frame)
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

def calculate_distance(face_width_pixels, focal_length, real_face_width_cm):
    #distance = (real_face_width_cm * focal_length) / face_width_pixels
    distance = (real_face_width_cm * focal_length) / face_width_pixels # i should probably refactor this (narrator: he didnt)
    return distance

def insult_user(distance_cm):
    if distance_cm < 30:
        return "GET YOUR FACE OUT OF MY SPACE" # this just works ok
    elif distance_cm < 50:
        return "You're a little too close for comfort, bud."
    elif distance_cm < 80:
        return "Back up a bit, I can smell your breath."
    elif distance_cm < 120:
        return "Maintain a respectful distance, please."
    else:
        return "Are you even there? Get closer so I can insult you properly."

def estimate_focal_length(known_distance, known_width, image_width_in_pixels):
    focal_length = (image_width_in_pixels * known_distance) / known_width
    return focal_length

def main():
    #Known parameters
    KNOWN_DISTANCE = 60.0 #centimeters
    KNOWN_WIDTH = 14.0 #centimeters (average face width)

    cap = cv2.VideoCapture(0)

    # Get the first frame to estimate focal length
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        return

    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # ok so this part is kinda jank but whatever
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        print("No face detected. Place your face in front of camera for initial calibration.")
        return

    face_width_in_pixels = faces[0][2] # Get width of the detected face

    focal_length_found = estimate_focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, face_width_in_pixels) #dont ask me why this works

    print("Focal Length:", focal_length_found)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #draw rectangle around the face
            distance = calculate_distance(w, focal_length_found, KNOWN_WIDTH) # calculate distance
            distance = round(distance, 2) #round
            bruh = insult_user(distance) # generate insult based on distance
            cv2.putText(frame, f"Distance: {distance} cm", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #display distance
            cv2.putText(frame, bruh, (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) # display insult

        cv2.imshow('Face Distance Insult Generator', frame) # Display the resulting frame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#future me is gonna hate past me for this
if __name__ == "__main__":
    main()