"""
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
                    initialfile=default_filename
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
                f"✅ CSV file exported successfully!\n\n"
                f"📁 File: {os.path.basename(file_path)}\n"
                f"📊 Records: {len(records)}\n"
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
                created_at = record['created_at']
                writer.writerow({
                    'Registration Number': record['regno'],
                    'Student Name': record['name'],
                    'IP Address': record['ip'],
                    'Date': created_at.strftime('%Y-%m-%d'),
                    'Time': created_at.strftime('%H:%M:%S'),
                    'Full Timestamp': created_at.strftime('%Y-%m-%d %H:%M:%S')
                })

    def quick_export(self) -> bool:
        """Quick export with automatic filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"attendance_export_{timestamp}.csv"
        file_path = os.path.join(self.export_directory, filename)

        return self.export_all_records(file_path)

# Global CSV exporter instance
csv_exporter = AttendanceCSVExporter()
