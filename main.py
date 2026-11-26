import sys
import traceback
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon
from app.database.models import init_db
from app.database import get_connection
from app.ui.windows.login_window import LoginWindow
from app.ui.windows.main_window import MainWindow

def start_main_app(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            role = "admin" if username == "admin" else "user"
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                           (username, "temp_hash", role))
            conn.commit()
        conn.close()

        login_window.close()
        global main_window
        main_window = MainWindow(username)
        main_window.show()
    except Exception as e:
        print("\n=== ПРОИЗОШЛА ОШИБКА ===")
        traceback.print_exc()

if __name__ == "__main__":
    # Установка ID для корректного отображения иконки в панели задач Windows
    myappid = 'mycompany.passwordmanager.app.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    
    # Устанавливаем иконку для всего приложения
    app.setWindowIcon(QIcon("icon.png"))
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    init_db()

    login_window = LoginWindow(on_login_success=start_main_app)
    login_window.show()

    sys.exit(app.exec())