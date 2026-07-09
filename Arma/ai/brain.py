from openai import OpenAI
from PySide6.QtCore import QThread, Signal
from config.settings import Settings
from utils.logger import setup_logger
from automation.app_control import AppController
from automation.system_control import SystemController

logger = setup_logger(__name__)

class AIBrainWorker(QThread):
    """
    Background thread for communicating with the AI API.
    Ensures network latency does not block the UI.
    """
    response_ready = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, messages: list):
        super().__init__()
        self.messages = messages
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=Settings.OPENROUTER_API_KEY
        )

    def run(self):
        try:
            logger.info("Sending request to AI provider...")
            completion = self.client.chat.completions.create(
                model=Settings.AI_MODEL,
                messages=self.messages
            )
            
            reply = completion.choices[0].message.content
            logger.debug(f"AI Reply: {reply}")
            self.response_ready.emit(reply)
            
        except Exception as e:
            logger.error(f"AI Brain request failed: {e}")
            self.error_occurred.emit(str(e))

class AIBrain:
    """
    Manages the AI context, system prompt, and short-term memory.
    """
    def __init__(self):
        self.system_prompt = (
            "You are ARMA (Artificial Responsive Machine Assistant), an advanced "
            "holographic desktop AI designed to help the user. You speak concisely, "
            "efficiently, and intelligently, similar to JARVIS from Iron Man. "
            "Provide helpful, direct answers. Do not use markdown if the response "
            "is meant to be spoken."
        )
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.max_memory = 20 
        self.active_worker = None

    def process_query(self, user_text: str, callback):
        """
        Adds user text to memory and starts a background API call.
        The `callback` function will be triggered when the reply arrives.
        """
        text = user_text.lower().strip()
        
        import re

        
        if re.search(r'\b(lock)\b.*\b(pc|computer|device|screen)\b', text):
            SystemController.lock_pc()
            callback("Locking the device, sir.")
            return
        if re.search(r'\b(shut down|shutdown|turn off)\b.*\b(pc|computer|system)\b', text):
            SystemController.shutdown()
            callback("Initiating shutdown sequence.")
            return
        if re.search(r'\b(restart)\b.*\b(pc|computer|system)\b', text):
            SystemController.restart()
            callback("Restarting the system.")
            return
        if re.search(r'\b(sleep)\b.*\b(pc|computer|system)\b', text):
            SystemController.sleep_pc()
            callback("Putting system to sleep.")
            return
            
        
        if re.search(r'\b(increase|up)\b.*\b(volume)\b', text):
            SystemController.volume_up()
            callback("Increasing volume.")
            return
        if re.search(r'\b(decrease|down|lower)\b.*\b(volume)\b', text):
            SystemController.volume_down()
            callback("Decreasing volume.")
            return
        if re.search(r'\b(mute)\b.*\b(volume|pc|computer|audio|system)\b', text):
            SystemController.toggle_mute()
            callback("Toggling system mute.")
            return
        if re.search(r'\b(unmute)\b', text):
            SystemController.toggle_mute()
            callback("Unmuting system.")
            return
        if re.search(r'\b(play|pause)\b.*\b(media|music|audio|video)\b', text) and "youtube" not in text:
            SystemController.play_pause_media()
            callback("Toggling media playback.")
            return

        if re.search(r'\b(close|exit|quit)\b.*\b(whatsapp)\b', text):
            import threading
            threading.Thread(target=AppController.close_application, args=("whatsapp",), daemon=True).start()
            callback("Closing WhatsApp, sir.")
            return

        if re.search(r'\b(close|exit|quit)\b.*\b(youtube)\b', text):
            import threading
            threading.Thread(target=AppController.close_application, args=("chrome",), daemon=True).start()
            callback("Closing YouTube (browser), sir.")
            return

        if re.search(r'\b(open|launch|start)\b.*\b(whatsapp)\b', text):
            AppController.open_whatsapp()
            callback("Opening WhatsApp, sir.")
            return
            
        if re.search(r'\b(search)\b.*\b(youtube)\b', text):
            match = re.search(r'search\s+(.+?)\s+on\s+youtube|search\s+youtube\s+for\s+(.+)', text)
            query = match.group(1) or match.group(2) if match else text.replace("search", "").replace("youtube", "").replace("for", "").strip()
            if query:
                AppController.search_youtube(query)
                callback(f"Searching YouTube for {query}.")
            else:
                AppController.open_website("youtube.com")
                callback("Opening YouTube.")
            return
            
        if re.search(r'\b(play)\b.*\b(youtube)\b', text):
            match = re.search(r'play\s+(.+?)\s+on\s+youtube', text)
            query = match.group(1) if match else text.replace("play", "").replace("on youtube", "").strip()
            if query:
                AppController.search_youtube(query)
                callback(f"Playing {query} on YouTube.")
            else:
                AppController.open_website("youtube.com")
                callback("Opening YouTube.")
            return
            
        if re.search(r'\b(open|launch|start)\b.*\b(youtube)\b', text):
            AppController.open_website("youtube.com")
            callback("Opening YouTube for you.")
            return
                
        if re.search(r'\b(search)\b', text) and re.search(r'\b(google|web)\b', text):
            match = re.search(r'search\s+(?:google|the web)\s+for\s+(.+)|search\s+(.+)\s+on\s+(?:google|the web)', text)
            query = match.group(1) or match.group(2) if match else text.replace("search", "").replace("google", "").replace("the web", "").replace("for", "").strip()
            if query:
                AppController.search_google(query)
                callback(f"Searching Google for {query}.")
            else:
                AppController.open_website("google.com")
                callback("Opening Google.")
            return

        close_match = re.search(r'\b(close|exit|quit)\b\s*(.*)', text)
        if close_match:
            app_name = close_match.group(2).strip()
            app_name = re.sub(r'\b(the|a|an|please|app|application|program)\b', '', app_name, flags=re.IGNORECASE)
            app_name = app_name.replace(".", "").strip()
            if app_name:
                import threading
                threading.Thread(target=AppController.close_application, args=(app_name,), daemon=True).start()
                callback(f"Closing {app_name}.")
                return
      
        open_match = re.search(r'\b(open|launch|start)\b\s*(.*)', text)
        if open_match:
            app_name = open_match.group(2).strip()
            app_name = re.sub(r'\b(the|a|an|please|app|application|program)\b', '', app_name, flags=re.IGNORECASE)
            app_name = app_name.replace(".", "").strip()
            if app_name:
                import threading
                threading.Thread(target=AppController.open_application, args=(app_name,), daemon=True).start()
                callback(f"Opening {app_name}.")
                return

      
        self.conversation_history.append({"role": "user", "content": user_text})
        self._trim_memory()

        self.active_worker = AIBrainWorker(self.conversation_history)
        
  
        self.active_worker.response_ready.connect(self._handle_response)
        self.active_worker.response_ready.connect(callback)
        self.active_worker.error_occurred.connect(
            lambda e: callback("I'm sorry, I am having trouble connecting to my cognitive systems.")
        )
        
        self.active_worker.start()

    def _handle_response(self, reply: str):
        """Adds the AI's reply to the conversation history."""
        self.conversation_history.append({"role": "assistant", "content": reply})
        self._trim_memory()

    def _trim_memory(self):
        """Ensures the memory does not exceed the maximum allowed messages."""
        if len(self.conversation_history) > self.max_memory:

            self.conversation_history = (
                [self.conversation_history[0]] + 
                self.conversation_history[-(self.max_memory - 1):]
            )
