import sys
import ctypes
from PySide6.QtWidgets import QApplication
from config.settings import Settings
from gui.main_window import ARMAWindow
from utils.logger import setup_logger

logger = setup_logger("Boot")

def hide_console():
    """Hides the Windows command prompt terminal if running natively."""
    try:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 0) 
    except Exception as e:
        pass

def main():
    logger.info("Initializing ARMA Boot Sequence...")
    
   
    Settings.validate()
    


    app = QApplication(sys.argv)
  
    app.setAttribute(PySide6.QtCore.Qt.AA_EnableHighDpiScaling if hasattr(PySide6.QtCore.Qt, 'AA_EnableHighDpiScaling') else None)
    
    logger.info("Starting Main Holographic Interface...")

    window = ARMAWindow()
    window.show()
    
    
    sys.exit(app.exec())

if __name__ == "__main__":
    import PySide6.QtCore
    main()
