import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to hold all settings and API keys.
    """
    # --- Voice Assistant Settings ---
    WAKE_WORD = "sahayak"
    LISTENING_TIMEOUT = 5  # seconds

    # --- Camera Settings ---
    CAMERA_INDEX = 0  # 0 for default webcam
    CAMERA_FPS = 30

    # --- Object Detection Settings ---
    MODEL_PATH = 'models/yolov8n.pt'
    DETECTION_CONFIDENCE_THRESHOLD = 0.5

    # --- GPS Settings ---
    GEOPY_USER_AGENT = os.getenv("GEOPY_USER_AGENT", "drishya_sahayak_default")
    
    # --- GUI Settings ---
    APP_TITLE = "Drishya Sahayak Pro" 
