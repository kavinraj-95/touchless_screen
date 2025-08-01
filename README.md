# Touchless Screen

# Gesture-Controlled Mouse Interface

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

## Setup

### 1. Install dependencies
```bash
chmod +x setup.sh
./setup.sh


