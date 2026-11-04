from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton

class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить запись")
        self.resize(300, 200)
        self.setStyleSheet("background-color: #1E1E2E; color: #E4E4F0;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Поле Название
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название (например, Google)")
        self.title_input.setStyleSheet("padding: 8px; border-radius: 3px; background-color: #2A2A3E; color: white;")
        layout.addWidget(self.title_input)

        # Поле Логин
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин (email)")
        self.login_input.setStyleSheet("padding: 8px; border-radius: 3px; background-color: #2A2A3E; color: white;")
        layout.addWidget(self.login_input)

        # Поле Пароль
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 8px; border-radius: 3px; background-color: #2A2A3E; color: white;")
        layout.addWidget(self.password_input)

        # Кнопка Сохранить
        save_btn = QPushButton("Сохранить")
        save_btn.setStyleSheet("background-color: #7C6AF7; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)

    def get_data(self):
        return self.title_input.text(), self.login_input.text(), self.password_input.text()