import sys
from PyQt6.QtWidgets import QApplication
from app.database.models import init_db
from app.ui.windows.login_window import LoginWindow
from app.ui.windows.main_window import MainWindow

def start_main_app(username):
    login_window.close()
    global main_window
    main_window = MainWindow(username)
    main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_db()

    login_window = LoginWindow(on_login_success=start_main_app)
    login_window.show()

    sys.exit(app.exec())