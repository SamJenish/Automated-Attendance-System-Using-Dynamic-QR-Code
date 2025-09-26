# 3. Configuration settings
settings_py_content = '''"""
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
    VERSION: str = "2.0.0"
    TITLE: str = "Smart Attendance System"
    QR_REFRESH_INTERVAL: int = 30  # seconds
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
'''

# 4. Database manager
db_manager_py_content = '''"""
Database Manager - Handle all database operations
smart_attendance_system/src/attendance/database/db_manager.py
"""
import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from ..config.settings import database_config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.connection: Optional[mysql.connector.MySQLConnection] = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=database_config.HOST,
                user=database_config.USER,
                password=database_config.PASSWORD,
                database=database_config.DATABASE,
                port=database_config.PORT,
                autocommit=True
            )
            logger.info("✅ Database connected successfully")
            return True
        except Error as e:
            logger.error(f"❌ Database connection error: {e}")
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("🔌 Database connection closed")
    
    def test_connection(self) -> bool:
        """Test database connection"""
        if self.connect():
            self.close_connection()
            return True
        return False
    
    def get_student_by_ip(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """Get student information by IP address"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE ip = %s", (ip_address,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            logger.error(f"❌ Error fetching student: {e}")
            return None
    
    def mark_attendance(self, regno: str, name: str, ip: str, timestamp: datetime) -> bool:
        """Mark attendance for a student"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO attendance (regno, name, ip, timestamp) VALUES (%s, %s, %s, %s)",
                (regno, name, ip, timestamp)
            )
            cursor.close()
            logger.info(f"✅ Attendance marked: {regno} - {name}")
            return True
        except Error as e:
            logger.error(f"❌ Error marking attendance: {e}")
            return False
    
    def get_all_attendance_records(self) -> List[Dict[str, Any]]:
        """Get all attendance records"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return []
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT regno, name, ip, timestamp 
                FROM attendance 
                ORDER BY timestamp DESC
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logger.error(f"❌ Error fetching attendance records: {e}")
            return []

# Global database manager instance
database_manager = DatabaseManager()
'''

print("✅ Created configuration and database files")
print("3. settings.py (smart_attendance_system/src/attendance/config/settings.py)")
print("4. db_manager.py (smart_attendance_system/src/attendance/database/db_manager.py)")