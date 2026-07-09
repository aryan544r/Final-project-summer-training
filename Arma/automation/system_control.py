import os
import shutil
import ctypes
from utils.logger import setup_logger

logger = setup_logger(__name__)

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

class SystemController:
    """
    Handles direct interaction with the Windows Operating System.
    Includes power management, media controls, and file operations.
    """

    @staticmethod
    def _press_key(hex_key_code):
        """Helper to simulate a media key press via ctypes."""
        ctypes.windll.user32.keybd_event(hex_key_code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(hex_key_code, 0, 2, 0)

    
    @staticmethod
    def shutdown():
        logger.info("Executing system shutdown...")
        os.system("shutdown /s /t 5")

    @staticmethod
    def restart():
        logger.info("Executing system restart...")
        os.system("shutdown /r /t 5")

    @staticmethod
    def lock_pc():
        logger.info("Locking PC...")
        ctypes.windll.user32.LockWorkStation()

    @staticmethod
    def sleep_pc():
        logger.info("Putting PC to sleep...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")



    @staticmethod
    def volume_up(clicks=5):
        logger.info("Increasing volume...")
        for _ in range(clicks):
            SystemController._press_key(VK_VOLUME_UP)

    @staticmethod
    def volume_down(clicks=5):
        logger.info("Decreasing volume...")
        for _ in range(clicks):
            SystemController._press_key(VK_VOLUME_DOWN)

    @staticmethod
    def toggle_mute():
        logger.info("Toggling mute...")
        SystemController._press_key(VK_VOLUME_MUTE)

    @staticmethod
    def play_pause_media():
        logger.info("Toggling play/pause...")
        SystemController._press_key(VK_MEDIA_PLAY_PAUSE)


    @staticmethod
    def create_folder(path):
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Created folder at: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create folder {path}: {e}")
            return False

    @staticmethod
    def delete_item(path, requires_confirmation=True):
        """
        Deletes a file or directory.
        The UI/AI brain should handle the `requires_confirmation` logic
        before actually calling this method.
        """
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            logger.info(f"Deleted item at: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {path}: {e}")
            return False

    @staticmethod
    def move_item(source, destination):
        try:
            shutil.move(source, destination)
            logger.info(f"Moved {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Failed to move item: {e}")
            return False
