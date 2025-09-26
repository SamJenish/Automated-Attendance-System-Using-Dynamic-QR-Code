"""
Database Setup Script - Create required database tables
smart_attendance_system/database_setup.py
"""

import mysql.connector
from mysql.connector import Error
import sys

def create_database_and_tables():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root'
    }

    try:
        print("🔗 Connecting to MySQL server...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("📝 Creating database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_system")
        cursor.execute("USE attendance_system")
        print("✅ Database 'attendance_system' created/verified")

        # Students table
        students_table = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            regno VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            ip VARCHAR(15) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_regno (regno),
            INDEX idx_ip (ip)
        )
        """
        cursor.execute(students_table)
        print("✅ Students table created/verified")

        # Attendance table (use created_at instead of `timestamp`)
        attendance_table = """
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            regno VARCHAR(50) NOT NULL,
            name VARCHAR(100) NOT NULL,
            ip VARCHAR(15) NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_regno (regno),
            INDEX idx_created_at (created_at)
        )
        """
        cursor.execute(attendance_table)
        print("✅ Attendance table created/verified")

        # Sample student data (using IPs)
        sample_students = [
            ('URK23CS1161', 'Vadde Shritej Reddy', '10.166.185.227'),
            ('URK23CS1073', 'Victor Paul GL', '10.166.185.20'),
            ("URK23CS1134","Nagareddygari Pavarna","10.235.183.171"),
             ("URK23CS9004","Penchala Soujanya","10.235.183.214")   
        ]

        print("👥 Adding sample student data...")
        for regno, name, ip in sample_students:
            try:
                cursor.execute(
                    "INSERT INTO students (regno, name, ip) VALUES (%s, %s, %s)",
                    (regno, name, ip)
                )
            except Error as e:
                if e.errno != 1062:  # Ignore duplicate entry
                    print(f"⚠️ Error inserting {regno}: {e}")

        connection.commit()
        print("✅ Sample data added successfully")

        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cursor.fetchone()[0]

        print("\n📊 Database Setup Summary:")
        print(f"   📚 Students: {student_count} records")
        print(f"   ✅ Attendance: {attendance_count} records")
        print("\n🎉 Database setup completed successfully!")
        print("\n📱 Sample student IPs:")
        for regno, name, ip in sample_students:
            print(f"   {regno} ({name}): {ip}")

    except Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    print("🚀 Smart Attendance System - Database Setup")
    print("=" * 50)

    try:
        create_database_and_tables()
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
    except Exception as e:
        print(f"💥 Setup failed: {e}")
