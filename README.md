# File Interceptor

## Overview

The **File Interceptor** is a monitoring tool designed to observe file activities such as creation, modification, deletion, and movement within a specified directory. It enhances security and auditing by providing logging, notifications, and integrity checks for monitored files.

## Features

1. **Logging Features**

   - Logs file events (creation, modification, deletion, movement) with timestamps and severity levels.
   - Uses a rotating log file to manage size and backups.

2. **File Monitoring Capabilities**

   - Monitors specific directories for file activity.
   - Filters events based on file extensions (e.g., `.exe`, `.docx`, `.py`).

3. **Real-Time Notifications**

   - Sends email alerts for critical file events.

4. **Security Enhancements**

   - Verifies file integrity using SHA-256 checksum.

5. **Performance Optimization**
   - Runs monitoring in a separate thread for efficient performance.

## Prerequisites

1. **Python Version**: Ensure Python 3.8 or higher is installed.
2. **Required Libraries**: Install the following Python modules:
   ```bash
   pip install watchdog
   ```
3. **Email Setup**:
   - Configure the `SMTP_SERVER`, `EMAIL_ADDRESS`, and `EMAIL_PASSWORD` in the script.
   - Ensure the email account supports SMTP access (e.g., enable app-specific passwords for Gmail).

## Configuration

1. **Directory to Monitor**:

   - Set the `MONITORED_DIR` variable to the absolute path of the directory you want to monitor.

2. **File Filters**:

   - Adjust the `FILE_EXTENSIONS` list to specify file types to monitor.

   Example:

   ```python
   FILE_EXTENSIONS = [".exe", ".docx", ".py"]
   ```

## How to Run

1. Save the script as `file_interceptor.py`.
2. Run the script in your terminal:
   ```bash
   python file_interceptor.py
   ```
3. The tool will begin monitoring the specified directory and log activities to `file_interceptor.log`.

## Logs

- Logs are stored in `file_interceptor.log`.
- Log files rotate automatically when they exceed 5MB.
- Log format: `YYYY-MM-DD HH:MM:SS - LEVEL - Message`

## Notifications

- Critical events trigger email alerts sent to the configured email address.

## Issues and Troubleshooting

- **SMTP Configuration Error**:

  - Ensure correct SMTP server, port, and login credentials.
  - Check for firewall or antivirus blocking SMTP access.

- **Permission Issues**:
  - Run the script with appropriate permissions to access the monitored directory.

