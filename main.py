import sys
from PyQt6.QtWidgets import QApplication
from app.database.models import init_db
from app.ui.windows.login_window import LoginWindow

def start_main_app(username):
    print(f"Успешный вход! Привет, {username}")
    # Позже здесь мы будем открывать главное окно

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Инициализация БД (создаем таблицы)
    init_db()

    # Запуск окна входа
    login_window = LoginWindow(on_login_success=start_main_app)
    login_window.show()

    sys.exit(app.exec())