from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QMouseEvent


from config.settings import Settings
from voice.recognizer import VoiceRecognizer
from voice.synthesizer import VoiceSynthesizer
from ai.brain import AIBrain
from system.monitor import SystemMonitorWorker

from gui.animations import AnimationFactory
from gui.widgets.ai_core import AICoreWidget
from gui.widgets.visualizer import AudioVisualizerWidget
from gui.widgets.system_panel import SystemPanelWidget
from gui.widgets.chat_panel import ChatPanelWidget
from gui.widgets.action_bar import ActionBarWidget

from utils.logger import setup_logger
logger = setup_logger(__name__)

class ARMAWindow(QMainWindow):
    """
    The main transparent, frameless holographic window.
    Integrates all visual widgets and orchestrates signals between core AI/Voice systems.
    """
    ai_response_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
        
      
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.resize(1200, 800)
       
        self._drag_pos = QPoint()

        self._init_ui()
        self._init_core_systems()
        self._connect_signals()

    
        self.fade_anim = AnimationFactory.fade_in(self.centralWidget(), 1000)
        self.fade_anim.start()

    def _init_ui(self):
        """Builds the main layout containing all the HUD panels."""
        central_widget = QWidget(self)
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)

     
        self.system_panel = SystemPanelWidget()
        
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        
        self.ai_core = AICoreWidget()
        self.visualizer = AudioVisualizerWidget()
        self.action_bar = ActionBarWidget()
        
        center_layout.addStretch()
        center_layout.addWidget(self.ai_core, alignment=Qt.AlignCenter)
        center_layout.addStretch()
        center_layout.addWidget(self.visualizer, alignment=Qt.AlignCenter)
        center_layout.addWidget(self.action_bar, alignment=Qt.AlignCenter)

      
        self.chat_panel = ChatPanelWidget()

        main_layout.addWidget(self.system_panel, alignment=Qt.AlignLeft)
        main_layout.addLayout(center_layout)
        main_layout.addWidget(self.chat_panel, alignment=Qt.AlignRight)

    def _init_core_systems(self):
        """Initializes the background threads (Voice, AI, Monitoring)."""
        logger.info("Initializing Core Systems...")
        
        self.system_monitor = SystemMonitorWorker(poll_rate_seconds=1.0)
        self.system_monitor.start()

        self.recognizer = VoiceRecognizer()
        self.synthesizer = VoiceSynthesizer()
        self.brain = AIBrain()
    
        self.recognizer.start()

    def _connect_signals(self):
        """Wires all the signals from background threads to GUI updates."""
        
        
        self.system_monitor.stats_updated.connect(self.system_panel.update_stats)

       
        self.recognizer.listening_status.connect(self.visualizer.set_listening)
       
        self.recognizer.speech_detected.connect(lambda txt: self.chat_panel.add_message("USER", txt))
        
        self.ai_response_signal.connect(self._handle_ai_response)
        
     
        self.recognizer.speech_detected.connect(
            lambda txt: self.brain.process_query(txt, self.ai_response_signal.emit)
        )

        self.recognizer.wake_word_detected.connect(
            lambda: self.ai_core.set_state_speaking(True) 
        )

 
        self.synthesizer.speech_started.connect(lambda: self.ai_core.set_state_speaking(True))
        self.synthesizer.speech_started.connect(lambda: self.visualizer.set_speaking(True))
        
        self.synthesizer.speech_finished.connect(lambda: self.ai_core.set_state_speaking(False))
        self.synthesizer.speech_finished.connect(lambda: self.visualizer.set_speaking(False))

    def _handle_ai_response(self, text: str):
        """Callback triggered when OpenRouter returns a text response."""
        
        self.chat_panel.add_message("ARMA", text)
   
        self.synthesizer.speak(text)


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def closeEvent(self, event):
        """Ensure threads are stopped safely when closing."""
        logger.info("Initiating ARMA Shutdown...")
        self.system_monitor.stop()
        self.recognizer.stop()
        super().closeEvent(event)
