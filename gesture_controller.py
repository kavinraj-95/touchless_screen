import math
import uinput

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

events = (
    uinput.ABS_X + (0, SCREEN_WIDTH, 0, 0),
    uinput.ABS_Y + (0, SCREEN_HEIGHT, 0, 0),
    uinput.BTN_LEFT,
)
device = uinput.Device(events)


class GestureController:
    def __init__(self, sensitivity=2.5, dead_zone=5):
        self.prev_finger_pos = None
        self.sensitivity = sensitivity
        self.dead_zone = dead_zone
        self.dragging = False
        self.cursor_x = SCREEN_WIDTH // 2
        self.cursor_y = SCREEN_HEIGHT // 2

    @staticmethod
    def distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.hypot(x2 - x1, y2 - y1)

    def move_cursor_relative(self, current_pos):
        if self.prev_finger_pos is None:
            self.prev_finger_pos = current_pos
            return

        dx = (current_pos[0] - self.prev_finger_pos[0]) * self.sensitivity
        dy = (current_pos[1] - self.prev_finger_pos[1]) * self.sensitivity

        if abs(dx) < self.dead_zone and abs(dy) < self.dead_zone:
            return

        self.cursor_x += int(dx)
        self.cursor_y += int(dy)

        self.cursor_x = max(0, min(SCREEN_WIDTH, self.cursor_x))
        self.cursor_y = max(0, min(SCREEN_HEIGHT, self.cursor_y))

        device.emit(uinput.ABS_X, self.cursor_x, syn=False)
        device.emit(uinput.ABS_Y, self.cursor_y)

        self.prev_finger_pos = current_pos

    def click_and_drag(self):
        if not self.dragging:
            device.emit(uinput.BTN_LEFT, 1)
            device.emit(uinput.BTN_LEFT, 1)
            self.dragging = True

    def release_drag(self):
        if self.dragging:
            device.emit(uinput.BTN_LEFT, 0)  # Release
            self.dragging = False

    def open_file(self):
        device.emit_click(uinput.BTN_LEFT)  # Simple click

    def detect_gestures(self, landmarks):
        if not landmarks:
            self.prev_finger_pos = None
            self.release_drag()
            return

        index_tip = (landmarks[8][1], landmarks[8][2])
        middle_tip = (landmarks[12][1], landmarks[12][2])
        thumb_tip = (landmarks[4][1], landmarks[4][2])

        index_middle_dist = self.distance(index_tip, middle_tip)
        index_thumb_dist = self.distance(index_tip, thumb_tip)

        if index_middle_dist < 40:
            self.move_cursor_relative(index_tip)

        if index_thumb_dist < 40:
            self.click_and_drag()
        else:
            self.release_drag()
