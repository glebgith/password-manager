from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon
from app.ui.animations import AnimatedBackground

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Manager - Вход")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(400, 500)
        
        self.bg = AnimatedBackground(self)
        self.bg.setGeometry(0, 0, 400, 500)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Вход в систему")
        title.setStyleSheet("""
            font-size: 26px; font-weight: bold; color: #E4E4F0; 
            font-family: 'Montserrat', Arial; margin-bottom: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px; font-size: 14px; border-radius: 5px;
                background-color: rgba(42, 42, 62, 0.9); color: #E4E4F0; 
                border: 1px solid #3A3A4E;
            }
            QLineEdit:focus { border: 1px solid #7C6AF7; background-color: #2A2A3E; }
        """)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px; font-size: 14px; border-radius: 5px;
                background-color: rgba(42, 42, 62, 0.9); color: #E4E4F0; 
                border: 1px solid #3A3A4E;
            }
            QLineEdit:focus { border: 1px solid #7C6AF7; background-color: #2A2A3E; }
        """)
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Войти")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #7C6AF7; color: white;
                padding: 12px; font-size: 16px; border-radius: 5px; font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #9B8BFF; }
            QPushButton:pressed { background-color: #5B4BC4; }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if username == "admin" and password == "admin":
            self.on_login_success(username)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def resizeEvent(self, event):
        self.bg.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)