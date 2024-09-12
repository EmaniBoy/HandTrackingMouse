import math
import pyautogui
import mediapipe as mp

mpHands = mp.solutions.hands


def get_pinky_and_thumb_positions(hand_landmarks):
    pinky_tip = hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP]
    thumb_tip = hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP]
    return pinky_tip, thumb_tip


def calculate_distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2 +
        (point1.z - point2.z) ** 2
    )


def control_zoom(hand_landmarks, previous_distance=None, zoom_sensitivity=50):
    pinky_tip, thumb_tip = get_pinky_and_thumb_positions(hand_landmarks)

    current_distance = calculate_distance(pinky_tip, thumb_tip)

    if previous_distance is not None:
        zoom_change = (current_distance - previous_distance) * zoom_sensitivity
        if zoom_change > 0:
            pyautogui.hotkey('ctrl', '+')  # Zoom in
        elif zoom_change < 0:
            pyautogui.hotkey('ctrl', '-')  # Zoom out

    return current_distance