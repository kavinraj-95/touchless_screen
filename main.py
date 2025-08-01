import cv2
from hand_tracker import HandTracker
from gesture_controller import GestureController

cap = cv2.VideoCapture(0)
tracker = HandTracker()
controller = GestureController(sensitivity=3.0, dead_zone=5)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Mirror camera
    frame = tracker.find_hands(frame, draw=False)
    lm_list = tracker.find_position(frame)

    controller.detect_gestures(lm_list)

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()