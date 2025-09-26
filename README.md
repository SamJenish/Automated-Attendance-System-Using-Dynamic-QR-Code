# Smart Attendance System - Modern UI

🎓 A professional QR-code based attendance management system with modern UI design.

## ✨ Features

- **🎨 Modern UI**: Clean, minimal interface built with CustomTkinter
- **📱 QR Code System**: Automatic QR generation with 30-second refresh
- **📊 CSV Export**: One-click export of attendance records  
- **🔒 IP Security**: Network-based access control
- **🌓 Theme Support**: Light, Dark, and System themes
- **⚡ Real-time**: Live status monitoring and updates

## 🚀 Quick Start

### Prerequisites
- Python 3.13.7 (or higher)
- MySQL Server 8.0+

### Installation

1. **Extract all files** maintaining the folder structure shown below
2. **Install dependencies**:
   ```bashp
   pip install -r requirements.txt
   ```
3. **Setup database**:
   ```bash
   python database_setup.py
   ```
4. **Run application**:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
smart_attendance_system/
├── main.py                                    # Main entry point
├── requirements.txt                           # Dependencies
├── database_setup.py                          # Database setup
├── README.md                                  # This file
├── src/
│   └── attendance/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py                    # App configuration
│       ├── database/
│       │   ├── __init__.py
│       │   └── db_manager.py                  # Database operations
│       ├── core/
│       │   ├── __init__.py
│       │   ├── qr_generator.py               # QR code generation
│       │   └── flask_server.py               # Web server
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── main_window.py                # Main UI window
│       │   ├── ui_components.py              # UI components
│       │   └── ui_styles.py                  # UI styling
│       └── utils/
│           ├── __init__.py
│           └── csv_exporter.py               # CSV export
├── logs/                                      # Application logs
└── exports/                                   # CSV export files
```

## ⚙️ Configuration

Edit `src/attendance/config/settings.py` to customize:

- **Database settings**: Host, user, password, database name
- **Server settings**: Port, host binding
- **UI settings**: Window size, refresh interval, QR size

## 🎯 Usage

1. **Start the application** - Run `python main.py`
2. **QR codes generate automatically** every 30 seconds
3. **Students scan QR codes** with mobile devices to mark attendance
4. **Export data** using the "📊 Export CSV" button
5. **Change themes** using the appearance dropdown

## 📱 Student Setup

Students need to be registered in the database with their device IP addresses:

```sql
INSERT INTO students (regno, name, ip) VALUES 
('REG001', 'Student Name', '192.168.1.100');
```

## 🛠️ Troubleshooting

### Common Issues

- **Import errors**: Ensure all files are in correct locations
- **Database connection**: Check MySQL service and credentials
- **Port conflicts**: Default Flask port is 5000
- **Theme not applying**: Restart the application

### Logs

Check the `logs/` directory for detailed error information.

## 📊 Database Schema

### Students Table
- `id`: Auto-increment primary key
- `regno`: Student registration number (unique)
- `name`: Student full name  
- `ip`: Device IP address

### Attendance Table
- `id`: Auto-increment primary key
- `regno`: Student registration number
- `name`: Student name
- `ip`: Client IP address
- `timestamp`: Attendance date and time

## 🎨 UI Features

- **Responsive design** - Adapts to different screen sizes
- **Status indicators** - Real-time system monitoring
- **Modern components** - Professional button and card designs
- **Theme switching** - Light/Dark/System appearance modes
- **Clean layout** - Organized sidebar and main content areas

## 🔒 Security

- **IP-based access control** - Only registered devices can mark attendance
- **Network restrictions** - Same subnet requirement
- **Token expiration** - QR codes expire every 30 seconds
- **Input validation** - All inputs are sanitized

## 📈 System Requirements

- **Python**: 3.13.7 or higher
- **RAM**: Minimum 512MB
- **Storage**: 100MB free space
- **Network**: Local area network connectivity
- **Database**: MySQL 8.0+

## 🤝 Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Verify all files are in correct locations
3. Ensure database is properly configured
4. Check Python and dependency versions

---

**Smart Attendance System v2.0.0** - Professional attendance management solution
