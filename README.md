<div align="center">

# Slate - https://discord.gg/HQbG5NFAS3
 
A packaged executable version of slate, a powerful tool for cleaning Roblox-related files and registry entries with advanced ban evasion capabilities.

---

## 🚀 Quick Start
</div>

1. **Extract** the package to a directory of your choice.
2. **Run** `slate.exe` as Administrator (required for registry operations).
3. The script will automatically install dependencies and clean your system.

<div align="center">

## 📁 Package Contents
</div>

* `slate.exe` - Main cleaning executable (compiled with PyInstaller)
* `slate.config.json` - Default configuration file
* `cacert.pem` - SSL certificate bundle for secure downloads
* `README.md` - This file

<div align="center">

## ⚙️ Configuration
</div>

The script uses `slate.config.json` for settings. You can edit this file to customize behavior:
You can use the web configurator [here](https://midinterlude.github.io/slate/)

### Key Settings

* **General**: Logging, console capture, screen clearing.
* **Cleaning**: Toggle file cleaning, process killing, registry cleanup.
* **Roblox**: Download fresh client, auto-launch after cleaning.
* **Tools**: Enable ByeBanAsync for advanced ban evasion.
* **Advanced**: Command outputs, file deletion force, auto-restart.

### Example Configuration
```json
{
    "general": {
        "log_enabled": true,
        "open_log_on_exit": false,
        "capture_console_history": true,
        "clear_screen_on_sections": false
    },
    "cleaning": {
        "kill_processes": true,
        "clean_folders": true,
        "remove_cookies": true,
        "flush_dns": true,
        "clean_registry": false,
        "clean_prefetch": false,
        "restart_explorer": false
    },
    "roblox": {
        "download_roblox": false,
        "launch_roblox_on_exit": false,
        "create_appsettings": false
    },
    "tools": {
        "run_byebanasync": true
    },
    "paths": {
        "temp_folders": [
            "%temp%",
            "%temp%/*",
            "%localappdata%\\Temp"
        ],
        "roblox_folders": [
            "%localappdata%\\Roblox",
            "%appdata%\\Roblox",
            "%appdata%\\Local\\Roblox"
        ]
    },
    "processes": {
        "roblox_processes": [
            "RobloxPlayerBeta.exe",
            "RobloxPlayerLauncher.exe"
        ]
    },
    "registry": {
        "roblox_keys": [
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Roblox",
            "HKEY_CURRENT_USER\\SOFTWARE\\Roblox"
        ]
    },
    "advanced": {
        "show_command_output": false,
        "force_file_deletion": false,
        "skip_confirmation_prompts": false,
        "auto_restart_after_cleaning": false
    }
}
```
<div align="center">

### Basic Usage
</div>
<div align="left">
```bash
# Run with default settings
slate.exe
```
</div>

<div align="center">

### Configuration

</div>
<div align="left">
1. Run `config.html` (any browser is fine)\
2. Go through options and toggle what you want\
3. put the given file within the same folder as slate.exe & cacert.pem\
4. Run `slate.exe`\
5. The script will use your custom configuration\
</div>

<div align="center">

## 🛡️ Features

</div>

<div align="center">

### Comprehensive Cleaning

</div>
<div align="left">
- ✅ Kill Roblox processes safely\
- ✅ Clean temporary files and Roblox directories\
- ✅ Remove Roblox cookies and cache\
- ✅ Flush DNS cache\
- ✅ Clean Windows registry entries\
- ✅ Remove prefetch files\
- ✅ Optional Explorer restart\
- ✅ Removes any traces of files
</div>
<div align="center">

### Roblox Management

</div>
<div align="left">
- ✅ Download fresh Roblox client from WEAO API\
- ✅ Auto-launch Roblox after cleaning\
</div>
<div align="center">

### Advanced Ban Evasion

</div>
<div align="left">
- ✅ **ByeBanAsync Python Port** - Imported ByeBanAsync into python for proven MAC address spoofing (credits to: centerepic)\
- ✅ **Registry cleanup** - Remove all Roblox traces\
- ✅ **Network adapter management** - Restart adapters after changes
 </div>

<div align="center">

## 📋 Requirements

</div>
<div align="left">
- **Windows 10/11**\
- **Administrator privileges** (required for registry and file operations)\
- **Internet connection** (for Roblox downloads)
 </div>

<div align="center">

## 🔍 Logs

</div>
<div align="left">
All operations are logged to:\
```
%temp%\slate\slate.log
```\
 
The log includes console history, command outputs, file operations, and error messages.

</div>
<div align="center">

## ⚠️ Safety & Security

</div>
<div align="left">
- **Administrator privileges required**\
- **Backup important data** before running\
- **Use at your own risk**
</div>

<div align="center">

## ⚠️ Warning

</div>
<div align="left">
- **Make sure** to log out of any roblox accounts on your browser\
- **Clear your browsers's cookies** before running this application.
 
</div>
<div align="center">

## 🐛 Troubleshooting

</div>

 <div align="center">

### Common Issues

</div>
<div align="left">
1. **"Access Denied" Errors**\
   - Ensure you're running as Administrator\
   - Close any open Roblox applications\\
 
2. **Download Failures**\
   - Check internet connection\
   - Verify firewall/antivirus isn't blocking\
   - Try using a VPN if downloads fail (We recommend Cloudflare Warp or ProtonVPN)\
 
3. **Configuration Not Loading**\
   - Ensure `slate.config.json` is in the same directory\
   - Check JSON syntax with an online validator\
</div>
<div align="center">

## 👥 Support

</div>
<div align="left">
For issues and support:\
- Check the log file: `%temp%\slate\slate.log`\
- DM 'midinterlude' on Discord with the log file\
- additionally, you can join the discord server found [here](https://discord.gg/HQbG5NFAS3)\\
 
---\\

https://github.com/midinterlude/slate\
</div>
