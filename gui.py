import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt

class DrishyaSahayakApp(QMainWindow):
    """
    The main GUI window for the application.
    It is designed to be controlled by the MainController.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drishya Sahayak Pro")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # --- Video Display Label ---
        self.video_label = QLabel("Initializing Camera...", self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black; color: white;")
        self.layout.addWidget(self.video_label, stretch=1)

        # --- Status & Control Layout ---
        control_layout = QHBoxLayout()
        self.status_label = QLabel("Status: Idle", self)
        self.status_label.setFont(QFont("Arial", 12))
        control_layout.addWidget(self.status_label, stretch=1)
        
        self.start_stop_button = QPushButton("Start System", self)
        self.start_stop_button.setFont(QFont("Arial", 12))
        control_layout.addWidget(self.start_stop_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFont(QFont("Arial", 12))
        self.exit_button.clicked.connect(self.close)
        control_layout.addWidget(self.exit_button)

        self.layout.addLayout(control_layout)

    def update_video_frame(self, q_image):
        """Updates the video label with a new QImage."""
        self.video_label.setPixmap(QPixmap.fromImage(q_image))

    def update_status(self, message):
        """Updates the status bar text."""
        self.status_label.setText(f"Status: {message}")

    def closeEvent(self, event):
        """Handle the window close event."""
        print("GUI closing signal sent.")
        # The main controller will catch this and shut down threads gracefully.
        super().closeEvent(event)
