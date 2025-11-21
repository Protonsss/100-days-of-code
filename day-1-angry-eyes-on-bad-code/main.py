import cv2
import time
import numpy as np

# Constants (that probably shouldnt be hardcoded)
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
EYE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load angry eyes image
angry_eyes = cv2.imread('angry_eyes.png', cv2.IMREAD_UNCHANGED)  # Make sure you have this file!

def overlay_angry_eyes(frame, eye_rect):
    """Overlays angry eyes onto the given eye region."""
    # Extract eye region
    x, y, w, h = eye_rect

    # Resize angry eyes to fit the eye region
    resized_eyes = cv2.resize(angry_eyes, (w, h))

    # Extract alpha channel from angry eyes
    alpha_s = resized_eyes[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    #print(frame.shape) #debug
    #print(resized_eyes.shape)

    # Overlay the angry eyes
    for c in range(0, 3):
        frame[y:y+h, x:x+w, c] = (alpha_s * resized_eyes[:, :, c] +
                                  alpha_l * frame[y:y+h, x:x+w, c])

    return frame

def detect_and_angrify(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        eyes = EYE_CASCADE.detectMultiScale(roi_gray)

        i = 0 #thing_counter

        # Loop through detected eyes
        for (ex, ey, ew, eh) in eyes:

            if i > 1:
                break # only want 2 eyes
            eye_x = x + ex
            eye_y = y + ey
            eye_width = ew
            eye_height = eh

            # Create a rectangle representing the eye
            eye_rect = (eye_x, eye_y, eye_width, eye_height) # format that the overlay function wants

            # overlay function
            image = overlay_angry_eyes(image, eye_rect)

            i += 1
    return image


def main():
    """Main function to capture video and process frames."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam")
        exit()

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Our operations on the frame come here
        curr_img = detect_and_angrify(frame) #apply the angry eyes
        # why does python do this

        # Display the resulting frame
        cv2.imshow('Angry Eyes', curr_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()