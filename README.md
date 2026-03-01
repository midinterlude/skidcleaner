# Roblox Cleaner Package
 
A packaged executable version of skidcleaner, a powerful tool for cleaning Roblox-related files and registry entries with advanced ban evasion capabilities.

![Configuration UI](https://imgur.com/mSxITiW)

 
## 🚀 Quick Start
 
1. **Extract** the package to a directory of your choice
2. **Run** `skidcleaner.exe` as Administrator (required for registry operations)
3. The script will automatically install dependencies and clean your system
 
## 📁 Package Contents
 
- `skidcleaner.exe` - Main cleaning executable (compiled with PyInstaller)
- `skidcleaner.config.json` - Default configuration file
- `cacert.pem` - SSL certificate bundle for secure downloads
- `README.md` - This file
 
## ⚙️ Configuration
 
The script uses `skidcleaner.config.json` for settings. You can edit this file to customize behavior:
 
### Key Settings
 
- **General**: Logging, console capture, screen clearing
- **Cleaning**: Toggle file cleaning, process killing, registry cleanup
- **Roblox**: Download fresh client, auto-launch after cleaning
- **Tools**: Enable ByeBanAsync for advanced ban evasion
- **Advanced**: Command outputs, file deletion force, auto-restart
 
### Example Configuration
```json
{
  "general": {
    "log_enabled": true,
    "open_log_on_exit": true
  },
  "cleaning": {
    "kill_processes": true,
    "clean_folders": true,
    "clean_registry": true
  },
  "roblox": {
    "download_roblox": true,
    "launch_roblox_on_exit": false
  }
}
```
 
## 🔧 Usage
 
### Basic Usage
```bash
# Run with default settings
skidcleaner.exe
```
 
### Configuration
1. Run `webconfig.html` (any browser is fine)
2. Go through options and toggle what you want
3. put the given file within the same folder as skidcleaner.exe & cacert.pem
4. Run `skidcleaner.exe`
5. The script will use your custom configuration
 
## 🛡️ Features
 
### Comprehensive Cleaning
- ✅ Kill Roblox processes safely
- ✅ Clean temporary files and Roblox directories
- ✅ Remove Roblox cookies and cache
- ✅ Flush DNS cache
- ✅ Clean Windows registry entries
- ✅ Remove prefetch files
- ✅ Optional Explorer restart
- ✅ Removes any traces of files
 
### Roblox Management
- ✅ Download fresh Roblox client from WEAO API
- ✅ Auto-launch Roblox after cleaning
 
### Advanced Ban Evasion
- ✅ **ByeBanAsync Python Port** - Imported ByeBanAsync into python for proven MAC address spoofing (credits to: centerepic)
- ✅ **Registry cleanup** - Remove all Roblox traces
- ✅ **Network adapter management** - Restart adapters after changes
 
## 📋 Requirements
 
- **Windows 10/11**
- **Administrator privileges** (required for registry and file operations)
- **Internet connection** (for Roblox downloads)
 
## 🔍 Logs
 
All operations are logged to:
```
%temp%\Roblox_Cleaner_Log.txt
```
 
The log includes console history, command outputs, file operations, and error messages.
 
## ⚠️ Safety & Security
 
- **Administrator privileges required**
- **Backup important data** before running
- **Use at your own risk**

## ⚠️ Warning

- **Make sure** to log out of any roblox accounts on your browser
- **Clear your browsers's cookies** before running this application.
 
## 🐛 Troubleshooting
 
### Common Issues
 
1. **"Access Denied" Errors**
   - Ensure you're running as Administrator
   - Close any open Roblox applications
 
2. **Download Failures**
   - Check internet connection
   - Verify firewall/antivirus isn't blocking
   - Try using a VPN if downloads fail (We recommend Cloudflare Warp or ProtonVPN)
 
3. **Configuration Not Loading**
   - Ensure `skidcleaner.config.json` is in the same directory
   - Check JSON syntax with an online validator
 
## 👥 Support
 
For issues and support:
- Check the log file: `%temp%\Roblox_Cleaner_Log.txt`
- DM 'midinterlude' on Discord with the log file
 
---

https://github.com/midinterlude/skidcleaner
