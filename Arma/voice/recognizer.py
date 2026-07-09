import speech_recognition as sr
from PySide6.QtCore import QThread, Signal
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VoiceRecognizer(QThread):
    """
    Background thread for continuously listening to the microphone.
    Emits signals when speech is detected, preventing UI freezes.
    """
    
    
    speech_detected = Signal(str)     
    wake_word_detected = Signal()     
    listening_status = Signal(bool)   

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._is_running = True
        
        
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 400
        self.recognizer.pause_threshold = 0.8  

    def run(self):
        """Main loop of the thread, continuously listens for audio."""
        logger.info("Voice Recognizer Thread Started.")
        
        with self.microphone as source:
            logger.info("Calibrating microphone for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone calibrated. Listening for wake word...")
            
            while self._is_running:
                try:
                    self.listening_status.emit(True)
                    
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    self.listening_status.emit(False)
                    
                    
                    self._process_audio(audio)
                    
                except sr.WaitTimeoutError:
                    
                    pass
                except Exception as e:
                    logger.error(f"Error while listening: {e}")

    def _process_audio(self, audio):
        """Attempts to transcribe audio using Google's free STT."""
        try:
            
            text = self.recognizer.recognize_google(audio).lower()
            logger.debug(f"Heard: '{text}'")
            
            self.speech_detected.emit(text)
            
            if Settings.WAKE_WORD in text:
                logger.info(f"Wake word '{Settings.WAKE_WORD}' detected!")
                self.wake_word_detected.emit()
                
        except sr.UnknownValueError:
            
            pass
        except sr.RequestError as e:
            logger.error(f"Could not request STT results; {e}")
            
    def stop(self):
        """Safely stops the background thread."""
        logger.info("Stopping Voice Recognizer Thread...")
        self._is_running = False
        self.wait() 
