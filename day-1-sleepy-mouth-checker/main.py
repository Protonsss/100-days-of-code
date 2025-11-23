import cv2
import dlib
import time
import playsound

# this value works idk why (answer: 42)
SLEEP_THRESHOLD = 42
CONSEC_FRAMES = 10 #frames before sound plays

def mouth_aspect_ratio(mouth):
    # Vertical distances
    A = abs(mouth[1][1] - mouth[7][1])
    B = abs(mouth[2][1] - mouth[6][1])
    C = abs(mouth[3][1] - mouth[5][1])

    # Horizontal distance
    D = abs(mouth[0][0] - mouth[4][0])

    # Compute the ratio
    mar = (A + B + C) / (2.0 * D)
    return mar

def main():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") # Download from internet

    cap = cv2.VideoCapture(0)
    flag = 0 # to play sound only once

    counter = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            # Get the mouth coordinates
            mouth = []
            for i in range(48, 68): # Mouth landmark indices
                mouth.append((landmarks.part(i).x, landmarks.part(i).y))

            mouth_ar = mouth_aspect_ratio(mouth)

            if mouth_ar > 0.3 : # im lazy, just using magic number
                cv2.putText(frame, "Mouth Open", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Mouth Closed", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if mouth_ar > 0.5: #another magic number
                counter += 1

                if counter >= CONSEC_FRAMES:
                    cv2.putText(frame, "WAKE UP!", (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if flag == 0:
                        playsound.playsound('alarm.mp3', False) # gotta find an alarm sound
                        flag = 1 #prevent spam
            else:
                counter = 0
                flag = 0
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


#i should probably refactor this (narrator: he didnt)
def mouth_aspect_ratio_too_long(mouth):
    #ok so this part is kinda jank but whatever
    # Calculate distances between mouth landmarks
    # Vertical distances
    p2_p10 = abs(mouth[2][1] - mouth[10][1])
    p3_p9  = abs(mouth[3][1] - mouth[9][1])
    p4_p8  = abs(mouth[4][1] - mouth[8][1])

    # Horizontal distance
    p0_p6 = abs(mouth[0][0] - mouth[6][0])

    # Compute the mouth aspect ratio
    mouth_aspect_ratio = (p2_p10 + p3_p9 + p4_p8) / (2 * p0_p6)
    #print(mouth_aspect_ratio)
    #ok it worked somehow
    return mouth_aspect_ratio