from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject, QByteArray
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget

class AnimationFactory:
    """
    Provides standardized PySide6 animations for a fluid, 60 FPS, JARVIS-like interface.
    """

    @staticmethod
    def fade_in(widget: QWidget, duration_ms: int = 500) -> QPropertyAnimation:
        """Fades a widget into view."""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity", widget)
        animation.setDuration(duration_ms)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        return animation

    @staticmethod
    def fade_out(widget: QWidget, duration_ms: int = 500) -> QPropertyAnimation:
        """Fades a widget out of view."""
        
        effect = widget.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            
        animation = QPropertyAnimation(effect, b"opacity", widget)
        animation.setDuration(duration_ms)
        animation.setStartValue(effect.opacity())
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
       
        animation.finished.connect(widget.hide)
        return animation

    @staticmethod
    def pulse_effect(widget: QWidget, duration_ms: int = 2000, max_opacity: float = 1.0, min_opacity: float = 0.4) -> QPropertyAnimation:
        """Creates an infinite breathing/pulsing opacity effect."""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity", widget)
        animation.setDuration(duration_ms)
        animation.setStartValue(min_opacity)
        
        
        animation.setKeyValueAt(0.5, max_opacity)
        animation.setEndValue(min_opacity)
        
        animation.setEasingCurve(QEasingCurve.InOutSine)
    
        animation.setLoopCount(-1)
        
        return animation

    @staticmethod
    def slide_in(widget: QWidget, start_geometry, end_geometry, duration_ms: int = 400) -> QPropertyAnimation:
        """Slides a widget from one geometry to another."""
        animation = QPropertyAnimation(widget, b"geometry", widget)
        animation.setDuration(duration_ms)
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.setEasingCurve(QEasingCurve.OutExpo)
        return animation
