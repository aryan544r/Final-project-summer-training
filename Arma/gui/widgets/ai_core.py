import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QRadialGradient, QPainterPath
from PySide6.QtCore import Qt, QTimer, QRectF
from config.settings import Settings

class AICoreWidget(QWidget):
    """
    The central holographic AI core.
    Renders rotating rings, a glowing center, and pulse effects using QPainter.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        
        self.angle_outer = 0
        self.angle_inner = 0
        self.angle_particles = 0
        
        
        self.pulse_radius = 0.0
        self.pulse_growing = True
        
        
        self.rotation_speed_multiplier = 1.0
        self.glow_intensity = 1.0

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_animations)
        self.timer.start(Settings.ANIMATION_SMOOTHNESS)

    def set_state_speaking(self, is_speaking: bool):
        """Modifies the core's animation intensity."""
        if is_speaking:
            self.rotation_speed_multiplier = 3.0
            self.glow_intensity = 1.5
        else:
            self.rotation_speed_multiplier = 1.0
            self.glow_intensity = 1.0

    def _update_animations(self):
        """Updates angles and triggers a repaint."""
        self.angle_outer = (self.angle_outer + (1.5 * self.rotation_speed_multiplier)) % 360
        self.angle_inner = (self.angle_inner - (2.5 * self.rotation_speed_multiplier)) % 360
        self.angle_particles = (self.angle_particles + (1.0 * self.rotation_speed_multiplier)) % 360
        
        
        pulse_speed = 0.5 * self.rotation_speed_multiplier
        if self.pulse_growing:
            self.pulse_radius += pulse_speed
            if self.pulse_radius >= 20.0:
                self.pulse_growing = False
        else:
            self.pulse_radius -= pulse_speed
            if self.pulse_radius <= 0.0:
                self.pulse_growing = True

        self.update() 

    def paintEvent(self, event):
        """Renders the complex glowing vector graphics."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center = self.rect().center()
        
        base_radius = min(width, height) / 3.0
        
        
        glow_radius = base_radius - 20 + self.pulse_radius
        gradient = QRadialGradient(center, glow_radius)
        
        core_color = QColor(Settings.COLORS.GLOW)
        core_color.setAlpha(int(255 * 0.4 * self.glow_intensity))
        
        gradient.setColorAt(0.0, core_color)
        gradient.setColorAt(0.5, QColor(0, 229, 255, int(100 * self.glow_intensity)))
        gradient.setColorAt(1.0, QColor(0, 229, 255, 0))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(center, glow_radius, glow_radius)
        
        
        painter.translate(center)
        painter.rotate(self.angle_inner)
        painter.translate(-center)
        
        inner_pen = QPen(QColor(Settings.COLORS.PRIMARY))
        inner_pen.setWidth(3)
        inner_pen.setStyle(Qt.DashLine)
        painter.setPen(inner_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center, base_radius, base_radius)
        
        
        painter.resetTransform()
        
        
        painter.translate(center)
        painter.rotate(self.angle_outer)
        painter.translate(-center)
        
        outer_pen = QPen(QColor(Settings.COLORS.ACCENT))
        outer_pen.setWidth(2)
        
        outer_pen.setDashPattern([15, 5, 5, 5])
        painter.setPen(outer_pen)
        painter.drawEllipse(center, base_radius + 25, base_radius + 25)
        
        painter.resetTransform()
        
        
        painter.translate(center)
        painter.rotate(self.angle_particles)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(Settings.COLORS.PRIMARY))
        
        
        particle_radius = base_radius + 40
        for i in range(3):
            angle = math.radians(i * 120)
            px = particle_radius * math.cos(angle)
            py = particle_radius * math.sin(angle)
            painter.drawEllipse(QRectF(px - 4, py - 4, 8, 8))
            
        painter.resetTransform()
        painter.end()
