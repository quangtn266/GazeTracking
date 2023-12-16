"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking


def visualization_state(frame, text, color):
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 3.2, color, 2)


def visualization_eyes(frame, left_pupil, right_pupil):
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

if __name__ == "__main__":

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_v2.mov', fourcc, 10.0, (1080, 720))
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_drowsy() == "Drowsy":
            text = "Drowsiness"
            color = (15, 255, 255)
            visualization_state(frame, text, color)

        elif gaze.is_blinking() == "Blinking":
            text = "Drowsiness"
            visualization_state(frame, text, color)
        elif gaze.is_right() or gaze.is_left():
            text = "Inattentive"
            color = (147, 58, 31)
            visualization_state(frame, text, color)
        elif gaze.is_center():
            text = " "

        frame = cv2.resize(frame, (1080, 720))
        out.write(frame)
        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    out.release()
    webcam.release()
    cv2.destroyAllWindows()