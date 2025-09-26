# 10. Main Window - The complete UI application
main_window_py_content = '''"""
Main Window - Primary application interface
smart_attendance_system/src/attendance/ui/main_window.py
"""
import customtkinter as ctk
import threading
import time
from datetime import datetime, timedelta
from typing import Optional
import logging

from .ui_components import QRDisplayArea, ControlPanel, SystemStatusPanel
from .ui_styles import ui_styles
from ..core.qr_generator import qr_generator
from ..core.flask_server import AttendanceFlaskServer
from ..database.db_manager import database_manager
from ..utils.csv_exporter import csv_exporter
from ..config.settings import app_settings

logger = logging.getLogger(__name__)

class AttendanceMainWindow(ctk.CTk):
    """Main application window with modern UI"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window properties
        self._configure_window()
        
        # Initialize application state
        self.current_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        self.is_qr_running = False
        self.qr_thread: Optional[threading.Thread] = None
        self.flask_server: Optional[AttendanceFlaskServer] = None
        
        # Setup UI theme
        ui_styles.configure_theme()
        
        # Create user interface
        self._create_interface()
        
        # Setup event handlers
        self._setup_event_handlers()
        
        # Initialize system status
        self._initialize_system_status()
        
        # Start QR generation
        self._start_qr_generation()
    
    def _configure_window(self):
        """Configure main window properties"""
        self.title(f"{app_settings.TITLE} v{app_settings.VERSION}")
        
        # Set window size and constraints
        window_width = ui_styles.DIMENSIONS['window_min_width']
        window_height = ui_styles.DIMENSIONS['window_min_height']
        
        self.geometry(f"{window_width}x{window_height}")
        self.minsize(window_width, window_height)
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
    def _create_interface(self):
        """Create the main user interface"""
        # Create sidebar
        self._create_sidebar()
        
        # Create main content area
        self._create_main_content()
    
    def _create_sidebar(self):
        """Create sidebar with controls and status"""
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(
            self,
            width=ui_styles.DIMENSIONS['sidebar_width'],
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(2, weight=1)  # Make middle section expandable
        
        # App header
        self.header_frame = ctk.CTkFrame(self.sidebar, **ui_styles.get_frame_style())
        self.header_frame.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")
        
        self.app_title = ctk.CTkLabel(
            self.header_frame,
            text="🎓 Smart Attendance",
            **ui_styles.get_label_style("title")
        )
        self.app_title.pack(pady=20)
        
        self.version_label = ctk.CTkLabel(
            self.header_frame,
            text=f"Version {app_settings.VERSION}",
            **ui_styles.get_label_style("caption")
        )
        self.version_label.pack(pady=(0, 16))
        
        # System status panel
        self.status_panel = SystemStatusPanel(self.sidebar)
        self.status_panel.grid(row=1, column=0, padx=16, pady=8, sticky="ew")
        
        # Control panel
        self.control_panel = ControlPanel(self.sidebar)
        self.control_panel.grid(row=3, column=0, padx=16, pady=(8, 16), sticky="ew")
    
    def _create_main_content(self):
        """Create main content area"""
        # Main content frame
        self.main_frame = ctk.CTkFrame(self, **ui_styles.get_frame_style())
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # QR display area
        self.qr_display = QRDisplayArea(self.main_frame)
        self.qr_display.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
    
    def _setup_event_handlers(self):
        """Setup event handlers and callbacks"""
        # Bind control panel commands
        self.control_panel.bind_commands(
            export_command=self._handle_export_csv,
            refresh_command=self._handle_refresh_qr,
            theme_command=self._handle_theme_change
        )
        
        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self._handle_window_close)
    
    def _initialize_system_status(self):
        """Initialize system status displays"""
        # Update IP address
        local_ip = qr_generator.get_local_ip()
        self.status_panel.update_ip_address(local_ip)
        
        # Test database connection
        if database_manager.test_connection():
            self.status_panel.update_database_status("online")
            logger.info("✅ Database connection verified")
        else:
            self.status_panel.update_database_status("offline")
            logger.warning("⚠️ Database connection failed")
        
        # Server status will be updated when server starts
        self.status_panel.update_server_status("connecting")
    
    def _start_qr_generation(self):
        """Start QR code generation in background thread"""
        if self.is_qr_running:
            return
        
        self.is_qr_running = True
        self.qr_thread = threading.Thread(target=self._qr_generation_loop, daemon=True)
        self.qr_thread.start()
        logger.info("🔄 QR generation started")
    
    def _qr_generation_loop(self):
        """Background thread for QR code generation"""
        while self.is_qr_running:
            try:
                # Generate new token
                self.current_token = self._generate_token()
                self.token_expiry = datetime.now() + timedelta(seconds=app_settings.QR_REFRESH_INTERVAL)
                
                # Create QR code image
                qr_image = qr_generator.create_tkinter_image(self.current_token)
                
                # Update server token
                if self.flask_server:
                    self.flask_server.update_token(self.current_token, self.token_expiry)
                
                # Update UI in main thread
                expiry_display = self.token_expiry.strftime('%H:%M:%S')
                self.after(0, self.qr_display.update_qr_display, qr_image, self.current_token, expiry_display)
                
                logger.info(f"🔄 QR updated: {self.current_token}")
                
                # Wait for next update
                time.sleep(app_settings.QR_REFRESH_INTERVAL)
                
            except Exception as e:
                logger.error(f"❌ Error in QR generation: {e}")
                self.after(0, self.qr_display.show_loading_message, "❌ QR Generation Error")
                time.sleep(5)  # Wait before retrying
    
    def _generate_token(self) -> str:
        """Generate unique attendance token"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"ATTEND-{timestamp}"
    
    def _stop_qr_generation(self):
        """Stop QR code generation"""
        if self.is_qr_running:
            self.is_qr_running = False
            if self.qr_thread and self.qr_thread.is_alive():
                self.qr_thread.join(timeout=2)
            logger.info("🛑 QR generation stopped")
    
    def _handle_export_csv(self):
        """Handle CSV export button click"""
        try:
            logger.info("📊 Starting CSV export...")
            success = csv_exporter.export_all_records()
            if success:
                logger.info("✅ CSV export completed")
            else:
                logger.info("ℹ️ CSV export cancelled by user")
        except Exception as e:
            logger.error(f"❌ CSV export error: {e}")
    
    def _handle_refresh_qr(self):
        """Handle refresh QR button click"""
        logger.info("🔄 Manual QR refresh requested")
        self.qr_display.show_loading_message("🔄 Refreshing QR Code...")
        
        # Generate new QR immediately
        threading.Thread(target=self._immediate_qr_refresh, daemon=True).start()
    
    def _immediate_qr_refresh(self):
        """Immediately refresh QR code"""
        try:
            # Generate new token
            self.current_token = self._generate_token()
            self.token_expiry = datetime.now() + timedelta(seconds=app_settings.QR_REFRESH_INTERVAL)
            
            # Create QR image
            qr_image = qr_generator.create_tkinter_image(self.current_token)
            
            # Update server
            if self.flask_server:
                self.flask_server.update_token(self.current_token, self.token_expiry)
            
            # Update UI
            expiry_display = self.token_expiry.strftime('%H:%M:%S')
            self.after(0, self.qr_display.update_qr_display, qr_image, self.current_token, expiry_display)
            
            logger.info(f"✅ QR refreshed manually: {self.current_token}")
            
        except Exception as e:
            logger.error(f"❌ Manual QR refresh error: {e}")
            self.after(0, self.qr_display.show_loading_message, "❌ Refresh Failed")
    
    def _handle_theme_change(self, theme: str):
        """Handle theme change"""
        try:
            ctk.set_appearance_mode(theme.lower())
            logger.info(f"🎨 Theme changed to: {theme}")
        except Exception as e:
            logger.error(f"❌ Theme change error: {e}")
    
    def _handle_window_close(self):
        """Handle application window close"""
        logger.info("🚪 Application closing...")
        
        # Stop background processes
        self._stop_qr_generation()
        
        # Close database connection
        database_manager.close_connection()
        
        # Stop Flask server
        if self.flask_server:
            self.flask_server.stop()
        
        # Close window
        self.destroy()
        logger.info("👋 Application closed successfully")
    
    def set_server(self, server: AttendanceFlaskServer):
        """Set the Flask server instance"""
        self.flask_server = server
        self.status_panel.update_server_status("online")
        logger.info("🌐 Flask server connected to UI")
    
    def show_error_message(self, title: str, message: str):
        """Show error message to user"""
        import tkinter.messagebox as msgbox
        msgbox.showerror(title, message)
    
    def show_info_message(self, title: str, message: str):
        """Show info message to user"""
        import tkinter.messagebox as msgbox
        msgbox.showinfo(title, message)
'''

print("✅ Created main window interface")
print("10. main_window.py (smart_attendance_system/src/attendance/ui/main_window.py)")