from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QVariantAnimation, QEasingCurve, Qt
from PyQt6.QtGui import QColor

class AnimatedButton(QPushButton):
    def __init__(self, text, color_normal, color_hover, text_color="white", parent=None):
        super().__init__(text, parent)
        self.color_normal = QColor(color_normal)
        self.color_hover = QColor(color_hover)
        self.text_color = text_color
        
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(150)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.valueChanged.connect(self._update_style)
        
        self._update_style(self.color_normal)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.color_normal)
        self.anim.setEndValue(self.color_hover)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.color_hover)
        self.anim.setEndValue(self.color_normal)
        self.anim.start()
        super().leaveEvent(event)

    def _update_style(self, color):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                color: {self.text_color};
                padding: 8px; font-size: 14px; border-radius: 5px; font-weight: bold;
                border: none;
            }}
        """)