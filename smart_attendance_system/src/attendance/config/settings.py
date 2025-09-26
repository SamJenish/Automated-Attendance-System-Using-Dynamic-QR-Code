"""
Application Configuration Settings
smart_attendance_system/src/attendance/config/settings.py
"""
import os
from dataclasses import dataclass

@dataclass
class DatabaseSettings:
    """Database configuration"""
    HOST: str = "localhost"
    USER: str = "root"
    PASSWORD: str = "root" 
    DATABASE: str = "attendance_system"
    PORT: int = 3306

@dataclass
class ServerSettings:
    """Flask server configuration"""
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    DEBUG: bool = False

@dataclass
class AppSettings:
    """Application settings"""
    VERSION: str = "BETA"
    TITLE: str = "Smart Attendance System"
    QR_REFRESH_INTERVAL: int = 5  # seconds
    QR_SIZE: tuple = (350, 350)
    WINDOW_SIZE: tuple = (900, 700)
    SIDEBAR_WIDTH: int = 250

# Global configuration instances
database_config = DatabaseSettings()
server_config = ServerSettings()
app_settings = AppSettings()

def create_directories():
    """Create necessary application directories"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    directories = [
        os.path.join(base_dir, 'logs'),
        os.path.join(base_dir, 'exports'),
        os.path.join(base_dir, 'assets', 'icons')
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
