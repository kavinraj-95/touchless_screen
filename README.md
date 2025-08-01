# Touchless Screen

A real-time hand gesture-based mouse control system using a webcam, `MediaPipe`, and virtual input events via `uinput`.

## Components

### `main.py`
Entry point. Captures video, processes each frame, and links hand tracking with gesture-based mouse events.

### `hand_tracker.py`
Uses MediaPipe to detect and track hand landmarks. Locks onto a specific hand and provides its landmark positions.

### `gesture_controller.py`
Interprets hand landmark positions as mouse events:
- Cursor movement from index finger motion.
- Click-and-drag when thumb and index finger are close.
- Stops tracking and resets when no hand is detected.

## Requirements
- Python 3.7+
- OpenCV
- MediaPipe
- python-uinput (Linux only)

## Usage
1. Ensure webcam access.
2. Run `main.py`.
3. Use your hand in front of the camera:
   - Move index finger to move the cursor.
   - Pinch thumb and index finger to click and drag.
   - Spread fingers apart to release drag.

## Notes
- Designed for 1920x1080 screens. Edit `SCREEN_WIDTH/HEIGHT` in `gesture_controller.py` to match yours.
- Runs only on Linux due to `uinput`.
- Press `ESC` to quit.

## Limitations
- No multi-hand interaction.
- Accuracy degrades in poor lighting or occlusion.
- Not tested for accessibility use cases.

