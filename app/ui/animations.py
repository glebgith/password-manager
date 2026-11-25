from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QPointF
from PyQt6.QtGui import QPainter, QColor, QRadialGradient
import math

class AnimatedBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.angle = 0
        self.pulse = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)

    def update_animation(self):
        self.angle += 0.02
        self.pulse += 0.05
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.fillRect(self.rect(), QColor("#1E1E2E"))
        
        w, h = self.width(), self.height()
        
        pulse_alpha = int(150 + math.sin(self.pulse) * 30)
        
        x1 = w/2 + math.sin(self.angle) * 200
        y1 = h/2 + math.cos(self.angle) * 150
        grad1 = QRadialGradient(QPointF(x1, y1), 350)
        grad1.setColorAt(0, QColor(124, 106, 247, pulse_alpha))
        grad1.setColorAt(1, QColor(30, 30, 46, 0))
        painter.fillRect(self.rect(), grad1)
        
        x2 = w/2 - math.cos(self.angle * 0.8) * 250
        y2 = h/2 - math.sin(self.angle * 0.8) * 200
        grad2 = QRadialGradient(QPointF(x2, y2), 300)
        grad2.setColorAt(0, QColor(59, 130, 246, pulse_alpha))
        grad2.setColorAt(1, QColor(30, 30, 46, 0))
        painter.fillRect(self.rect(), grad2)