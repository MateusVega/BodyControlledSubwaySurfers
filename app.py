import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_areas(image, w, h):
    # Draw vertical areas
    cv2.line(image, (int(w/3), 0), (int(w/3), h), (0, 0, 255), 2)
    cv2.line(image, (int(w*2/3), 0), (int(w*2/3), h), (0, 0, 255), 2)
    # Draw horizontal areas
    cv2.line(image, (0, int(h/3)), (w, int(h/3)), (255, 0, 0), 2)
    cv2.line(image, (0, int(2*h/3)), (w, int(2*h/3)), (255, 0, 0), 2)

lhand_down = None
rhand_down = None

def control_hands(lhand, rhand, h):
    global lhand_down, rhand_down
    if lhand[1] < h/3 and lhand_down:
        lhand_down = False
        pyautogui.click()
    if lhand[1] >= h/3:
        lhand_down = True

    if rhand[1] < h/3 and rhand_down:
        rhand_down = False
        pyautogui.press('space')
    if rhand[1] >= h/3:
        rhand_down = True

can_jump = None
can_crouch = None
stage = "center"
last_stage = "center"

def control_mov(center, w, h):
    global can_jump, can_crouch, stage, last_stage
    if center[1] < h/3 and can_jump:
        pyautogui.press('up')
        can_jump = False
    elif center[1] > h*2/3 and can_crouch:
        pyautogui.press('down')
        can_crouch = False
    elif center[1] > h/3 and center[1] < h*2/3:
        can_jump = True
        can_crouch = True

    last_stage = stage
    if center[0] < w/3:
        stage = "left"
    elif center[0] > 2*w/3:
        stage = "right"
    else:
        stage = "center"

    if last_stage != stage:
        if (last_stage == "center" and stage == "left") or (last_stage == "right" and stage == "center"):
            pyautogui.press('left')
        elif (last_stage == "center" and stage == "right") or (last_stage == "left" and stage == "center"):
            pyautogui.press('right')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3, smooth_landmarks=True, static_image_mode=False, model_complexity=0) as pose:
    while cap.isOpened():
        cap.grab()
        ret, frame = cap.retrieve()
        frame = cv2.flip(frame, 1)

        zoom_factor = 1.2
        
        height, width = frame.shape[:2]
        
        new_height = int(height / zoom_factor)
        new_width = int(width / zoom_factor)
        
        # Calculate the bounding box for cropping (centered)
        y1 = int((height - new_height) / 2)
        y2 = y1 + new_height
        x1 = int((width - new_width) / 2)
        x2 = x1 + new_width
        
        # Crop the frame and resize it back to the original size
        cropped = frame[y1:y2, x1:x2]
        frame = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LINEAR)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        h, w, _ = image.shape

        try:
            landmarks = results.pose_landmarks.landmark
            
            left_shoulder = [landmarks[11].x, landmarks[11].y]
            right_shoulder = [landmarks[12].x, landmarks[12].y]

            cx = (left_shoulder[0] + right_shoulder[0])/2
            cy = (left_shoulder[1] + right_shoulder[1])/2
            center = (int(cx * w), int(cy * h - 10))

            left_hand = (int(landmarks[16].x * w), int(landmarks[16].y * h))
            right_hand = (int(landmarks[15].x * w), int(landmarks[15].y * h))

            control_hands(left_hand, right_hand, h)
            control_mov(center, w, h)

            cv2.circle(image, center, 3, (255,255,255), -1)
            cv2.circle(image, left_hand, 3, (0, 255, 0), -1)
            cv2.circle(image, right_hand, 3, (0, 255, 0), -1)
            
        except Exception as e:
            pass
            #print(type(e).__name__, e)

        draw_areas(image, w, h)

        """
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(244,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2),
        )
        """
        cv2.imshow('Mediapipe', image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()