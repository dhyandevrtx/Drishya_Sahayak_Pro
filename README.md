 
# Drishya Sahayak Pro - AI-Powered Assistive Device

Drishya Sahayak Pro is a professional-grade, AI-powered assistive system designed to enhance the independence and safety of visually impaired individuals. It uses real-time object detection, voice command control, and GPS navigation, all managed through a stable and responsive user interface.

## Features

- **Real-Time Object Detection:** Uses the powerful YOLOv8 model to identify objects, people, and potential hazards from a live camera feed.
- **Distance Estimation:** Provides approximate distances to detected objects to improve spatial awareness.
- **Voice-Activated Control:** A hands-free interface allows the user to interact with the system using voice commands.
- **GPS Navigation:** Fetches the current location and can provide directions (framework included).
- **Responsive GUI:** Built with PyQt5, the interface displays the camera feed and system status without freezing, thanks to robust multithreading.
- **Secure Configuration:** API keys and sensitive settings are kept out of the source code using a `.env` file.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Drishya_Sahayak_Pro

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


### 4. Download the YOLOv8 Model
Download the `yolov8n.pt` model weights and place it inside the `models/` directory. You can find it in the [YOLOv8 repository](https://github.com/ultralytics/ultralytics).

### 5. Configure API Keys
Create a file named `.env` in the root directory (`Drishya_Sahayak_Pro/`). This file will store your secret keys. Add the following, replacing the placeholders with your actual keys.

```env
# .env file

# (Optional) For GPS location services
# GEOPY_USER_AGENT="drishya_sahayak_pro"

