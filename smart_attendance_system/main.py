#!/usr/bin/env python3
"""
Smart Attendance System - Main Entry Point
Compatible with Python 3.13.7
"""

import sys
import os
import logging
from datetime import datetime

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from attendance.ui.main_window import AttendanceMainWindow
    from attendance.core.flask_server import attendance_server
    from attendance.database.db_manager import database_manager
    from attendance.config.settings import app_settings, create_directories
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure all files are in their correct directories.")
    sys.exit(1)

def setup_logging():
    """Setup application logging"""
    log_dir = os.path.join(current_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"attendance_{datetime.now().strftime('%Y%m%d')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info(f"Smart Attendance System v{app_settings.VERSION} - Starting")
    logger.info("=" * 60)

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = ['customtkinter', 'PIL', 'qrcode', 'mysql.connector', 'flask']

    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print("❌ Missing required dependencies:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n📦 Install missing dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

def initialize_application():
    """Initialize application components"""
    logger = logging.getLogger(__name__)

    # Create necessary directories
    create_directories()

    # Test database connection
    logger.info("Testing database connection...")
    if database_manager.test_connection():
        logger.info("✅ Database connection successful")
    else:
        logger.error("❌ Database connection failed")
        print("\n⚠️ Database connection failed!")
        print("Please check your MySQL server and database configuration.")
        choice = input("Continue anyway? (y/N): ")
        if choice.lower() != 'y':
            sys.exit(1)

    # Start Flask server
    logger.info("Starting Flask server...")
    attendance_server.start()

    logger.info(f"📱 QR Scanner URL: http://{attendance_server.get_local_ip()}:5000/scan/<token>")

def main():
    """Main application entry point"""
    try:
        print("🚀 Starting Smart Attendance System...")

        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)

        # Check dependencies
        logger.info("Checking dependencies...")
        check_dependencies()
        logger.info("✅ All dependencies available")

        # Initialize application
        initialize_application()

        # Create and run main window
        logger.info("Launching main window...")
        app = AttendanceMainWindow()

        # Connect server to UI for token updates
        app.set_server(attendance_server)

        logger.info("🎉 Application started successfully")

        # Start main UI loop
        app.mainloop()

    except KeyboardInterrupt:
        logger.info("\n👋 Application interrupted by user")
    except Exception as e:
        logger.error(f"💥 Application error: {e}", exc_info=True)
        print(f"\n❌ Application error: {e}")
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        attendance_server.stop()
        database_manager.close_connection()
        print("👋 Application closed")

if __name__ == "__main__":
    main()
