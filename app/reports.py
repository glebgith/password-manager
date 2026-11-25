import os
import shutil
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.database import get_connection
from app.security.crypto import decrypt_data

key = b'0123456789abcdef0123456789abcdef'

# Подключаем русский шрифт для PDF
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\Arial.ttf'))
    font_name = 'Arial'
except:
    font_name = 'Helvetica'

def get_entries():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, login, password_enc FROM vault_entries WHERE user_id = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def export_to_excel():
    rows = get_entries()
    wb = Workbook()
    ws = wb.active
    ws.title = "Мои пароли"

    headers = ["Название", "Логин", "Пароль"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="7C6AF7", end_color="7C6AF7", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")

    for row_idx, row in enumerate(rows, 2):
        title = row['title']
        login = row['login']
        try:
            password = decrypt_data(key, row['password_enc'])
        except Exception:
            password = "Ошибка"

        ws.cell(row=row_idx, column=1, value=title)
        ws.cell(row=row_idx, column=2, value=login)
        ws.cell(row=row_idx, column=3, value=password)

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    filename = "passwords_report.xlsx"
    wb.save(filename)
    return os.path.abspath(filename)

def export_to_pdf():
    rows = get_entries()
    filename = "passwords_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Стиль для заголовка на русском
    title_style = ParagraphStyle(
        name='RussianTitle',
        parent=styles['Title'],
        fontName=font_name
    )
    
    title = Paragraph("<b>Отчёт по хранилищу паролей</b>", title_style)
    elements.append(title)

    data = [["Название", "Логин", "Пароль"]]
    for row in rows:
        try:
            password = decrypt_data(key, row['password_enc'])
        except Exception:
            password = "Ошибка"
        data.append([row['title'], row['login'], password])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#7C6AF7")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), font_name), # Применяем русский шрифт ко всей таблице
        ('FONTNAME', (0, 0), (-1, 0), font_name),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#2A2A3E")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#E4E4F0")),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#3A3A4E")),
    ]))
    elements.append(table)

    doc.build(elements)
    return os.path.abspath(filename)

def backup_db(db_path="vault.db"):
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"vault_backup_{timestamp}.db")
    shutil.copy2(db_path, backup_path)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO backups (filepath) VALUES (?)", (backup_path,))
    conn.commit()
    conn.close()

    return os.path.abspath(backup_path)