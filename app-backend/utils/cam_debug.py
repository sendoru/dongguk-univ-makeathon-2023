import cv2
import picamera2
import numpy as np
from PIL import Image

# Initialize the webcam. 0 indicates the default camera (usually the built-in webcam).
# You can specify a different camera by changing the index.
picam2 = picamera2.Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
picam2.start()

while True:
    # Read a frame from the webcam
    frame = np.array(picam2.capture_image())
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame
    cv2.imshow("Webcam", frame)

    # Break the loop if the 'q' key is pressed (to exit the program)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows when done
cv2.destroyAllWindows()