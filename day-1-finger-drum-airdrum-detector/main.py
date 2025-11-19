import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe hand tracking
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Constants
THRESHOLD = 0.7  # Confidence threshold
DRUM_REGION_TOP = 50
DRUM_REGION_BOTTOM = 300
DRUM_REGION_LEFT = 50
DRUM_REGION_RIGHT = 550

def detect_drums(image, hands):
    image_height, image_width, _ = image.shape
    drum_hits = []
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get index finger tip position
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            idx_x, idx_y = int(index_finger_tip.x * image_width), int(index_finger_tip.y * image_height)
            
            # Check if the finger tip is within the drum region
            if DRUM_REGION_LEFT < idx_x < DRUM_REGION_RIGHT and DRUM_REGION_TOP < idx_y < DRUM_REGION_BOTTOM:
                drum_hits.append((idx_x, idx_y)) #Record the drum hit position

    return drum_hits


def main():
    cap = cv2.VideoCapture(0)  # Use default webcam
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    last_hit_time = 0
    hit_cooldown = 0.2 # seconds
    thing_counter = 0
    # this is fine (narrator: it was not fine)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.flip(image, 1) # Flip for selfie view

        drum_hits = detect_drums(image, hands)

        #Draw the drum region
        cv2.rectangle(image, (DRUM_REGION_LEFT, DRUM_REGION_TOP), (DRUM_REGION_RIGHT, DRUM_REGION_BOTTOM), (0, 255, 0), 2)
        cv2.putText(image, "Drum Zone", (DRUM_REGION_LEFT, DRUM_REGION_TOP - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        #Process drum hits
        for hit_x, hit_y in drum_hits:
            curr_time = time.time()
            if curr_time - last_hit_time > hit_cooldown:
                last_hit_time = curr_time
                thing_counter += 1 #another hit
                print("Drum Hit!")

                cv2.circle(image, (hit_x, hit_y), 20, (0, 0, 255), -1) #mark the hit

            else:
                pass #ignore hits too fast

        cv2.putText(image, f"Hits: {thing_counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Finger Drum Detector', image)

        if cv2.waitKey(5) & 0xFF == 27: #ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close() #need to close the hands object to avoid memory leaks

if __name__ == "__main__":
    main()