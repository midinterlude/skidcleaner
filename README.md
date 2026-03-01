# skidcleaner.

A very overkill option on roblox alt ban evasion for people who want 0 compromizes on their accounts :3

A powerful Python script for cleaning Roblox-related files, registry entries, and temporary data, with advanced ban evasion capabilities for users who want zero compromises on their accounts.

Download here:
https://github.com/midinterlude/skidcleaner./releases/tag/skidcleaner

## ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️
- THIS SHIT IS VIBE CODED AS FUCK.
- Don't come after me with a torch and a pitchfork if some shit is fucked
- anyways imma let chatgpt describe it


## Features

### 🧹 **Comprehensive Cleaning**
- Kill Roblox processes safely
- Clean temporary files and folders
- Remove Roblox cookies
- Flush DNS cache
- Clean Windows registry entries
- Remove prefetch files
- Optional Explorer restart

### 🎮 **Roblox Management**
- Download fresh Roblox client from WEAO API
- Install with RDD (Roblox Deployment Downloader) format
- Create required AppSettings.xml
- Launch Roblox after cleaning

### 🛡️ **Advanced Ban Evasion**
- **Overkill**: Maximum privacy and security for users who want zero compromises
- MAC address spoofing capability
- Complete cookie deletion
- Network adapter management
- Registry cleanup

### ⚙️ **Advanced Configuration**
- JSON-based configuration system
- Interactive configuration editor
- Skip confirmation prompts option
- Customizable paths and processes
- Toggle individual cleaning operations

## Installation

### Recommended Installation:

- go to https://github.com/midinterlude/skidcleaner./releases/tag/skidcleaner
- download skidcleaner.exe and cleaner_config.json
- put in the same folder and run

### Python Installation

1. Ensure Python 3.7+ is installed
2. Install cleaner.py
3. Run the script as Administrator (required for registry operations)
4. Install dependencies automatically handled by script

## Usage

### Standard Usage (Python file)

press win+r and type cmd
```bash
python cleaner.py
```

## Overkill - Zero Compromise Approach

This script is VERY **overkill** designed for users who want absolutely no traces or compromises on their Roblox accounts. This is perfect for:

- **Privacy-conscious users** who want zero data retention
- **Security-focused users** who want maximum protection
- **Alt account users** who need complete isolation
- **Users avoiding detection** who want no digital footprints

### Overkill Features:
- **Complete cookie deletion** (including all Roblox data files)
- **MAC address spoofing** to change network identity
- **Registry cleanup** to remove all Roblox traces
- **Prefetch deletion** to prevent Windows from caching Roblox data
- **Process termination** for all Roblox-related applications
- **DNS cache flushing** to clear network resolution history

## Configuration

The script uses `cleaner_config.json` for settings. If the file doesn't exist, default settings are used.

### Configuration Sections

#### General
- `log_enabled`: Enable/disable logging
- `open_log_on_exit`: Open log file when script finishes
- `capture_console_history`: Save console content before clearing screen
- `clear_screen_on_sections`: Clear screen between operations

#### Cleaning
- `kill_processes`: Terminate Roblox processes
- `clean_folders`: Clean Roblox directories
- `remove_cookies`: Delete Roblox cookies
- `flush_dns`: Flush DNS cache
- `restart_explorer`: Restart Windows Explorer
- `clean_registry`: Clean registry entries
- `clean_prefetch`: Remove prefetch files

#### Roblox
- `download_roblox`: Download fresh client
- `launch_roblox_on_exit`: Auto-launch after cleaning
- `create_appsettings`: Create AppSettings.xml

#### Tools
- `run_byebanasync`: Run ByeBanAsync functionality

#### Paths
- `temp_folders`: Temporary directories to clean
- `roblox_folders`: Roblox directories to clean

#### Processes
- `roblox_processes`: Process names to terminate

#### Registry
- `registry_paths`: Registry keys to delete

#### Advanced
- `show_command_output`: Log command outputs
- `force_file_deletion`: Force delete stubborn files
- `skip_confirmation_prompts`: Run without user prompts
- `auto_restart_after_cleaning`: Auto-restart when done

## Logging

All operations are logged to:
```
%temp%\Roblox_Cleaner_Log.txt
```

The log includes:
- Console history capture (when enabled)
- Command execution with outputs
- File operations
- Error messages
- Success/failure status

## Security Features

### ByeBanAsync Integration
- Cookie file deletion
- MAC address spoofing
- Network adapter management
- Interactive adapter selection

### MAC Address Spoofing
- Generates random MAC addresses starting with `02` (wireless compatible)
- Updates Windows registry directly
- Restarts network adapters to apply changes
- Supports multiple network adapters

## File Structure

```
pythonprojects/
├── cleaner.py                 # Main script
├── cleaner_config.json        # Configuration file
└── README.md                # This file
```

## Requirements

### Python Dependencies
- `pyuac` - Administrator privilege elevation
- `requests` - HTTP requests for downloads
- `winreg` - Windows registry access (built-in)

### System Requirements
- Windows 10/11
- Administrator privileges
- Internet connection (for Roblox download)

## Safety Features

- **Backup protection**: Won't delete system files
- **Error handling**: Comprehensive try-catch blocks
- **Permission handling**: Multiple deletion attempts for stubborn files
- **Confirmation prompts**: User control over operations
- **Logging**: Complete audit trail of all actions

## Troubleshooting

### Common Issues

1. **"Access Denied" Errors**
   - Run as Administrator
   - Check if files are in use

2. **Download Failures**
   - Check internet connection
   - Verify WEAO API is accessible
   - Check firewall settings
   - Download and use Cloudflare Warp

3. **Registry Access Denied**
   - Ensure Administrator privileges
   - Check antivirus interference

4. **MAC Address Issues**
   - Run as Administrator
   - Select correct network adapter
   - Restart PC if changes don't apply

## Credits

**Original Author**: midinterlude  
**ByeBanAsync**: centerepic
**Enhanced by**: Advanced configuration and Python integration

## Support

For issues and support, DM 'midinterlude' on Discord with the log file from `%temp%\Roblox_Cleaner_Log.txt`.

---

**⚠️ Disclaimer**: This script modifies system files and registry. Use at your own risk and ensure you have appropriate backups.
