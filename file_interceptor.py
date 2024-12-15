import os
import time
import hashlib
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logging.handlers import RotatingFileHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Logging Setup
LOG_FILE = "file_interceptor.log"
logging.basicConfig(
    handlers=[RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("FileInterceptor")

# Email Notification Setup
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"

# Monitor Settings
MONITORED_DIR = "/path/to/directory"
FILE_EXTENSIONS = [".exe", ".docx", ".py"]  # Monitor specific file types

# Event Handler
class FileInterceptorHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_hashes = {}

    def calculate_checksum(self, file_path):
        """Calculate SHA-256 checksum of a file."""
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
                return file_hash.hexdigest()
        except FileNotFoundError:
            return None

    def on_created(self, event):
        if event.is_directory:
            return
        if not self._filter_file(event.src_path):
            return
        logger.info(f"File created: {event.src_path}")
        self._send_email(f"File created: {event.src_path}")

    def on_modified(self, event):
        if event.is_directory:
            return
        if not self._filter_file(event.src_path):
            return
        logger.info(f"File modified: {event.src_path}")
        self._send_email(f"File modified: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        if not self._filter_file(event.src_path):
            return
        logger.info(f"File deleted: {event.src_path}")
        self._send_email(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            return
        logger.info(f"File moved: {event.src_path} to {event.dest_path}")
        self._send_email(f"File moved: {event.src_path} to {event.dest_path}")

    def _filter_file(self, file_path):
        """Filter files based on extension."""
        _, ext = os.path.splitext(file_path)
        return ext in FILE_EXTENSIONS

    def _send_email(self, message):
        """Send email notification."""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS
            msg['Subject'] = "File Interceptor Alert"
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            logger.info(f"Email notification sent: {message}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

# Monitoring Thread
def start_monitoring():
    """Start monitoring the directory."""
    event_handler = FileInterceptorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITORED_DIR, recursive=True)
    observer.start()
    logger.info(f"Started monitoring directory: {MONITORED_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Main Execution
if __name__ == "__main__":
    monitoring_thread = threading.Thread(target=start_monitoring)
    monitoring_thread.start()
