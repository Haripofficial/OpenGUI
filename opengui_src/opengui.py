import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QWidget, QScrollArea, QFrame, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import configparser
import os
import re

class OpenGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.config_file = 'config.ini'
        self.initUI()
        self.loadConfig()
        self.initTrayIcon()
        self.hide()
        
    def initUI(self):
        self.setWindowTitle('OpenGUI')
        self.setGeometry(100, 100, 620, 450)
        self.setStyleSheet("background-color: #ffffff;") # Set background color 
        
        # Central Widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        
        # Layout
        main_layout = QVBoxLayout(centralWidget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Header
        header = QLabel('OpenGUI', self)
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont('Arial', 24, QFont.Bold))
        header.setStyleSheet("color: #333333; margin-bottom: 20px;")
        main_layout.addWidget(header)
        
        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout2 = QHBoxLayout()
        
        # Run Command Button
        self.configViewButton = QPushButton('Config View', self)
        self.configViewButton.setFont(QFont('Arial', 12))
        self.configViewButton.setStyleSheet("""
            QPushButton {
                background-color: #0A1D56;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0F1035;
            }
        """)
        self.configViewButton.clicked.connect(self.configViewCommand)
        button_layout.addWidget(self.configViewButton)


        # Input Field for File Location
        self.fileInput = QLineEdit(self)
        self.fileInput.setPlaceholderText('Enter config file location')
        self.fileInput.setFont(QFont('Arial', 12))
        self.fileInput.setStyleSheet("""
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #666666;
            }
        """)

        # Start Command Button
        self.startButton = QPushButton('Start Session', self)
        self.startButton.setFont(QFont('Arial', 12))
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.startButton.clicked.connect(self.startCommand)
        button_layout2.addWidget(self.startButton)
        
        # Active Sessions Button
        self.activeSessionsButton = QPushButton('Active Sessions', self)
        self.activeSessionsButton.setFont(QFont('Arial', 12))
        self.activeSessionsButton.setStyleSheet("""
            QPushButton {
                background-color: #0A1D56;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0F1035;
            }
        """)
        self.activeSessionsButton.clicked.connect(self.showActiveSessions)
        button_layout.addWidget(self.activeSessionsButton)
        
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.fileInput)
        main_layout.addLayout(button_layout2)


        # Sessions Area
        self.sessionsArea = QScrollArea(self)
        self.sessionsArea.setWidgetResizable(True)
        self.sessionsContainer = QWidget()
        self.sessionsLayout = QVBoxLayout(self.sessionsContainer)
        self.sessionsContainer.setLayout(self.sessionsLayout)
        self.sessionsArea.setWidget(self.sessionsContainer)
        main_layout.addWidget(self.sessionsArea)
        self.sessionsArea.hide()


        # Output Field
        self.outputField = QTextEdit(self)
        self.outputField.setReadOnly(True)
        self.outputField.setFont(QFont('Arial', 12))
        self.outputField.setStyleSheet("""
            QTextEdit {
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                background-color: #f9f9f9;
            }
        """)
        # self.outputField.setFixedSize(600, 200)
        main_layout.addWidget(self.outputField)
        
        
        # Set layout to the central widget
        centralWidget.setLayout(main_layout)

            
    def initTrayIcon(self):
        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('openvpn.svg'))  # Set your icon path here
        
        # Create the tray menu
        tray_menu = QMenu()
        
        # Add an action to show the application
        show_action = QAction("Open", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        # Add an action to quit the application
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)
        
        # Set the tray menu
        self.tray_icon.setContextMenu(tray_menu)
        
        # Show the tray icon
        self.tray_icon.show()


    def closeEvent(self, event):
            self.hide()
            event.ignore()

    def configViewCommand(self):
        file_location = self.fileInput.text()
        self.outputField.show()
        self.fileInput.show()
        self.sessionsArea.hide()
        self.startButton.show()
        # Save the file location to the config file
        self.saveConfig(file_location)

        
    def startCommand(self):
        file_location = self.fileInput.text()
        self.outputField.show()
        self.fileInput.show()
        self.sessionsArea.hide()
        # Save the file location to the config file
        self.saveConfig(file_location)
        
        try:
            # Run the command in the host terminal
            result = subprocess.run(['openvpn3', 'session-start', '--config', file_location], capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)
        
        #Display the output in the output field
        self.outputField.setText(output)
    
    def showActiveSessions(self):
        try:
            # Run the openvpn3 sessions-list command
            result = subprocess.run(['openvpn3 sessions-list'], capture_output=True, text=True, shell=True)
            output = result.stdout + result.stderr
            self.sessionsArea.show()
            self.fileInput.hide()
            self.outputField.hide()
            self.startButton.hide()
            self.parseAndDisplaySessions(output)
        except Exception as e:
            output = str(e)
            self.outputField.setText(output)
    
    def parseAndDisplaySessions(self, output):
        # Clear previous session cards
        for i in reversed(range(self.sessionsLayout.count())): 
            widgetToRemove = self.sessionsLayout.itemAt(i).widget()
            self.sessionsLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
        
        # Split the output into sessions
        sessions = re.split(r'\n\s*\n', output.strip())
        for session in sessions:
            self.createSessionCard(session)
    
    def createSessionCard(self, session):
        card = QFrame(self)
        #card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                border: 1px solid #ffffff;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
                background-color: #F0F0F0;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Concatenate session details into a single label
        session_details = '\n'.join(re.split(r'\n\s*', session.strip()))
        label = QLabel(session_details, self)
        label.setFont(QFont('Arial', 10))
        layout.addWidget(label)
        
        stopButton = QPushButton('Stop Session', self)
        stopButton.setFont(QFont('Arial', 10))
        stopButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 5px;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        stopButton.clicked.connect(lambda _, s=session: self.stopSession(s))
        layout.addWidget(stopButton)
    
        self.sessionsLayout.addWidget(card)


    
    def stopSession(self, session):
        path_match = re.search(r'Path: (\S+)', session)
        if path_match:
            path = path_match.group(1)
            try:
                result = subprocess.run([f'openvpn3 session-manage --session-path {path} --disconnect'], capture_output=True, text=True, shell=True)
                output = result.stdout + result.stderr
                self.outputField.setText(output)
                self.showActiveSessions()  # Refresh the session list
            except Exception as e:
                output = str(e)
                self.outputField.setText(output)
    
    def saveConfig(self, file_location):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'file_location': file_location}
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)
    
    def loadConfig(self):
        if os.path.exists(self.config_file):
            config = configparser.ConfigParser()
            config.read(self.config_file)
            self.fileInput.setText(config['DEFAULT'].get('file_location', ''))

def main():
    app = QApplication(sys.argv)
    window = OpenGUI()
    # Do not call window.show() here to prevent the main window from showing initially
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

