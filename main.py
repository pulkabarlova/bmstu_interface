import sys
import sqlite3
import random
from threading import *
import time
import cv2
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.uic.properties import QtCore, QtWidgets
from u2_file import Ui_Form
import numpy
from ui_file import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_bmstu.ui', self)
        self.setupUi(self)
        self.registration.clicked.connect(self.on_registration)
        self.login.clicked.connect(self.on_login)
        self.group.hide()
        self.group_label.hide()
        self.fio.hide()
        self.fio_label.hide()
        self.toregister.hide()
        pixmap = QPixmap('gerb_mgtu.png')
        pixmap = pixmap.scaled(QSize(70, 70), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.mgtu_logo.setPixmap(pixmap)
        self.toregister.clicked.connect(self.on_toregister)

    def on_registration(self):
        self.first_timelabel.hide()
        self.login.hide()
        self.fio.show()
        self.fio_label.show()
        self.group_label.show()
        self.group.show()
        self.registration.hide()
        self.toregister.show()

    def on_login(self):
        connection = sqlite3.connect('db_bmstu.db')
        cur = connection.cursor()
        user_address = self.address.toPlainText()
        user_password = self.password.toPlainText()
        cur.execute("SELECT email FROM users")
        addresses = [i[0] for i in cur.fetchall()]
        cur.execute("SELECT password FROM users")
        passwords = [i[0] for i in cur.fetchall()]
        if user_address in addresses:
            if passwords[addresses.index(user_address)] == user_password:
                second_window.show()
                self.hide()
            else:
                self.password_label.setText("Неверный пароль")
        else:
            self.address_label.setText("Такой поты нет в базе данных")

    def on_toregister(self):
        user_email = self.address.toPlainText()
        user_password = self.password.toPlainText()
        user_group_name = self.group.toPlainText()
        user_mane = self.fio.toPlainText().split()[1]
        user_surname = self.fio.toPlainText().split()[0]
        user_fathername = self.fio.toPlainText().split()[2]

        connection = sqlite3.connect('db_bmstu.db')
        cur = connection.cursor()
        cur.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                group_number TEXT NOT NULL,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                fathername TEXT NOT NULL
                )
                ''')
        cur.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (1, user_email, user_password, user_group_name,
                     user_mane, user_surname, user_fathername))
        connection.commit()
        connection.close()


class SecondWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        uic.loadUi('u2_bmstu.ui', self)
        self.setupUi(self)
        self.video_capture = cv2.VideoCapture(0)
        self.width = 640
        self.height = 480
        self.video_capture.set(3, self.width)
        self.video_capture.set(4, self.height)
        self.recording = False

        self.start_button.clicked.connect(self.toggle_recording)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.end_button.clicked.connect(self.closeeven)
        self.timer.start(33)

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter('output.mp4', fourcc, 30, (self.width, self.height))
        else:
            if hasattr(self, 'video_writer'):
                self.video_writer.release()

    def update_frame(self):
        _, frame = self.video_capture.read()
        if frame is not None and not (frame.size == 0):  # Check if the frame is valid
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            h, w, ch = rgb_frame.shape  # Retrieve height, width, and number of channels
            bytes_per_line = ch * w  # Calculate bytes per line
            convert_to_qt_format = QImage(rgb_frame.data, w, h, bytes_per_line,
                                          QImage.Format_RGB888)  # Convert to QImage format
            pixmap = QPixmap.fromImage(convert_to_qt_format)  # Convert to QPixmap
            self.video_frame.setPixmap(pixmap)  # Display the frame
        if self.recording:
            self.video_writer.write(frame)

    def closeeven(self):
        self.video_capture.release()
        if hasattr(self, 'video_writer'):
            self.video_writer.release()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    second_window = SecondWindow()
    second_window.close()
    sys.exit(app.exec_())
