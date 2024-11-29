
Ability Point & Monster Tracker
A sleek and modern application for monitoring Ability Points Gained and Monsters Slain from your game logs in real time. Perfect for streamers who want to display this information on their streams or players who want to keep track of their progress.

Features
Real-time Log Monitoring:
Tracks Ability Points Gained and Monsters Slain from your game logs.
Live Counter Display:
Displays the counts in a modern, intuitive GUI.
Stream Integration:
Outputs the data to ability_points.txt for use with OBS or other streaming software.
User-Friendly Interface:
Stylish, responsive GUI with easy-to-use controls.
Installation
Prerequisites
Ensure you have Python 3.8+ installed on your system. Download it from python.org.

Installation Steps
Clone the repository or download the ZIP:

bash
Copy code
git clone https://github.com/your-username/ability-point-tracker.git
cd ability-point-tracker
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python app.py
Usage
Select Your Log File:

Choose the log file to monitor from the application.
Start Monitoring:

Click the Start Monitoring button to begin tracking in real time.
Reset Counts:

Use the Reset Counts button to reset both counters.
Output File:

The live counters are saved to ability_points.txt in the format:
yaml
Copy code
AA Points Gained: 5
Monsters Slain: 12
Add this file as a text source in OBS to display it on your stream.

Requirements
Python 3.8+
Required Python libraries (installed automatically):
PyQt5
Other dependencies in requirements.txt
Contributing
We welcome contributions! Feel free to submit a pull request or report issues.

License
This project is licensed under the MIT License.

Contact
For questions or support, open an issue on GitHub or email us at your-email@example.com.
