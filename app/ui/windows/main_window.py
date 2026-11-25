from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QGraphicsDropShadowEffect, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from app.ui.windows.add_password_dialog import AddPasswordDialog
from app.database import get_connection
from app.security.crypto import encrypt_data, decrypt_data
from app.ui.animations import AnimatedBackground
from app.ui.widgets import AnimatedButton
from app.reports import export_to_excel, export_to_pdf, backup_db

class MainWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("Password Manager - Главная")
        self.resize(900, 600)

        self.bg = AnimatedBackground(self)
        self.bg.setGeometry(0, 0, 900, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- ШАПКА ---
        header = QWidget()
        header.setStyleSheet("background-color: rgba(42, 42, 62, 0.95); padding: 10px;")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Мой Менеджер Паролей")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #E4E4F0;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 5px; font-size: 14px; border-radius: 5px;
                background-color: #1E1E2E; color: #E4E4F0; border: 1px solid #3A3A4E;
                width: 200px;
            }
            QLineEdit:focus { border: 1px solid #7C6AF7; }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        
        user_info = QLabel(f"Пользователь: {self.username}")
        user_info.setStyleSheet("color: #A0A0B8;")
        
        admin_btn = AnimatedButton("Админка", "#7C6AF7", "#D8B4FE")
        admin_btn.clicked.connect(self.open_admin)
        
        about_btn = QPushButton("О программе")
        about_btn.setStyleSheet("background-color: #3A3A4E; color: white; padding: 5px 10px; border-radius: 3px;")
        about_btn.clicked.connect(self.open_about)
        
        logout_btn = QPushButton("Выйти")
        logout_btn.setStyleSheet("background-color: #F87171; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(self.search_input)
        header_layout.addStretch()
        header_layout.addWidget(user_info)
        header_layout.addWidget(admin_btn)
        header_layout.addWidget(about_btn)
        header_layout.addWidget(logout_btn)
        main_layout.addWidget(header)

        # --- КОНТЕНТ ---
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Панель с кнопками
        btn_layout = QHBoxLayout()
        
        self.add_btn = AnimatedButton("+ Добавить пароль", "#4ADE80", "#86EFAC", text_color="#1E1E2E")
        self.add_btn.clicked.connect(self.add_password)
        btn_layout.addWidget(self.add_btn)

        self.excel_btn = QPushButton("Выгрузить в Excel")
        self.excel_btn.setStyleSheet("background-color: #3A3A4E; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.excel_btn.clicked.connect(self.export_excel)
        btn_layout.addWidget(self.excel_btn)

        self.pdf_btn = QPushButton("Выгрузить в PDF")
        self.pdf_btn.setStyleSheet("background-color: #3A3A4E; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.pdf_btn.clicked.connect(self.export_pdf)
        btn_layout.addWidget(self.pdf_btn)

        self.backup_btn = QPushButton("Создать бэкап БД")
        self.backup_btn.setStyleSheet("background-color: #3A3A4E; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.backup_btn.clicked.connect(self.make_backup)
        btn_layout.addWidget(self.backup_btn)

        content_layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Логин", "Пароль", "Действие"])
        
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 100)
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(42, 42, 62, 0.95); color: #E4E4F0;
                border: 1px solid #7C6AF7; border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #1E1E2E; color: #7C6AF7; font-weight: bold; padding: 5px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(124, 106, 247, 150))
        shadow.setOffset(0, 0)
        self.table.setGraphicsEffect(shadow)
        
        content_layout.addWidget(self.table)
        main_layout.addWidget(content)

        # --- ПОДВАЛ ---
        footer = QWidget()
        footer.setStyleSheet("background-color: rgba(42, 42, 62, 0.95); padding: 5px;")
        footer_layout = QHBoxLayout(footer)
        footer_label = QLabel("© 2026 Твоё ФИО, Твоя Группа")
        footer_label.setStyleSheet("color: #A0A0B8; font-size: 12px;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(footer_label)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def load_data(self, filter_text=""):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, login, password_enc FROM vault_entries WHERE user_id = 1")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        for row in rows:
            title = row['title']
            login = row['login']
            
            if filter_text:
                if (filter_text.lower() not in title.lower()) and (filter_text.lower() not in login.lower()):
                    continue
            
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            
            self.table.setItem(row_pos, 0, QTableWidgetItem(title))
            self.table.setItem(row_pos, 1, QTableWidgetItem(login))
            self.table.setItem(row_pos, 2, QTableWidgetItem("********"))
            
            toggle_btn = QPushButton("Показать")
            toggle_btn.setStyleSheet("background-color: #7C6AF7; color: white; border-radius: 3px; padding: 2px;")
            toggle_btn.setProperty("enc_pass", row['password_enc'])
            toggle_btn.clicked.connect(lambda checked, b=toggle_btn, r=row_pos: self.toggle_password(b, r))
            
            self.table.setCellWidget(row_pos, 3, toggle_btn)

    def filter_table(self, text):
        self.load_data(filter_text=text)

    def toggle_password(self, button, row):
        key = b'0123456789abcdef0123456789abcdef'
        enc_pass = button.property("enc_pass")
        
        if button.text() == "Показать":
            try:
                decrypted_pass = decrypt_data(key, enc_pass)
                self.table.setItem(row, 2, QTableWidgetItem(decrypted_pass))
                button.setText("Скрыть")
                button.setStyleSheet("background-color: #F87171; color: white; border-radius: 3px; padding: 2px;")
            except Exception:
                self.table.setItem(row, 2, QTableWidgetItem("Ошибка"))
        else:
            self.table.setItem(row, 2, QTableWidgetItem("********"))
            button.setText("Показать")
            button.setStyleSheet("background-color: #7C6AF7; color: white; border-radius: 3px; padding: 2px;")

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

    def export_excel(self):
        try:
            path = export_to_excel()
            QMessageBox.information(self, "Успех", f"Excel-отчёт сохранен:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать Excel:\n{str(e)}")

    def export_pdf(self):
        try:
            path = export_to_pdf()
            QMessageBox.information(self, "Успех", f"PDF-отчёт сохранен:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать PDF:\n{str(e)}")

    def make_backup(self):
        try:
            path = backup_db()
            QMessageBox.information(self, "Успех", f"Бэкап создан:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сделать бэкап:\n{str(e)}")

    def open_admin(self):
        from app.ui.windows.admin_window import AdminWindow
        self.admin_win = AdminWindow()
        self.admin_win.show()

    def open_about(self):
        from app.ui.windows.about_window import AboutWindow
        self.about_win = AboutWindow()
        self.about_win.show()

    def resizeEvent(self, event):
        self.bg.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)