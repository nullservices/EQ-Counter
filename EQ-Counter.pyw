import os
import time
from threading import Thread
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QWidget,
    QFileDialog,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from datetime import datetime


# Real-Time Log Monitoring Class
class LogMonitor:
    def __init__(self, log_file, aa_callback, slain_callback):
        self.log_file = log_file
        self.aa_callback = aa_callback
        self.slain_callback = slain_callback
        self.running = False
        self.last_position = 0

    def start(self):
        self.running = True
        self.last_position = os.path.getsize(self.log_file)
        Thread(target=self.monitor, daemon=True).start()

    def stop(self):
        self.running = False

    def monitor(self):
        while self.running:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()

                for line in new_lines:
                    if "You have gained an ability point!" in line:
                        self.aa_callback()
                    elif "You have slain" in line:
                        self.slain_callback()

            time.sleep(0.5)


# GUI Application
class MonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.log_file = None
        self.aa_count = 0
        self.slain_count = 0
        self.start_time = None
        self.monitor = None

        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()

        # Title
        self.title_label = QLabel("Ability Point & Monster Tracker")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label, 0, 0, 1, 2)

        # AA Points Counter
        self.aa_label = QLabel(f"AA Points Gained: {self.aa_count}")
        self.aa_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.aa_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.aa_label, 1, 0)

        # Monsters Slain Counter
        self.slain_label = QLabel(f"Monsters Slain: {self.slain_count}")
        self.slain_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.slain_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.slain_label, 1, 1)

        # AA Points Per Hour Label
        self.aa_rate_label = QLabel("AA Points Per Hour: 0.0")
        self.aa_rate_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.aa_rate_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.aa_rate_label, 2, 0, 1, 2)

        # Select Log File Button
        self.select_file_button = QPushButton("Select Log File")
        self.select_file_button.clicked.connect(self.select_log_file)
        self.layout.addWidget(self.select_file_button, 3, 0, 1, 2)

        # Start Monitoring Button
        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.start_monitoring)
        self.start_button.setEnabled(False)
        self.layout.addWidget(self.start_button, 4, 0)

        # Stop Monitoring Button
        self.stop_button = QPushButton("Stop Monitoring")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button, 4, 1)

        # Reset Counts Button
        self.reset_button = QPushButton("Reset Counts")
        self.reset_button.clicked.connect(self.reset_counts)
        self.layout.addWidget(self.reset_button, 5, 0, 1, 2)

        # Reset AA Per Hour Button
        self.reset_rate_button = QPushButton("Reset AA Per Hour")
        self.reset_rate_button.clicked.connect(self.reset_aa_rate)
        self.layout.addWidget(self.reset_rate_button, 6, 0, 1, 2)

        # Status Label
        self.status_label = QLabel("Select a log file to start.")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label, 7, 0, 1, 2)

        self.setLayout(self.layout)

        # Apply styling
        self.setStyleSheet(
            """
            QWidget {
                background-color: #2E2E2E;
                color: #E0E0E0;
            }
            QLabel {
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:disabled {
                background-color: #888888;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            """
        )

        self.setWindowTitle("Ability Point & Monster Tracker")
        self.resize(400, 300)
        self.show()

    def select_log_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Log File", "", "Log Files (*.txt);;All Files (*)")

        if file_path:
            self.log_file = file_path
            self.status_label.setText(f"Log File Selected: {self.log_file}")
            self.start_button.setEnabled(True)

    def update_aa_counter(self):
        self.aa_count += 1
        self.aa_label.setText(f"AA Points Gained: {self.aa_count}")
        self.update_aa_rate()
        self.write_to_file()

    def update_slain_counter(self):
        self.slain_count += 1
        self.slain_label.setText(f"Monsters Slain: {self.slain_count}")
        self.write_to_file()

    def reset_counts(self):
        self.aa_count = 0
        self.slain_count = 0
        self.start_time = None
        self.aa_label.setText(f"AA Points Gained: {self.aa_count}")
        self.slain_label.setText(f"Monsters Slain: {self.slain_count}")
        self.aa_rate_label.setText("AA Points Per Hour: 0.0")
        self.write_to_file()

    def reset_aa_rate(self):
        self.start_time = datetime.now()
        self.aa_rate_label.setText("AA Points Per Hour: 0.0")
        self.status_label.setText("AA Points Per Hour Reset")
        self.write_to_file()

    def update_aa_rate(self):
        if not self.start_time:
            self.start_time = datetime.now()
        elapsed_time = (datetime.now() - self.start_time).total_seconds() / 3600
        rate = self.aa_count / elapsed_time if elapsed_time > 0 else 0
        self.aa_rate_label.setText(f"AA Points Per Hour: {rate:.2f}")

    def write_to_file(self):
        with open("ability_points.txt", "w") as f:
            f.write(f"AA Points Gained: {self.aa_count}\n")
            f.write(f"Monsters Slain: {self.slain_count}\n")
            elapsed_time = (datetime.now() - self.start_time).total_seconds() / 3600 if self.start_time else 0
            rate = self.aa_count / elapsed_time if elapsed_time > 0 else 0
            f.write(f"AA Points Per Hour: {rate:.2f}")

    def start_monitoring(self):
        if self.log_file and not self.monitor:
            self.monitor = LogMonitor(self.log_file, self.update_aa_counter, self.update_slain_counter)
            self.monitor.start()
            self.start_time = datetime.now()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText("Monitoring Started!")

    def stop_monitoring(self):
        if self.monitor:
            self.monitor.stop()
            self.monitor = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Monitoring Stopped!")


def main():
    app = QApplication(sys.argv)
    ex = MonitorApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
