import cv2
from openrouter import generate

def run_webcam():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
        elif key == ord("q"):
            cv2.imwrite("capture.jpg", frame)
            print(generate("capture.jpg"))
            
    vc.release()
    cv2.destroyWindow("preview")

if __name__ == "__main__":
    run_webcam()