import os
import asyncio
import tempfile
import edge_tts
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TTSWorker(QThread):
    """
    Background thread to generate the speech file asynchronously
    so we don't freeze the PySide6 UI while waiting for the network.
    """
    file_ready = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self.voice = Settings.VOICE_NAME
        self.rate = Settings.VOICE_RATE
        self.pitch = Settings.VOICE_PITCH

    def run(self):
        try:
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._generate_audio())
            loop.close()
        except Exception as e:
            logger.error(f"TTS Worker failed: {e}")
            self.error_occurred.emit(str(e))

    async def _generate_audio(self):
        communicate = edge_tts.Communicate(
            text=self.text,
            voice=self.voice,
            rate=self.rate,
            pitch=self.pitch
        )
        
        
        import uuid
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, f"arma_speech_{uuid.uuid4().hex}.mp3")
        
        await communicate.save(output_file)
        self.file_ready.emit(output_file)


class VoiceSynthesizer(QObject):
    """
    Manages text-to-speech generation and audio playback.
    Lives in the main thread (for QMediaPlayer safety) but spawns workers.
    """
    
    speech_started = Signal()
    speech_finished = Signal()

    def __init__(self):
        super().__init__()
        
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)
        
        
        self.player.playbackStateChanged.connect(self._on_playback_state_changed)
        
        self.active_worker = None

    @Slot(str)
    def speak(self, text: str):
        """Public method to start speaking."""
        if not text:
            return
            
        logger.info(f"ARMA Speaking: '{text}'")
        
        
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.stop()

        
        self.active_worker = TTSWorker(text)
        self.active_worker.file_ready.connect(self._play_audio_file)
        self.active_worker.start()

    @Slot(str)
    def _play_audio_file(self, file_path: str):
        """Called by the worker thread when the file is ready to play."""
        self.speech_started.emit()
        
        url = QUrl.fromLocalFile(file_path)
        self.player.setSource(url)
        self.player.play()

    def _on_playback_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.StoppedState:
            
            self.speech_finished.emit()
