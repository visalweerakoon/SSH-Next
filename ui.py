import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QLabel
)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import QTimer, Qt

from ssh_client import SSHClient


def resource_path(path):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, path)


class Terminal(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptRichText(False)
        self.current_input = ""

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cmd = self.current_input.strip()
            self.current_input = ""
            if not cmd:
                self.parent.ssh.send("")
            else:
                self.parent.ssh.send(cmd)
            self.append("")
            return

        if event.key() == Qt.Key_Backspace:
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:-1]
                super().keyPressEvent(event)
            return

        text = event.text()
        if text and text.isprintable():
            self.current_input += text
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)


class SSHApp(QWidget):
    def __init__(self):
        super().__init__()

        self.ssh = SSHClient()

        self.setWindowTitle("SSH Next")
        self.setGeometry(200, 150, 900, 600)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.read_output)
        self.timer.start(100)

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QLineEdit {
                background-color: #181825;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 4px;
                padding: 4px;
            }
            QTextEdit {
                background-color: #181825;
                color: #a6e3a1; /* Green terminal letters */
                border: 1px solid #313244;
                border-radius: 4px;
                padding: 4px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #cba6f7;
            }
            QPushButton {
                background-color: #cba6f7;
                color: #11111b;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:pressed {
                background-color: #89b4fa;
            }
        """)

        layout = QVBoxLayout()

        self.host = QLineEdit()
        self.user = QLineEdit()
        self.password = QLineEdit()
        self.port = QLineEdit()

        self.password.setEchoMode(QLineEdit.Password)
        self.port.setText("22")

        self.host.setPlaceholderText("Host")
        self.user.setPlaceholderText("Username")
        self.password.setPlaceholderText("Password")
        self.port.setPlaceholderText("Port")

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_ssh)

        self.term = Terminal(self)

        layout.addWidget(QLabel("Host"))
        layout.addWidget(self.host)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.user)

        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)

        layout.addWidget(QLabel("Port"))
        layout.addWidget(self.port)

        layout.addWidget(self.connect_btn)
        layout.addWidget(self.term)

        self.setLayout(layout)

    def connect_ssh(self):
        result = self.ssh.connect(
            self.host.text(),
            self.user.text(),
            self.password.text(),
            self.port.text()
        )

        self.term.append(result)
        self.term.append("") # Row break

    def read_output(self):
        data = self.ssh.receive()

        if data:
            cursor = self.term.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.term.setTextCursor(cursor)
            self.term.insertPlainText(data)
            self.term.ensureCursorVisible()