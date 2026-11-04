import sys
from PyQt6.QtWidgets import QApplication
from app.database.models import init_db

app = QApplication(sys.argv)

# Создаем базу данных
init_db()

sys.exit(app.exec())