"""
QR Code Generator - Generate QR codes for attendance
smart_attendance_system/src/attendance/core/qr_generator.py
"""
import qrcode
from PIL import Image, ImageTk
import socket
import logging
from ..config.settings import app_settings

logger = logging.getLogger(__name__)

class QRCodeGenerator:
    """Handles QR code generation for attendance tokens"""

    def __init__(self):
        self.qr_size = app_settings.QR_SIZE

    def get_local_ip(self) -> str:
        """Get local machine IP address"""
        try:
            # Connect to a remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            try:
                return socket.gethostbyname(socket.gethostname())
            except Exception as e:
                logger.error(f"❌ Error getting local IP: {e}")
                return "127.0.0.1"

    def create_qr_image(self, token: str, server_port: int = 5000) -> Image.Image:
        """Generate QR code image for attendance token"""
        try:
            local_ip = self.get_local_ip()
            scan_url = f"http://{local_ip}:{server_port}/scan/{token}"

            # Create QR code with optimal settings
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(scan_url)
            qr.make(fit=True)

            # Generate image with high contrast
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image = qr_image.resize(self.qr_size, Image.Resampling.LANCZOS)

            logger.info(f"📱 QR code generated: {scan_url}")
            return qr_image

        except Exception as e:
            logger.error(f"❌ Error generating QR code: {e}")
            raise

    def create_tkinter_image(self, token: str, server_port: int = 5000) -> ImageTk.PhotoImage:
        """Generate QR code as Tkinter PhotoImage"""
        qr_image = self.create_qr_image(token, server_port)
        return ImageTk.PhotoImage(qr_image)

# Global QR generator instance
qr_generator = QRCodeGenerator()
