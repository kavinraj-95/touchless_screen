import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=2, detection_conf=0.7, track_conf=0.7):
        self.max_hands = max_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=track_conf
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.locked_hand_landmarks = None  # Store locked hand landmarks

    def find_hands(self, frame, draw=True):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
            if self.locked_hand_landmarks is None:
                # Lock onto the first detected hand
                self.locked_hand_landmarks = self.results.multi_hand_landmarks[0]
            else:
                matched = False
                for handLms in self.results.multi_hand_landmarks:
                    locked_tip = self.locked_hand_landmarks.landmark[8]  # Index fingertip
                    new_tip = handLms.landmark[8]
                    dist = ((locked_tip.x - new_tip.x) ** 2 + (locked_tip.y - new_tip.y) ** 2) ** 0.5
                    if dist < 0.1:  # Threshold for considering same hand
                        self.locked_hand_landmarks = handLms
                        matched = True
                        break
                if not matched:
                    # Lost locked hand; clear lock
                    self.locked_hand_landmarks = None

            if draw and self.locked_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, self.locked_hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        else:
            # No hands detected; clear lock
            self.locked_hand_landmarks = None

        return frame

    def find_position(self, frame):
        landmark_list = []
        if self.locked_hand_landmarks:
            hand = self.locked_hand_landmarks
            for id, lm in enumerate(hand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append((id, cx, cy))
        return landmark_list
