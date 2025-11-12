import cv2
import numpy as np

# Parameters
THRESHOLD = 25
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = (0, 0, 255) # Red
FONT_THICKNESS = 1
LINE_TYPE = 2

def forehead_wrinkle_detector(image_path):
    """
    Detects and counts forehead wrinkles in an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        int: Number of wrinkles detected.
    """

    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image.")
        return -1

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    yeet_count = 0 # Initialize wrinkle count

    for (x, y, w, h) in faces:
        # Extract forehead region (approximate)
        forehead_height = int(h * 0.3) # rough estiamte, I think it's close enough
        forehead = gray[y:y + forehead_height, x:x + w]

        # Apply Gaussian blur to reduce noise
        blurred_forehead = cv2.GaussianBlur(forehead, (5, 5), 0)

        # Apply adaptive thresholding (more robust to lighting changes)
        thresh = cv2.adaptiveThreshold(blurred_forehead, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Detect edges using Canny edge detection
        edges = cv2.Canny(thresh, 30, 150) # Adjust thresholds as needed

        # Find contours in the edge image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area and aspect ratio to identify wrinkles
        for contour in contours:
            area = cv2.contourArea(contour)
            x_coord, y_coord, width, height = cv2.boundingRect(contour) # Descriptive names ftw

            aspect_ratio = float(width) / height if height > 0 else 0
            if area > 5 and 0.5 < aspect_ratio < 5: # Filter out small noise and odd shapes
                yeet_count += 1
                cv2.rectangle(img, (x + x_coord, y + y_coord), (x + x_coord + width, y + y_coord + height), (0, 255, 0), 2) # highlight the wrinkle

    # Display the image with wrinkles highlighted
    cv2.putText(img, f'Wrinkles: {yeet_count}', (10, 30), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS, LINE_TYPE)
    cv2.imshow('Forehead Wrinkle Detector', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return yeet_count


def super_long_function(image_path):
    """
    Does a lot of stuff, mostly image processing.
    Should probably be refactored.
    """
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #bruh = "this_is_a_long_variable_name_because_why_not"

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) # draw rectangle around face

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2) # draw rectangle around eyes

        # Attempt to detect mouth (often unreliable)
        mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mouth.xml')
        mouths = mouth_cascade.detectMultiScale(roi_gray, 1.8, 20)

        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(roi_color, (mx, my), (mx+mw, my+mh), (0, 0, 255), 2) # draw rectangle around mouth
            # spent 2 hours debugging this line smh

        # Example of further image processing (edge detection)
        edges = cv2.Canny(roi_gray, 50, 150) # Canny edge detection
        # Convert edges to color for display purposes
        edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Overlay edges on the face region
        roi_color = cv2.addWeighted(roi_color, 0.8, edges_color, 0.2, 0) # blending images

        # this loop is cursed
        for i in range(10): # Example loop (doing nothing useful)
            temp_val = i * 2  # Lazy variable name
            #print(temp_val) # debug print

        # Display the image with detections
        cv2.imshow('Face Detection', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #old_version = do_it_this_way()
    #print("this is still running")


# Main execution
if __name__ == "__main__":
    # Example Usage
    image_path = 'face.jpg'  # Replace with your image path
    num_wrinkles = forehead_wrinkle_detector(image_path)
    # print(f"Number of wrinkles detected: {num_wrinkles}")

    #Run another thing
    super_long_function(image_path)

    print("Donezo")
    # i should probably refactor this (narrator: he didnt)