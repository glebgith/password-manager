from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget)
from app.database import get_connection

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #1E1E2E; color: #E4E4F0;")
        self.init_ui()
        self.load_users()
        self.load_logs()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Панель администратора")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #7C6AF7;")
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #3A3A4E; background: #2A2A3E; }
            QTabBar::tab { background: #2A2A3E; color: #E4E4F0; padding: 8px; }
            QTabBar::tab:selected { background: #7C6AF7; color: white; }
        """)

        users_tab = QWidget()
        users_layout = QVBoxLayout(users_tab)
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["ID", "Логин", "Роль"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setStyleSheet("QTableWidget { background-color: #2A2A3E; color: #E4E4F0; }")
        users_layout.addWidget(self.users_table)
        tabs.addTab(users_tab, "Пользователи")

        logs_tab = QWidget()
        logs_layout = QVBoxLayout(logs_tab)
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(3)
        self.logs_table.setHorizontalHeaderLabels(["ID", "ID Пользователя", "Действие"])
        self.logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.logs_table.setStyleSheet("QTableWidget { background-color: #2A2A3E; color: #E4E4F0; }")
        logs_layout.addWidget(self.logs_table)
        tabs.addTab(logs_tab, "Журнал действий")

        layout.addWidget(tabs)

        back_btn = QPushButton("Назад в хранилище")
        back_btn.setStyleSheet("background-color: #7C6AF7; color: white; padding: 8px; border-radius: 5px;")
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)

    def load_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        rows = cursor.fetchall()
        conn.close()

        self.users_table.setRowCount(0)
        for row in rows:
            pos = self.users_table.rowCount()
            self.users_table.insertRow(pos)
            self.users_table.setItem(pos, 0, QTableWidgetItem(str(row['id'])))
            self.users_table.setItem(pos, 1, QTableWidgetItem(row['username']))
            self.users_table.setItem(pos, 2, QTableWidgetItem(row['role']))

    def load_logs(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, action FROM audit_log")
        rows = cursor.fetchall()
        conn.close()

        self.logs_table.setRowCount(0)
        for row in rows:
            pos = self.logs_table.rowCount()
            self.logs_table.insertRow(pos)
            self.logs_table.setItem(pos, 0, QTableWidgetItem(str(row['id'])))
            self.logs_table.setItem(pos, 1, QTableWidgetItem(str(row['user_id'])))
            self.logs_table.setItem(pos, 2, QTableWidgetItem(row['action']))