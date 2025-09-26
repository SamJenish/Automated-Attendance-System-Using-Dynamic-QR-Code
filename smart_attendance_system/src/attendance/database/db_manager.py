"""
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

    def mark_attendance(self, regno: str, name: str, ip: str, created_at: datetime) -> bool:
        """Mark attendance for a student"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False

            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO attendance (regno, name, ip, created_at) VALUES (%s, %s, %s, %s)",
                (regno, name, ip, created_at)
            )
            self.connection.commit()
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
                SELECT regno, name, ip, created_at 
                FROM attendance 
                ORDER BY created_at DESC
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logger.error(f"❌ Error fetching attendance records: {e}")
            return []

# Global database manager instance
database_manager = DatabaseManager()
