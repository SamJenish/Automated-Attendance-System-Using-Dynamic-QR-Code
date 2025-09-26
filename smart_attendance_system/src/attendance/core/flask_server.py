"""
Flask Server - Handle QR code scanning requests
smart_attendance_system/src/attendance/core/flask_server.py
"""
from flask import Flask, jsonify, request
from datetime import datetime
import logging
import threading
import socket
from typing import Optional, Dict, Any, Tuple

from ..database.db_manager import database_manager
from ..config.settings import server_config

logger = logging.getLogger(__name__)

class AttendanceFlaskServer:
    """Flask server for handling QR scan requests"""

    def __init__(self):
        self.app = Flask(__name__)
        self.app.logger.disabled = True  # Disable Flask logging

        self.current_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False

        self._setup_routes()

    def get_local_ip(self) -> str:
        """Get local machine IP address"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route("/scan/<token>", methods=['GET', 'POST'])
        def handle_scan(token: str):
            return self._process_scan(token)

        @self.app.route("/health")
        def health_check():
            return jsonify({
                "status": "healthy", 
                "timestamp": datetime.now().isoformat(),
                "server": "online"
            })

        @self.app.route("/api/status")
        def api_status():
            return jsonify({
                "server": "online",
                "database": "online" if database_manager.connection else "offline",
                "current_token": self.current_token[-8:] if self.current_token else None,
                "expires": self.token_expiry.isoformat() if self.token_expiry else None
            })

    def _process_scan(self, token: str) -> Tuple[Dict[str, Any], int]:
        """Process QR code scan request"""
        client_ip = request.remote_addr
        logger.info(f"📱 Scan request from {client_ip} with token {token}")

        # Validate token
        if not self._is_token_valid(token):
            logger.warning(f"⏰ Invalid/expired token from {client_ip}")
            return jsonify({
                "status": "⏰ QR Code Expired",
                "error": "TOKEN_INVALID",
                "message": "Please scan the latest QR code"
            }), 403

        # Validate network (same subnet)
        if not self._is_network_allowed(client_ip):
            logger.warning(f"🚫 Access blocked from {client_ip}")
            return jsonify({
                "status": "🚫 Access Denied", 
                "error": "NETWORK_BLOCKED",
                "message": "Access from this network is not allowed"
            }), 403

        # Process attendance
        return self._mark_student_attendance(client_ip)

    def _is_token_valid(self, token: str) -> bool:
        """Check if token is valid and not expired"""
        if not self.current_token or not self.token_expiry:
            return False

        if token != self.current_token:
            return False

        return datetime.now() <= self.token_expiry

    def _is_network_allowed(self, client_ip: str) -> bool:
        """Check if client IP is from allowed network"""
        try:
            server_ip = self.get_local_ip()
            # Allow same subnet (first 3 octets)
            client_network = ".".join(client_ip.split(".")[:3])
            server_network = ".".join(server_ip.split(".")[:3])
            return client_network == server_network
        except Exception as e:
            logger.error(f"❌ Network validation error: {e}")
            return False

    def _mark_student_attendance(self, client_ip: str) -> Tuple[Dict[str, Any], int]:
        """Mark attendance for student"""
        try:
            # Get student info
            student = database_manager.get_student_by_ip(client_ip)

            if not student:
                logger.info(f"❓ Unknown device: {client_ip}")
                return jsonify({
                    "status": "❓ Device Not Registered",
                    "error": "DEVICE_UNKNOWN",
                    "message": f"Device {client_ip} is not registered",
                    "ip": client_ip
                }), 200

            # Mark attendance
            attendance_time = datetime.now()
            success = database_manager.mark_attendance(
                student["regno"],
                student["name"], 
                client_ip,
                attendance_time
            )

            if success:
                logger.info(f"✅ Attendance: {student['regno']} ({student['name']})")
                return jsonify({
                    "status": "✅ Attendance Recorded",
                    "student": {
                        "regno": student["regno"],
                        "name": student["name"]
                    },
                    "timestamp": attendance_time.strftime('%H:%M:%S'),
                    "date": attendance_time.strftime('%Y-%m-%d')
                }), 200
            else:
                return jsonify({
                    "status": "⚠️ Database Error",
                    "error": "DB_ERROR",
                    "message": "Failed to record attendance"
                }), 500

        except Exception as e:
            logger.error(f"💥 Error processing attendance: {e}")
            return jsonify({
                "status": "💥 Server Error",
                "error": "SERVER_ERROR", 
                "message": "Internal server error"
            }), 500

    def update_token(self, token: str, expiry: datetime):
        """Update current token and expiry time"""
        self.current_token = token
        self.token_expiry = expiry
        logger.debug(f"🔄 Token updated: {token} expires {expiry.strftime('%H:%M:%S')}")

    def start(self):
        """Start Flask server in background thread"""
        if self.is_running:
            return

        self.is_running = True
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        logger.info(f"🌐 Flask server started on {self.get_local_ip()}:{server_config.PORT}")

    def _run_server(self):
        """Run Flask server"""
        try:
            # Suppress Werkzeug logs
            import logging as werkzeug_logging
            werkzeug_logging.getLogger('werkzeug').setLevel(werkzeug_logging.ERROR)

            self.app.run(
                host=server_config.HOST,
                port=server_config.PORT,
                debug=server_config.DEBUG,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            logger.error(f"💥 Flask server error: {e}")
            self.is_running = False

    def stop(self):
        """Stop Flask server"""
        if self.is_running:
            self.is_running = False
            logger.info("🛑 Flask server stopped")

# Global server instance
attendance_server = AttendanceFlaskServer()
