from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from config.settings import Settings
from automation.app_control import AppController
from automation.system_control import SystemController

class GlowingButton(QPushButton):
    """A custom button styled for the JARVIS HUD."""
    def __init__(self, text: str, callback):
        super().__init__(text)
        
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(35)
        
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba({Settings.COLORS.PRIMARY}, 0.3);
                border-radius: 5px;
                color: {Settings.COLORS.TEXT};
                font-family: 'Consolas', 'Courier New', monospace;
                padding: 5px 15px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: rgba({Settings.COLORS.PRIMARY}, 0.2);
                border: 1px solid {Settings.COLORS.PRIMARY};
                color: {Settings.COLORS.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: rgba({Settings.COLORS.PRIMARY}, 0.4);
            }}
        """)
        
        self.clicked.connect(callback)

class ActionBarWidget(QWidget):
    """
    Bottom HUD panel containing quick-action execution buttons.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Settings.COLORS.PANEL_BG};
                border-radius: 15px;
                border: 1px solid rgba({Settings.COLORS.PRIMARY}, 0.3);
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)

        
        self.btn_chrome = GlowingButton("CHROME", lambda: AppController.open_application("chrome"))
        self.btn_vscode = GlowingButton("VS CODE", lambda: AppController.open_application("vscode"))
        self.btn_youtube = GlowingButton("YOUTUBE", lambda: AppController.open_website("youtube.com"))
        self.btn_whatsapp = GlowingButton("WHATSAPP", lambda: AppController.open_whatsapp())
        self.btn_settings = GlowingButton("SETTINGS", lambda: AppController.open_application("settings"))
        self.btn_lock = GlowingButton("LOCK", lambda: SystemController.lock_pc())
        
        
        layout.addWidget(self.btn_chrome)
        layout.addWidget(self.btn_vscode)
        layout.addWidget(self.btn_youtube)
        layout.addWidget(self.btn_whatsapp)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_lock)
