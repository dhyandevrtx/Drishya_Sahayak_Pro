import sys
import cv2
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QImage

from app.gui import DrishyaSahayakApp
from app.object_detector import ObjectDetector
from app.voice_assistant import VoiceAssistant
from app.navigation import Navigation
from config import Config

class VideoThread(QObject):
    """
    A dedicated thread to handle video capture and processing.
    This prevents the GUI from freezing.
    """
    frame_ready = pyqtSignal(QImage)
    objects_detected_signal = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.detector = ObjectDetector()

    def run(self):
        """Main loop for the video thread."""
        cap = cv2.VideoCapture(Config.CAMERA_INDEX)
        if not cap.isOpened():
            print("Error: Cannot open camera.")
            return

        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                continue

            # Process the frame for object detection
            processed_frame, detected_objects = self.detector.detect_and_draw(frame)
            
            # Announce new, significant objects
            if detected_objects:
                self.objects_detected_signal.emit(detected_objects)

            # Convert frame for Qt display
            rgb_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.frame_ready.emit(qt_image.copy())

        cap.release()
        print("Video thread stopped.")

    def stop(self):
        self.is_running = False

class MainController:
    """
    The main controller that connects the GUI, AI modules, and threads.
    """
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.gui = DrishyaSahayakApp()
        self.voice_assistant = VoiceAssistant()
        self.navigation = Navigation()

        self.is_system_active = False
        self.last_announced = {} # To avoid spamming announcements
        self.announce_lock = threading.Lock()

        # --- Threading Setup ---
        self.video_thread_instance = None
        self.video_worker = None

        self._connect_signals()
        self.gui.show()

    def _connect_signals(self):
        """Connect all signals and slots."""
        self.gui.start_stop_button.clicked.connect(self.toggle_system)
        self.gui.exit_button.clicked.connect(self.shutdown)
    
    def toggle_system(self):
        if not self.is_system_active:
            self.start_system()
        else:
            self.stop_system()

    def start_system(self):
        """Starts the video and voice recognition threads."""
        self.is_system_active = True
        self.gui.update_status("System starting...")
        self.gui.start_stop_button.setText("Stop System")

        # Start Video Thread
        self.video_thread_instance = QThread()
        self.video_worker = VideoThread()
        self.video_worker.moveToThread(self.video_thread_instance)
        
        self.video_worker.frame_ready.connect(self.gui.update_video_frame)
        self.video_worker.objects_detected_signal.connect(self.handle_detections)
        
        self.video_thread_instance.started.connect(self.video_worker.run)
        self.video_thread_instance.start()

        # Start Voice Command Thread
        self.voice_thread = threading.Thread(target=self.listen_for_voice_commands, daemon=True)
        self.voice_thread.start()
        
        self.voice_assistant.speak("Drishya Sahayak is now active.")
        self.gui.update_status("Running")

    def stop_system(self):
        """Stops all running threads gracefully."""
        if not self.is_system_active:
            return
            
        self.is_system_active = False
        self.gui.update_status("System stopping...")
        
        # Stop video worker and thread
        if self.video_worker:
            self.video_worker.stop()
        if self.video_thread_instance:
            self.video_thread_instance.quit()
            self.video_thread_instance.wait()

        self.gui.start_stop_button.setText("Start System")
        self.gui.update_status("Idle")
        self.gui.video_label.setText("System Off")
        self.voice_assistant.speak("System deactivated.")

    def handle_detections(self, detected_objects):
        """Processes detections from the video thread to announce them."""
        with self.announce_lock:
            if not self.is_system_active:
                return
            
            # Simple logic to announce only the most significant object
            if detected_objects:
                # Announce the first detected object as an example
                announcement = detected_objects[0]
                # Avoid re-announcing the same thing immediately
                if self.last_announced.get("last") != announcement:
                    self.voice_assistant.speak(announcement)
                    self.last_announced["last"] = announcement

    def listen_for_voice_commands(self):
        """Dedicated thread loop for listening to voice commands."""
        while self.is_system_active:
            command = self.voice_assistant.listen_for_command()
            if command:
                self.process_command(command)

    def process_command(self, command):
        """Executes actions based on the recognized voice command."""
        self.gui.update_status(f"Command: {command}")
        if "where am i" in command:
            self.voice_assistant.speak("Checking your location.")
            location = self.navigation.get_current_location()
            self.voice_assistant.speak(location)
        elif "what's in front of me" in command:
             # The system is already announcing this. Could add a summary feature.
             self.voice_assistant.speak("Describing surroundings now.")
        elif "stop" in command or "exit" in command:
            self.stop_system()
        else:
            self.voice_assistant.speak("Sorry, I didn't recognize that command.")
        
        if self.is_system_active:
            self.gui.update_status("Running")

    def shutdown(self):
        """Properly shuts down the entire application."""
        self.stop_system()
        QApplication.instance().quit()

if __name__ == "__main__":
    controller = MainController()
    sys.exit(controller.app.exec_())
