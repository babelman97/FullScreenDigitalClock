import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from babel.dates import format_time
from datetime import datetime
import pytz

class FullScreenClock(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('Full Screen Digital Clock')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(245, 245, 245))  # Light gray
        self.setPalette(palette)

        # Set up the clock label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.font_size = 240  # Default font size
        self.label.setFont(QFont('Arial', self.font_size))
        self.label.setStyleSheet("color: black;")  # Black font color

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        # Update time initially
        self.update_time()

    def update_time(self):
        # Get current time in Taipei timezone
        taipei_tz = pytz.timezone('Asia/Taipei')
        current_time = datetime.now(taipei_tz)
        # Format time using Babel with "HH:mm:ss"
        formatted_time = format_time(current_time, format='HH:mm:ss', locale='zh_TW')
        self.label.setText(formatted_time)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.confirm_exit()
        elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
            self.change_font_size(10)
        elif event.key() == Qt.Key_Minus:
            self.change_font_size(-10)
        elif Qt.Key_1 <= event.key() <= Qt.Key_9:
            self.switch_screen(event.key() - Qt.Key_0)

    def change_font_size(self, delta):
        self.font_size += delta
        if self.font_size < 10:
            self.font_size = 10
        self.label.setFont(QFont('Arial', self.font_size))

    def confirm_exit(self):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def switch_screen(self, screen_number):
        desktop = QDesktopWidget()
        screen_count = desktop.screenCount()
        if 1 <= screen_number <= screen_count:
            screen_geometry = desktop.screenGeometry(screen_number - 1)
            self.move(screen_geometry.topLeft())
            self.resize(screen_geometry.width(), screen_geometry.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = FullScreenClock()
    clock.show()
    sys.exit(app.exec_())
