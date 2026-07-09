from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from config.settings import Settings

class GlassProgressBar(QProgressBar):
    """A custom progress bar styled to look like a glowing sci-fi HUD element."""
    def __init__(self, color_hex: str):
        super().__init__()
        self.setTextVisible(False)
        self.setFixedHeight(8)
        
        
        style = f"""
            QProgressBar {{
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            QProgressBar::chunk {{
                background-color: {color_hex};
                border-radius: 4px;
                /* Create a glowing box-shadow effect using linear gradient */
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 0, 0, 0),
                    stop: 1 {color_hex}
                );
            }}
        """
        self.setStyleSheet(style)

class SystemPanelWidget(QWidget):
    """
    Left-side HUD panel displaying real-time system stats (CPU, RAM, Network).
    Uses a glassmorphism background.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(250)
        
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Settings.COLORS.PANEL_BG};
                border-radius: 15px;
                border: 1px solid rgba({Settings.COLORS.PRIMARY}, 0.3);
                color: {Settings.COLORS.TEXT};
                font-family: 'Consolas', 'Courier New', monospace;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        
        title = QLabel("SYSTEM STATUS")
        title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {Settings.COLORS.PRIMARY};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        
        self.cpu_label, self.cpu_bar = self._create_stat_row(layout, "CPU USAGE", Settings.COLORS.PRIMARY)
        self.ram_label, self.ram_bar = self._create_stat_row(layout, "RAM ALLOC", Settings.COLORS.ACCENT)
        self.bat_label, self.bat_bar = self._create_stat_row(layout, "BATTERY", Settings.COLORS.GLOW)
        self.disk_label, self.disk_bar = self._create_stat_row(layout, "STORAGE", Settings.COLORS.PRIMARY)
        
        
        self.net_up_label = QLabel("UP: 0.0 Mbps")
        self.net_down_label = QLabel("DOWN: 0.0 Mbps")
        self.net_up_label.setStyleSheet("font-size: 11px; color: #aaaaaa;")
        self.net_down_label.setStyleSheet("font-size: 11px; color: #aaaaaa;")
        
        layout.addWidget(self.net_up_label)
        layout.addWidget(self.net_down_label)
        
        layout.addStretch()

    def _create_stat_row(self, layout: QVBoxLayout, title: str, color_hex: str):
        """Helper to create a label and a progress bar."""
        label = QLabel(f"{title}: 0%")
        label.setStyleSheet("font-size: 12px;")
        bar = GlassProgressBar(color_hex)
        bar.setValue(0)
        
        layout.addWidget(label)
        layout.addWidget(bar)
        return label, bar

    def update_stats(self, stats: dict):
        """Called by the SystemMonitorWorker signal to update the UI."""
        
        self.cpu_label.setText(f"CPU USAGE: {stats['cpu_percent']}%")
        self.cpu_bar.setValue(int(stats['cpu_percent']))
        
        
        self.ram_label.setText(f"RAM ALLOC: {stats['ram_percent']}% ({stats['ram_text']})")
        self.ram_bar.setValue(int(stats['ram_percent']))
        
        
        plug_status = "(AC)" if stats['is_plugged'] else "(BATT)"
        self.bat_label.setText(f"BATTERY: {stats['battery_percent']}% {plug_status}")
        self.bat_bar.setValue(int(stats['battery_percent']))
        
        
        if stats['battery_percent'] <= 20 and not stats['is_plugged']:
            self.bat_bar.setStyleSheet(self.bat_bar.styleSheet().replace(Settings.COLORS.GLOW, Settings.COLORS.ERROR))
            
        
        self.disk_label.setText(f"STORAGE: {stats['disk_percent']}%")
        self.disk_bar.setValue(int(stats['disk_percent']))
        
        
        self.net_up_label.setText(f"UP:   {stats['net_up_mbps']} Mbps")
        self.net_down_label.setText(f"DOWN: {stats['net_down_mbps']} Mbps")
