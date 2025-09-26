"""
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
