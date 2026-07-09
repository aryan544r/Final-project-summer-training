import psutil
import time
from PySide6.QtCore import QThread, Signal
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SystemMonitorWorker(QThread):
    """
    Background thread that continuously polls hardware telemetry.
    Emits a dictionary of stats to be rendered by the holographic HUD.
    """
    
    
    stats_updated = Signal(dict)

    def __init__(self, poll_rate_seconds=1.0):
        super().__init__()
        self.poll_rate = poll_rate_seconds
        self._is_running = True
        
        
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()

    def run(self):
        logger.info("System Hardware Monitor Thread Started.")
        
        while self._is_running:
            try:
                stats = self._gather_stats()
                self.stats_updated.emit(stats)
            except Exception as e:
                logger.error(f"Error gathering system stats: {e}")
                
            time.sleep(self.poll_rate)

    def _gather_stats(self) -> dict:
        """Gathers CPU, RAM, Battery, Disk, and Network telemetry."""
        
        
        cpu_usage = psutil.cpu_percent(interval=None)
        
        
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_used_gb = ram.used / (1024 ** 3)
        ram_total_gb = ram.total / (1024 ** 3)
        
        
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else 100
        is_plugged_in = battery.power_plugged if battery else True

        
        try:
            disk = psutil.disk_usage('C:\\')
            disk_usage = disk.percent
        except:
            disk_usage = 0

        
        current_time = time.time()
        current_net_io = psutil.net_io_counters()
        
        time_elapsed = current_time - self.last_time
        bytes_sent = current_net_io.bytes_sent - self.last_net_io.bytes_sent
        bytes_recv = current_net_io.bytes_recv - self.last_net_io.bytes_recv
        
        
        upload_mbps = (bytes_sent * 8 / (1024 * 1024)) / time_elapsed
        download_mbps = (bytes_recv * 8 / (1024 * 1024)) / time_elapsed
        
        self.last_net_io = current_net_io
        self.last_time = current_time

        return {
            "cpu_percent": cpu_usage,
            "ram_percent": ram_usage,
            "ram_text": f"{ram_used_gb:.1f}/{ram_total_gb:.1f} GB",
            "battery_percent": battery_percent,
            "is_plugged": is_plugged_in,
            "disk_percent": disk_usage,
            "net_up_mbps": round(upload_mbps, 1),
            "net_down_mbps": round(download_mbps, 1)
        }

    def stop(self):
        """Safely stops the telemetry polling thread."""
        logger.info("Stopping System Monitor Thread...")
        self._is_running = False
        self.wait()
