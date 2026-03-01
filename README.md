# skidcleaner.

A very overkill option on roblox alt ban evasion for people who want 0 compromizes on their accounts :3

Everything here is designed with redundancy in mind

A powerful Python script for cleaning Roblox-related files, registry entries, and temporary data, with advanced ban evasion capabilities for users who want zero compromises on their accounts.

Download here:
https://github.com/midinterlude/skidcleaner./releases/tag/skidcleaner

## ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️
- THIS SHIT IS VIBE CODED AS FUCK.
- Half this shit is AI
- Don't come after me with a torch and a pitchfork if some shit is fucked
- You can control anything this app does... but i really dont recommend it


## Features

### 🧹 **Comprehensive Cleaning**
- Kills Roblox processes safely
- Cleans temporary files and folders
- Removes Roblox cookies
- Flushes DNS cache
- Cleans Windows registry entries
- Removes prefetch files
- Optional Explorer restart

### 🛡️ **Advanced Ban Evasion**
- MAC address spoofing capability
- Complete cookie deletion
- Network adapter management
- Registry cleanup
- Completely reinstalls roblox and removes any files or registeries linked to it

### ⚙️ **Advanced Configuration**
- You are in control of everything it does
- Interactive configuration editor
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

MAKE SURE TO CLEAR YOUR COOKIES AND CASHED DATA BEFORE RUNNING APPLICATION! ⚠️⚠️⚠️

### Standard Usage (Python file)

press win+r and type cmd
```bash
python cleaner.py
```
select standard run
select yes or no depending on what you want it to do
wait for it to finish
restart pc (if it doesn't automatically)

### Executable file

install the executable
run file
select standard run
select yes or no depending on what you want it to do
wait for it to finish
restart pc (if it doesn't automatically)

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
- a pc.

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
**Mainly actually coded by**: AI... shout out SWE-1.5 fast

## Support

For issues and support, DM 'midinterlude' on Discord with the log file from `%temp%\Roblox_Cleaner_Log.txt`.

---

**⚠️ Disclaimer**: This script modifies system files and registry. Use at your own risk and ensure you have appropriate backups.
