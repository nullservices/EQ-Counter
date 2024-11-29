import os
import time
from threading import Thread
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QWidget, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys


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
        # Start at the end of the file to skip historical data
        self.last_position = os.path.getsize(self.log_file)
        Thread(target=self.monitor, daemon=True).start()

    def stop(self):
        self.running = False

    def monitor(self):
        while self.running:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                f.seek(self.last_position)  # Move to the last known position
                new_lines = f.readlines()
                self.last_position = f.tell()  # Update the position

                for line in new_lines:
                    print(f"[DEBUG] New line detected: {line.strip()}")  # Debugging
                    if "You have gained an ability point!" in line:
                        print("[DEBUG] Match found for AA point!")  # Debugging
                        self.aa_callback()
                    elif "You have slain" in line:
                        print("[DEBUG] Match found for slain monster!")  # Debugging
                        self.slain_callback()

            time.sleep(0.5)  # Small delay to prevent excessive CPU usage


# GUI Application
class MonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.log_file = None
        self.aa_count = 0
        self.slain_count = 0
        self.monitor = None

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Large AA Points Counter Display Label
        self.aa_label = QLabel(f"AA Points Gained: {self.aa_count}", self)
        self.aa_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.aa_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.aa_label)

        # Large Monsters Slain Counter Display Label
        self.slain_label = QLabel(f"Monsters Slain: {self.slain_count}", self)
        self.slain_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.slain_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.slain_label)

        # Select Log File Button
        self.select_file_button = QPushButton("Select Log File", self)
        self.select_file_button.clicked.connect(self.select_log_file)
        self.layout.addWidget(self.select_file_button)

        # Start Monitoring Button
        self.start_button = QPushButton("Start Monitoring", self)
        self.start_button.clicked.connect(self.start_monitoring)
        self.start_button.setEnabled(False)  # Disabled until log file is selected
        self.layout.addWidget(self.start_button)

        # Stop Monitoring Button
        self.stop_button = QPushButton("Stop Monitoring", self)
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)  # Disabled initially
        self.layout.addWidget(self.stop_button)

        # Reset Counters Button
        self.reset_button = QPushButton("Reset Counts", self)
        self.reset_button.clicked.connect(self.reset_counts)
        self.layout.addWidget(self.reset_button)

        # Status Label
        self.status_label = QLabel("Select a log file to start.", self)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)
        self.setWindowTitle("Ability Point and Monster Counter")
        self.show()

    def select_log_file(self):
        # Open file dialog to select the log file
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Log File", "", "Log Files (*.log);;All Files (*)")

        if file_path:
            self.log_file = file_path
            self.status_label.setText(f"Log File Selected: {self.log_file}")
            self.start_button.setEnabled(True)  # Enable start button once file is selected

    def update_aa_counter(self):
        self.aa_count += 1
        self.aa_label.setText(f"AA Points Gained: {self.aa_count}")
        self.write_to_file()
        print(f"[DEBUG] AA Points Counter updated: {self.aa_count}")  # Debugging

    def update_slain_counter(self):
        self.slain_count += 1
        self.slain_label.setText(f"Monsters Slain: {self.slain_count}")
        self.write_to_file()
        print(f"[DEBUG] Monsters Slain Counter updated: {self.slain_count}")  # Debugging

    def reset_counts(self):
        self.aa_count = 0
        self.slain_count = 0
        self.aa_label.setText(f"AA Points Gained: {self.aa_count}")
        self.slain_label.setText(f"Monsters Slain: {self.slain_count}")
        self.write_to_file()
        self.status_label.setText("Counts reset.")
        print("[DEBUG] Counters reset.")

    def write_to_file(self):
        # Write the formatted message to the output file
        with open("ability_points.txt", "w") as f:
            f.write(f"AA Points Gained: {self.aa_count}\n")
            f.write(f"Monsters Slain: {self.slain_count}")

    def start_monitoring(self):
        if self.log_file and not self.monitor:
            self.monitor = LogMonitor(self.log_file, self.update_aa_counter, self.update_slain_counter)
            self.monitor.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText("Monitoring Started!")
            print(f"[DEBUG] Monitoring started on file: {self.log_file}")

    def stop_monitoring(self):
        if self.monitor:
            self.monitor.stop()
            self.monitor = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Monitoring Stopped!")
            print("[DEBUG] Monitoring stopped.")

    def closeEvent(self, event):
        if self.monitor:
            self.monitor.stop()
        event.accept()


# Main Application Function
def main():
    app = QApplication(sys.argv)
    ex = MonitorApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
