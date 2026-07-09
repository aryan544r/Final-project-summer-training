from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt
from config.settings import Settings

class ChatPanelWidget(QWidget):
    """
    Right-side HUD panel displaying the conversation log between the User and ARMA.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Settings.COLORS.PANEL_BG};
                border-radius: 15px;
                border: 1px solid rgba({Settings.COLORS.PRIMARY}, 0.3);
                color: {Settings.COLORS.TEXT};
                font-family: 'Consolas', 'Courier New', monospace;
            }}
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background: rgba(0, 0, 0, 0.2);
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba({Settings.COLORS.PRIMARY}, 0.5);
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        
        title = QLabel("COMMUNICATIONS LINK")
        title.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {Settings.COLORS.ACCENT}; border: none; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background: transparent; border: none;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area)

    def add_message(self, sender: str, text: str):
        """Adds a new message bubble to the chat panel."""
        msg_box = QFrame()
        msg_layout = QVBoxLayout(msg_box)
        msg_layout.setContentsMargins(10, 10, 10, 10)
        
        sender_label = QLabel(sender)
        sender_label.setStyleSheet(f"font-weight: bold; font-size: 12px; border: none; background: transparent;")
        
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("font-size: 13px; border: none; background: transparent;")
        
        
        if sender == "USER":
            sender_label.setStyleSheet(f"font-weight: bold; color: {Settings.COLORS.TEXT}; border: none; background: transparent;")
            msg_box.setStyleSheet(f"""
                QFrame {{
                    background: rgba(255, 255, 255, 0.1);
                    border-left: 3px solid {Settings.COLORS.TEXT};
                    border-radius: 5px;
                }}
            """)
        else: 
            sender_label.setStyleSheet(f"font-weight: bold; color: {Settings.COLORS.PRIMARY}; border: none; background: transparent;")
            msg_box.setStyleSheet(f"""
                QFrame {{
                    background: rgba(0, 229, 255, 0.1);
                    border-left: 3px solid {Settings.COLORS.PRIMARY};
                    border-radius: 5px;
                }}
            """)
            
        msg_layout.addWidget(sender_label)
        msg_layout.addWidget(text_label)
        
        self.chat_layout.addWidget(msg_box)
        
        
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
