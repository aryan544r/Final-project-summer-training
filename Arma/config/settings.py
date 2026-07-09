import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()

@dataclass
class ColorTheme:
    """Color palette for the holographic JARVIS-like UI."""
    PRIMARY: str = "#00E5FF"       
    GLOW: str = "#00FFFF"          
    ACCENT: str = "#007BFF"        
    WARNING: str = "#FFA500"       
    ERROR: str = "#FF0000"        
    TEXT: str = "#FFFFFF"       
    BG_TRANSPARENT: str = "transparent"
    PANEL_BG: str = "rgba(0, 20, 40, 0.3)" 

class Settings:
    """Central configuration class for ARMA."""
    
   
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    AI_MODEL = os.getenv("AI_MODEL", "google/gemini-pro")
    
   
    WAKE_WORD = os.getenv("WAKE_WORD", "hey arma").lower()
    VOICE_PITCH = "+0Hz"
    VOICE_RATE = "+0%"
    VOICE_NAME = "en-US-ChristopherNeural"
   
    TARGET_FPS = int(os.getenv("TARGET_FPS", "60"))
    ANIMATION_SMOOTHNESS = 1000 // TARGET_FPS 
    
   
    COLORS = ColorTheme()

    @classmethod
    def validate(cls):
        """Check if crucial settings are present."""
        if not cls.OPENROUTER_API_KEY:
            print("WARNING: OPENROUTER_API_KEY is missing. AI chat will not work.")
