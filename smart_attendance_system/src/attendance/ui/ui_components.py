"""
UI Components - Reusable modern UI components
smart_attendance_system/src/attendance/ui/ui_components.py
"""
import customtkinter as ctk
from typing import Callable, Optional
from datetime import datetime
from PIL import ImageTk

from .ui_styles import ui_styles

class StatusCard(ctk.CTkFrame):
    """Status indicator card component"""

    def __init__(self, parent, title: str, status: str = "offline", **kwargs):
        super().__init__(parent, **ui_styles.get_frame_style(), **kwargs)

        self.title = title
        self.current_status = status

        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            **ui_styles.get_label_style("body_small")
        )
        self.title_label.pack(pady=(12, 4))

        # Status label with icon
        self.status_label = ctk.CTkLabel(
            self,
            text=self._get_status_display(status),
            **ui_styles.get_label_style("body")
        )
        self.status_label.pack(pady=(0, 12))

    def _get_status_display(self, status: str) -> str:
        """Get status display with icon"""
        status_map = {
            'online': '🟢 Online',
            'offline': '🔴 Offline',
            'warning': '🟡 Warning',
            'error': '🔴 Error',
            'connecting': '🟡 Connecting...',
        }
        return status_map.get(status, '⚪ Unknown')

    def update_status(self, new_status: str):
        """Update the status display"""
        self.current_status = new_status
        self.status_label.configure(text=self._get_status_display(new_status))

class InfoCard(ctk.CTkFrame):
    """Information display card"""

    def __init__(self, parent, title: str, value: str = "...", **kwargs):
        super().__init__(parent, **ui_styles.get_frame_style(), **kwargs)

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            **ui_styles.get_label_style("body_small")
        )
        self.title_label.pack(pady=(12, 4))

        # Value
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            **ui_styles.get_label_style("body")
        )
        self.value_label.pack(pady=(0, 12))

    def update_value(self, new_value: str):
        """Update the displayed value"""
        self.value_label.configure(text=new_value)

class ActionButton(ctk.CTkButton):
    """Styled action button with icon"""

    def __init__(self, parent, text: str, icon: str = "", variant: str = "primary", 
                 command: Optional[Callable] = None, **kwargs):

        # Get button styling
        style = ui_styles.get_button_style(variant)
        style.update(kwargs)

        # Combine icon and text
        button_text = f"{icon} {text}".strip()

        super().__init__(parent, text=button_text, command=command, **style)

class QRDisplayArea(ctk.CTkFrame):
    """QR code display area with information"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **ui_styles.get_frame_style(), **kwargs)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(
            self,
            text="🎯 Scan QR Code to Mark Attendance",
            **ui_styles.get_label_style("heading")
        )
        self.header_label.grid(row=0, column=0, padx=24, pady=(24, 16))

        # QR code display
        self.qr_label = ctk.CTkLabel(
            self,
            text="🔄 Generating QR Code...",
            **ui_styles.get_label_style("body"),
            width=ui_styles.DIMENSIONS['qr_display_size'][0],
            height=ui_styles.DIMENSIONS['qr_display_size'][1]
        )
        self.qr_label.grid(row=1, column=0, padx=24, pady=16)

        # Info cards frame
        self.info_frame = ctk.CTkFrame(self, **ui_styles.get_frame_style())
        self.info_frame.grid(row=2, column=0, sticky="ew", padx=24, pady=(16, 24))
        self.info_frame.grid_columnconfigure((0, 1), weight=1)

        # Token info card
        self.token_card = InfoCard(self.info_frame, "Current Token", "Generating...")
        self.token_card.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="ew")

        # Expiry info card
        self.expiry_card = InfoCard(self.info_frame, "Expires At", "--:--:--")
        self.expiry_card.grid(row=0, column=1, padx=(8, 0), pady=8, sticky="ew")

    def update_qr_display(self, qr_image: ImageTk.PhotoImage, token: str, expiry_time: str):
        """Update QR code display with new image and info"""
        # Update QR image
        self.qr_label.configure(image=qr_image, text="")
        self.qr_label.image = qr_image  # Keep reference to prevent garbage collection

        # Update info cards
        self.token_card.update_value(f"...{token[-8:]}")
        self.expiry_card.update_value(expiry_time)

    def show_loading_message(self, message: str = "🔄 Generating QR Code..."):
        """Show loading message"""
        self.qr_label.configure(image=None, text=message)
        if hasattr(self.qr_label, 'image'):
            delattr(self.qr_label, 'image')

class ControlPanel(ctk.CTkFrame):
    """Control panel with action buttons and settings"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **ui_styles.get_frame_style(), **kwargs)

        self.grid_columnconfigure(0, weight=1)

        current_row = 0

        # Controls section header
        self.controls_label = ctk.CTkLabel(
            self,
            text="📋 Controls",
            **ui_styles.get_label_style("subheading")
        )
        self.controls_label.grid(row=current_row, column=0, padx=20, pady=(20, 16))
        current_row += 1

        # Export CSV button
        self.export_button = ActionButton(
            self,
            text="Export CSV",
            icon="📊",
            variant="primary"
        )
        self.export_button.grid(row=current_row, column=0, padx=20, pady=8, sticky="ew")
        current_row += 1

        # Refresh QR button
        self.refresh_button = ActionButton(
            self,
            text="Refresh QR",
            icon="🔄",
            variant="secondary"
        )
        self.refresh_button.grid(row=current_row, column=0, padx=20, pady=8, sticky="ew")
        current_row += 1

        # Settings section
        self.settings_label = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            **ui_styles.get_label_style("subheading")
        )
        self.settings_label.grid(row=current_row, column=0, padx=20, pady=(24, 16))
        current_row += 1

        # Theme selector
        self.theme_label = ctk.CTkLabel(
            self,
            text="Appearance:",
            **ui_styles.get_label_style("body_small")
        )
        self.theme_label.grid(row=current_row, column=0, padx=20, pady=(0, 4), sticky="w")
        current_row += 1

        self.theme_selector = ctk.CTkOptionMenu(
            self,
            values=["System", "Light", "Dark"],
            height=ui_styles.DIMENSIONS['input_height'],
            corner_radius=ui_styles.DIMENSIONS['border_radius']
        )
        self.theme_selector.grid(row=current_row, column=0, padx=20, pady=(0, 16), sticky="ew")
        current_row += 1

    def bind_commands(self, export_command: Callable, refresh_command: Callable, 
                     theme_command: Callable):
        """Bind command functions to controls"""
        self.export_button.configure(command=export_command)
        self.refresh_button.configure(command=refresh_command)
        self.theme_selector.configure(command=theme_command)

class SystemStatusPanel(ctk.CTkFrame):
    """System status monitoring panel"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **ui_styles.get_frame_style(), **kwargs)

        # Status section header
        self.status_label = ctk.CTkLabel(
            self,
            text="🖥️ System Status",
            **ui_styles.get_label_style("subheading")
        )
        self.status_label.pack(pady=(20, 16))

        # Server status card
        self.server_status = StatusCard(self, "Flask Server", "offline")
        self.server_status.pack(fill="x", padx=16, pady=4)

        # Database status card
        self.database_status = StatusCard(self, "Database", "offline")
        self.database_status.pack(fill="x", padx=16, pady=4)

        # IP address display
        self.ip_label = ctk.CTkLabel(
            self,
            text="📡 IP: Detecting...",
            **ui_styles.get_label_style("body_small")
        )
        self.ip_label.pack(pady=(8, 20))

    def update_server_status(self, status: str):
        """Update server status"""
        self.server_status.update_status(status)

    def update_database_status(self, status: str):
        """Update database status"""
        self.database_status.update_status(status)

    def update_ip_address(self, ip: str):
        """Update IP address display"""
        self.ip_label.configure(text=f"📡 IP: {ip}")
