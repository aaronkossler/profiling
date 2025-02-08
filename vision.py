import cv2
from openrouter import generate
import time
import threading

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return len(faces) > 0  # Return True if a face is detected

def process_face(frame):
    print("Person detected!")
    cv2.imwrite("capture.jpg", frame)
    print(generate("capture.jpg"))


def run_webcam():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    last_detection_time = 0  # Store the last detection time
    cooldown_seconds = 30  # Set cooldown time in seconds

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
        # elif key == ord("q"):
        current_time = time.time()  # Get current timestamp
        if(detect_face(frame) and (current_time - last_detection_time > cooldown_seconds)):
            thread = threading.Thread(target=process_face, args=(frame,))
            thread.start()
            last_detection_time = current_time
            
    vc.release()
    cv2.destroyWindow("preview")

if __name__ == "__main__":
    run_webcam()