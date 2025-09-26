# 7. CSV Exporter
csv_exporter_py_content = '''"""
CSV Exporter - Export attendance data to CSV files
smart_attendance_system/src/attendance/utils/csv_exporter.py
"""
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from tkinter import filedialog, messagebox
import logging

from ..database.db_manager import database_manager

logger = logging.getLogger(__name__)

class AttendanceCSVExporter:
    """Handles exporting attendance records to CSV format"""
    
    def __init__(self):
        self.export_directory = self._get_export_directory()
    
    def _get_export_directory(self) -> str:
        """Get or create exports directory"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        export_dir = os.path.join(base_dir, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        return export_dir
    
    def export_all_records(self, custom_path: Optional[str] = None) -> bool:
        """Export all attendance records to CSV"""
        try:
            # Get attendance data
            records = database_manager.get_all_attendance_records()
            
            if not records:
                messagebox.showinfo(
                    "No Data", 
                    "No attendance records found in the database."
                )
                return False
            
            # Get file path
            if not custom_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                default_filename = f"attendance_report_{timestamp}.csv"
                
                file_path = filedialog.asksaveasfilename(
                    title="Save Attendance Report",
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    initialdir=self.export_directory,
                    initialvalue=default_filename
                )
            else:
                file_path = custom_path
            
            if not file_path:
                return False
            
            # Write CSV file
            self._write_csv_file(file_path, records)
            
            # Show success message
            messagebox.showinfo(
                "Export Successful",
                f"✅ CSV file exported successfully!\\n\\n"
                f"📁 File: {os.path.basename(file_path)}\\n"
                f"📊 Records: {len(records)}\\n"
                f"📍 Location: {os.path.dirname(file_path)}"
            )
            
            logger.info(f"✅ CSV exported: {file_path} ({len(records)} records)")
            return True
            
        except Exception as e:
            error_message = f"❌ Failed to export CSV: {str(e)}"
            messagebox.showerror("Export Error", error_message)
            logger.error(f"❌ CSV export error: {e}")
            return False
    
    def _write_csv_file(self, file_path: str, records: List[Dict[str, Any]]):
        """Write attendance records to CSV file"""
        fieldnames = [
            'Registration Number',
            'Student Name', 
            'IP Address',
            'Date',
            'Time',
            'Full Timestamp'
        ]
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in records:
                timestamp = record['timestamp']
                writer.writerow({
                    'Registration Number': record['regno'],
                    'Student Name': record['name'],
                    'IP Address': record['ip'],
                    'Date': timestamp.strftime('%Y-%m-%d'),
                    'Time': timestamp.strftime('%H:%M:%S'),
                    'Full Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
    
    def quick_export(self) -> bool:
        """Quick export with automatic filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"attendance_export_{timestamp}.csv"
        file_path = os.path.join(self.export_directory, filename)
        
        return self.export_all_records(file_path)

# Global CSV exporter instance
csv_exporter = AttendanceCSVExporter()
'''

# 8. UI Styles and Theme Manager
ui_styles_py_content = '''"""
UI Styles - Modern interface styling and themes
smart_attendance_system/src/attendance/ui/ui_styles.py
"""
import customtkinter as ctk
from typing import Dict, Any, Tuple

class ModernUIStyles:
    """Centralized styling for the modern attendance system UI"""
    
    # Color palette
    COLORS = {
        'primary': '#2563eb',      # Blue
        'primary_dark': '#1d4ed8', # Dark blue  
        'success': '#16a34a',      # Green
        'warning': '#ca8a04',      # Yellow
        'danger': '#dc2626',       # Red
        'info': '#0284c7',         # Light blue
        'background': '#f8fafc',   # Light gray
        'surface': '#ffffff',      # White
        'text': '#1f2937',         # Dark gray
        'text_light': '#6b7280',   # Light gray
    }
    
    # Typography
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'heading': ('Segoe UI', 18, 'bold'),
        'subheading': ('Segoe UI', 16, 'bold'),
        'body': ('Segoe UI', 14, 'normal'),
        'body_small': ('Segoe UI', 12, 'normal'),
        'button': ('Segoe UI', 14, 'normal'),
        'caption': ('Segoe UI', 10, 'normal'),
    }
    
    # Layout dimensions
    DIMENSIONS = {
        'window_min_width': 900,
        'window_min_height': 700,
        'sidebar_width': 280,
        'button_height': 45,
        'input_height': 40,
        'qr_display_size': (350, 350),
        'border_radius': 12,
        'padding_small': 8,
        'padding_medium': 16,
        'padding_large': 24,
    }
    
    @classmethod
    def configure_theme(cls, appearance: str = "system", color_theme: str = "blue"):
        """Configure CustomTkinter appearance and color theme"""
        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme(color_theme)
    
    @classmethod
    def get_button_style(cls, variant: str = "primary") -> Dict[str, Any]:
        """Get button styling configuration"""
        base_style = {
            'height': cls.DIMENSIONS['button_height'],
            'font': ctk.CTkFont(size=14, weight='normal'),
            'corner_radius': cls.DIMENSIONS['border_radius'],
        }
        
        if variant == "primary":
            base_style.update({
                'fg_color': cls.COLORS['primary'],
                'hover_color': cls.COLORS['primary_dark'],
            })
        elif variant == "success":
            base_style.update({
                'fg_color': cls.COLORS['success'],
                'hover_color': '#15803d',
            })
        elif variant == "secondary":
            base_style.update({
                'height': 40,
                'font': ctk.CTkFont(size=12),
            })
        
        return base_style
    
    @classmethod
    def get_frame_style(cls) -> Dict[str, Any]:
        """Get frame styling configuration"""
        return {
            'corner_radius': cls.DIMENSIONS['border_radius'],
            'border_width': 0,
        }
    
    @classmethod  
    def get_label_style(cls, variant: str = "body") -> Dict[str, Any]:
        """Get label styling configuration"""
        font_config = cls.FONTS.get(variant, cls.FONTS['body'])
        
        return {
            'font': ctk.CTkFont(
                family=font_config[0], 
                size=font_config[1],
                weight=font_config[2]
            )
        }

# Global styles instance
ui_styles = ModernUIStyles()
'''

print("✅ Created CSV exporter and UI styles")
print("7. csv_exporter.py (smart_attendance_system/src/attendance/utils/csv_exporter.py)")  
print("8. ui_styles.py (smart_attendance_system/src/attendance/ui/ui_styles.py)")