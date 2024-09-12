import pyautogui
import math
import mediapipe as mp

mpHands = mp.solutions.hands

def get_finger_positions(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP]
    return thumb_tip, index_tip, pinky_tip

def pinch_detected(thumb_tip, finger_tip, threshold=0.05):
    distance = math.sqrt(
        (finger_tip.x - thumb_tip.x) ** 2 +
        (finger_tip.y - thumb_tip.y) ** 2 +
        (finger_tip.z - thumb_tip.z) ** 2
    )
    return distance < threshold

def smooth_cursor_movement(prev_pos, current_pos, alpha=0.5):
    return (
        int(prev_pos[0] * (1 - alpha) + current_pos[0] * alpha),
        int(prev_pos[1] * (1 - alpha) + current_pos[1] * alpha)
    )

def control_cursor_and_click(hand_landmarks, prev_cursor_pos):
    thumb_tip, index_tip, pinky_tip = get_finger_positions(hand_landmarks)

    # Mirror the index finger tip position horizontally and/or vertically
    screen_width, screen_height = pyautogui.size()
    mirrored_x = screen_width - int(index_tip.x * screen_width)
    mirrored_y = int(index_tip.y * screen_height)

    # Smooth cursor movement
    smoothed_cursor_pos = smooth_cursor_movement(
        prev_cursor_pos,
        (mirrored_x, mirrored_y)
    )

    # Move cursor to the smoothed position
    pyautogui.moveTo(smoothed_cursor_pos[0], smoothed_cursor_pos[1])

    # Check for pinch gestures
    if pinch_detected(thumb_tip, index_tip):
        # Perform left click if thumb and index are pinched
        pyautogui.click(button='left')
    elif pinch_detected(thumb_tip, pinky_tip):
        # Perform right click if thumb and pinky are pinched
        pyautogui.click(button='right')

    return smoothed_cursor_pos