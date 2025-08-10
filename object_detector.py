import cv2
from ultralytics import YOLO
from config import Config
class ObjectDetector:
    """
    Handles object detection using the YOLOv8 model.
    """
    def __init__(self, model_path=Config.MODEL_PATH):
        self.model = YOLO(model_path)
        # Known width of objects in meters for distance estimation (example values)
        self.known_widths = {
            'person': 0.5,
            'car': 1.8,
            'bicycle': 1.0,
            'motorbike': 0.8
        }

    def detect_and_draw(self, frame):
        """
        Detects objects in a frame, draws bounding boxes, and returns detections.
        """
        results = self.model(frame, verbose=False)
        detected_objects = []

        for result in results:
            for box in result.boxes:
                confidence = box.conf[0]
                if confidence < Config.DETECTION_CONFIDENCE_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                label = self.model.names[class_id]

                # Estimate distance
                distance_str = self._estimate_distance(x2 - x1, label)

                # Append detected object info
                detected_objects.append(f"{label} at {distance_str}")

                # Draw on frame
                display_text = f"{label} ({distance_str})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, display_text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return frame, detected_objects

    def _estimate_distance(self, object_pixel_width, label):
        """
        A simple model for distance estimation.
        Requires calibration for accuracy.
        """
        known_width = self.known_widths.get(label)
        if known_width is None:
            return "unknown distance"

        # This is a placeholder focal length. You MUST calibrate this.
        # To calibrate: Hold an object of known width at a known distance.
        # Focal_Length = (Pixel_Width * Known_Distance) / Known_Width
        focal_length = 800
        
        try:
            distance = (known_width * focal_length) / object_pixel_width
            return f"{distance:.2f}m"
        except ZeroDivisionError:
            return "unknown distance"
