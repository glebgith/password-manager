from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from app.ui.windows.add_password_dialog import AddPasswordDialog
from app.database import get_connection
from app.security.crypto import encrypt_data, decrypt_data

class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Password Manager - Главная")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #1E1E2E; color: #E4E4F0;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- ШАПКА (HEADER) ---
        header = QWidget()
        header.setStyleSheet("background-color: #2A2A3E; padding: 10px;")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Мой Менеджер Паролей")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #E4E4F0;")
        
        user_info = QLabel(f"Пользователь: {self.username}")
        user_info.setStyleSheet("color: #A0A0B8;")
        
        logout_btn = QPushButton("Выйти")
        logout_btn.setStyleSheet("background-color: #F87171; color: white; padding: 5px 10px; border-radius: 3px;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(user_info)
        header_layout.addWidget(logout_btn)
        main_layout.addWidget(header)

        # --- КОНТЕНТ (ТАБЛИЦА) ---
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)

        self.add_btn = QPushButton("+ Добавить пароль")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4ADE80; color: #1E1E2E;
                padding: 8px; font-size: 14px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #22C55E; }
        """)
        self.add_btn.clicked.connect(self.add_password)
        content_layout.addWidget(self.add_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Название", "Логин", "Пароль"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2A2A3E; color: #E4E4F0;
                border: 1px solid #3A3A4E; border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #1E1E2E; color: #7C6AF7; font-weight: bold; padding: 5px;
            }
        """)
        
        content_layout.addWidget(self.table)
        main_layout.addWidget(content)

        # --- ПОДВАЛ (FOOTER) ---
        footer = QWidget()
        footer.setStyleSheet("background-color: #2A2A3E; padding: 5px;")
        footer_layout = QHBoxLayout(footer)
        footer_label = QLabel("© 2026 Твоё ФИО, Твоя Группа")
        footer_label.setStyleSheet("color: #A0A0B8; font-size: 12px;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(footer_label)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def load_data(self):
        """Загружает данные из БД и расшифровывает пароли"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, login, password_enc FROM vault_entries WHERE user_id = 1")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        for row in rows:
            title, login = row['title'], row['login']
            
            key = b'0123456789abcdef0123456789abcdef'
            try:
                decrypted_pass = decrypt_data(key, row['password_enc'])
            except Exception:
                decrypted_pass = "Ошибка"
            
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, QTableWidgetItem(title))
            self.table.setItem(row_pos, 1, QTableWidgetItem(login))
            self.table.setItem(row_pos, 2, QTableWidgetItem(decrypted_pass))

    def add_password(self):
        dialog = AddPasswordDialog(self)
        if dialog.exec():
            title, login, password = dialog.get_data()
            if not title or not login or not password:
                return

            key = b'0123456789abcdef0123456789abcdef'
            encrypted_pass = encrypt_data(key, password)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO vault_entries (user_id, title, login, password_enc) VALUES (?, ?, ?, ?)",
                (1, title, login, encrypted_pass)
            )
            conn.commit()
            conn.close()

            self.load_data()