from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Manager - Вход")
        self.resize(400, 350)
        
        # Темный фон для всего окна
        self.setStyleSheet("background-color: #1E1E2E;")

        # Главный контейнер
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15) 

        # Заголовок
        title = QLabel("Вход в систему")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #E4E4F0; font-family: 'Montserrat';")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Поле Логин
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; font-size: 14px; border-radius: 5px;
                background-color: #2A2A3E; color: #E4E4F0; border: 1px solid #3A3A4E;
            }
            QLineEdit:focus { border: 1px solid #7C6AF7; }
        """)
        layout.addWidget(self.username_input)

        # Поле Пароль
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; font-size: 14px; border-radius: 5px;
                background-color: #2A2A3E; color: #E4E4F0; border: 1px solid #3A3A4E;
            }
            QLineEdit:focus { border: 1px solid #7C6AF7; }
        """)
        layout.addWidget(self.password_input)

        # Кнопка Войти
        self.login_btn = QPushButton("Войти")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #7C6AF7; color: white;
                padding: 10px; font-size: 16px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #9B8BFF; }
            QPushButton:pressed { background-color: #5B4BC4; }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Временная заглушка (позже свяжем с базой данных)
        if username == "admin" and password == "admin":
            self.on_login_success(username)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")