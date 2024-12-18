import cv2
from ultralytics import YOLO
import numpy as np

def detect_pests():
    model = YOLO('./models/yolov8n.pt')

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame)
        
        annotated_frame = results[0].plot()
        
        cv2.imshow('Pest Detection', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_pests()