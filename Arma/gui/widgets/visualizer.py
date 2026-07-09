import random
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QRectF
from config.settings import Settings

class AudioVisualizerWidget(QWidget):
    """
    A holographic audio visualizer consisting of frequency bars.
    Animates when the microphone is actively listening or the AI is speaking.
    """
    def __init__(self, parent=None, num_bars=30):
        super().__init__(parent)
        self.setMinimumSize(300, 100)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.num_bars = num_bars
        self.bar_heights = [0.1] * self.num_bars
        self.target_heights = [0.1] * self.num_bars
        
        self.is_active = False
        self.is_speaking = False

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_bars)
        self.timer.start(Settings.ANIMATION_SMOOTHNESS)

    def set_listening(self, active: bool):
        """Called by the voice recognizer signal."""
        self.is_active = active
        
    def set_speaking(self, active: bool):
        """Called by the voice synthesizer signal."""
        self.is_speaking = active

    def _update_bars(self):
        """Calculates the smooth interpolation for the audio bars."""
        
        if self.is_active or self.is_speaking:
            
            if random.random() < 0.3:
                for i in range(self.num_bars):
                    
                    max_h = 1.0 if self.is_speaking else 0.6
                    self.target_heights[i] = random.uniform(0.1, max_h)
        else:
            
            self.target_heights = [0.05] * self.num_bars

        
        needs_update = False
        for i in range(self.num_bars):
            diff = self.target_heights[i] - self.bar_heights[i]
            if abs(diff) > 0.01:
                
                self.bar_heights[i] += diff * 0.2
                needs_update = True
                
        if needs_update:
            self.update()

    def paintEvent(self, event):
        """Renders the glowing audio bars."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        
        spacing = 4
        total_spacing = spacing * (self.num_bars - 1)
        bar_width = (width - total_spacing) / self.num_bars
        
        
        base_color = QColor(Settings.COLORS.PRIMARY)
        if self.is_speaking:
            base_color = QColor(Settings.COLORS.ACCENT) 
        
        painter.setPen(Qt.NoPen)

        for i in range(self.num_bars):
            
            bar_h = height * self.bar_heights[i]
            
            
            x = i * (bar_width + spacing)
            
            y = height - bar_h
            
            
            gradient = QLinearGradient(x, y, x, height)
            gradient.setColorAt(0, base_color)
            gradient.setColorAt(1, QColor(base_color.red(), base_color.green(), base_color.blue(), 50))
            
            painter.setBrush(gradient)
            
            
            painter.drawRoundedRect(QRectF(x, y, bar_width, bar_h), 2, 2)
            
        painter.end()
