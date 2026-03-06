<picture>
  <source
    width="100%"
    srcset="./851x315.png"
    media="(prefers-color-scheme: dark)"
  />
  <source
    width="100%"
    srcset="./docs/content/public/banner-light-1280x640.avif"
    media="(prefers-color-scheme: light), (prefers-color-scheme: no-preference)"
  />
  <img width="250" src="./docs/content/public/banner-light-1280x640.avif" />
</picture>

<h1 align="center"></h1>

<p align="center">Advanced anti-alt detection system for Roblox with comprehensive cleaning, privacy protection, and network spoofing capabilities.</p>

<p align="center">
  [<a href="https://github.com/midinterlude/Slate">GitHub Repository</a>] [<a href="https://midinterlude.github.io/slate">Configuration</a>] [<a href="#installation">Installation</a>] [<a href="#features">Features</a>]
</p>

<p align="center">
  <a href="https://github.com/midinterlude/Slate/blob/main/LICENSE"><img src="https://img.shields.io/github/license/midinterlude/Slate.svg?style=flat&colorA=080f12&colorB=1fa669"></a>
  <a href="https://github.com/midinterlude/Slate/stargazers"><img src="https://img.shields.io/github/stars/midinterlude/Slate.svg?style=flat&colorA=080f12&colorB=1fa669"></a>
  <a href="https://github.com/midinterlude/Slate/forks"><img src="https://img.shields.io/github/forks/midinterlude/Slate.svg?style=flat&colorA=080f12&colorB=1fa669"></a>
  <a href="https://github.com/midinterlude/Slate/issues"><img src="https://img.shields.io/github/issues/midinterlude/Slate.svg?style=flat&colorA=080f12&colorB=1fa669"></a>
  <a href="https://github.com/midinterlude"><img src="https://img.shields.io/badge/author-midinterlude-black?style=flat&logo=github&labelColor=%23101419&color=%232d2e30"></a>
  <a href="https://discord.gg/bP3XKVRGmf"><img src="https://img.shields.io/badge/join-discord-blue?style=flat&logo=discord&labelColor=%235865F2&color=%235865F2"></a>
</p>

> Built with Python for comprehensive system cleaning and privacy protection. Designed specifically for Roblox users who need advanced anti-detection capabilities.

> [!WARNING]
> **Attention:** This tool is intended for educational and legitimate privacy protection purposes only. Use responsibly and in accordance with platform terms of service.

> [!NOTE]
> Slate requires a configuration file to function properly. Visit the [configuration page](https://midinterlude.github.io/slate) to generate your personalized `slate.config.json` file.

> [!TIP]
> For maximum effectiveness, run Slate as administrator and consider restarting your system after cleaning to ensure all changes take effect.

Have you been struggling with Roblox alt detection and need a comprehensive solution to protect your privacy?

With the increasing sophistication of detection systems, users need advanced tools that can thoroughly clean digital footprints and provide network-level protection. Traditional cleaning methods often miss critical traces that can be used for identification.

> But, what about having a tool that handles everything from file cleaning to MAC address spoofing?

Perhaps you've tried basic cleaners that only scratch the surface. They leave behind registry entries, prefetch files, cookies, and network identifiers that can still be used to track you. **Slate provides a complete solution: deep system cleaning, network spoofing, and automated Roblox management**.

## Recent Updates

- [Slate v3.0 Release](https://github.com/midinterlude/Slate) - Complete rewrite with enhanced error handling and logging
- [ByeBanAsync Integration](https://github.com/midinterlude/Slate) - Added MAC address spoofing capabilities
- [Configuration System](https://midinterlude.github.io/slate) - Web-based configuration generator for easy setup
- [Enhanced Logging](https://github.com/midinterlude/Slate) - Detailed operation logging with error tracking

## What Makes Slate Special?

Unlike other cleaning tools that focus only on basic file deletion, Slate was built with **comprehensive privacy protection** as the primary goal.

> [!TIP]
> Worried about incomplete cleaning leaving traces behind?
>
> Don't worry! Slate uses multiple layers of cleaning including file deletion, registry cleanup, process termination, DNS flushing, and network adapter spoofing. The multi-vector approach ensures maximum privacy protection.

This means that **Slate provides complete digital footprint elimination** covering files, registry entries, network identifiers, and application data. The configurable nature allows users to customize the cleaning process to their specific needs.

> [!NOTE]
>
> Slate is perfect for users who need comprehensive privacy protection and anti-detection capabilities.
>
> It's ideal if you're concerned about:
>
> - Account tracking and linking
> - Digital fingerprinting
> - Network-level identification
> - Incomplete cleaning by basic tools
>
> Technologies and capabilities:
>
> - Python-based system cleaning
> - Windows registry manipulation
> - Network adapter MAC address spoofing
> - Process termination and management
> - Roblox client automation
> - Comprehensive logging and error tracking
> - Web-based configuration management
>
> **Perfect for:**
> - Privacy-conscious users
> - People who miss their favorite game but can't get back on it because of a ban ;)
> - Digital privacy advocates

## Current Features

✅ **Core Cleaning Operations**
  - [x] Process Termination
    - [x] Roblox process killing
    - [x] Forced termination support
    - [x] Process validation
  - [x] File System Cleaning
    - [x] Temp folder cleanup
    - [x] Roblox directory removal
    - [x] Force deletion capabilities
    - [x] Prefetch file cleanup
  - [x] Registry Cleanup
    - [x] Roblox registry entries
    - [x] User profile cleaning
    - [x] System registry paths
  - [x] Cookie Removal
    - [x] Roblox cookie deletion
    - [x] Browser data cleanup
    - [x] Session data removal

✅ **Network & Privacy**
  - [x] MAC Address Spoofing (ByeBanAsync)
    - [x] Network adapter detection
    - [x] Random MAC generation
    - [x] Adapter restart automation
  - [x] DNS Cache Flushing
    - [x] Network cache clearing
    - [x] Connection reset
  - [x] Explorer Restart
    - [x] Shell refresh
    - [x] Cache clearing

✅ **Roblox Management**
  - [x] Client Download
    - [x] Version management
    - [x] Past version support
    - [x] Package extraction
  - [x] Automatic Launch
    - [x] Version detection
    - [x] Process monitoring
  - [x] AppSettings Creation
    - [x] Configuration management
    - [x] Custom settings

## Installation & Setup

> For detailed instructions, see the [Installation Guide](#installation) section below.

> [!NOTE]
> Slate requires Python 3.7+ and administrator privileges for full functionality. Some features may be limited without elevated permissions.

### Prerequisites

**For Python Users:**
```shell
# Python 3.7 or higher
python --version

# Required packages (auto-installed)
pip install requests tqdm
```

**For EXE Users:**
- Windows 10/11
- Administrator privileges (recommended)
- Internet connection for Roblox downloads
- SSL certificate bundle (`cacert.pem`) for secure downloads

### Quick Setup

#### Option 1: Using the Precompiled EXE (Recommended)

1. **Download the EXE**: Get the latest `Slate.exe` from the [GitHub Releases](https://github.com/midinterlude/Slate/releases)
2. **Download Configuration**: Visit [https://midinterlude.github.io/slate](https://midinterlude.github.io/slate) to generate your `slate.config.json`
3. **Download SSL Certificate**: Get `cacert.pem` from the repository or [Mozilla's certificate bundle](https://curl.se/docs/caextract.html)
4. **Place Files**: Put `Slate.exe`, `slate.config.json`, and `cacert.pem` in the same folder
5. **Run as Administrator**: Right-click `Slate.exe` and select "Run as administrator"
6. **Follow Prompts**: The application will guide you through the cleaning process

#### Option 2: Using Python Script

```shell
# Clone the repository
git clone https://github.com/midinterlude/Slate.git
cd Slate

# Download configuration file
# Visit: https://midinterlude.github.io/slate
# Place slate.config.json in the same directory as slate.py

# Run Slate
python slate.py
```

### Configuration

1. **Generate Configuration**: Visit [https://midinterlude.github.io/slate](https://midinterlude.github.io/slate)
2. **Customize Settings**: Select which cleaning operations to enable
3. **Download Config**: Save the generated `slate.config.json` file
4. **Place File**: Put the config file in the same directory as `slate.py`

### Advanced Setup

For power users, the configuration file supports granular control:

```json
{
  "general": {
    "log_enabled": true,
    "open_log_on_exit": true,
    "clear_screen_on_sections": false
  },
  "cleaning": {
    "kill_processes": true,
    "clean_folders": true,
    "remove_cookies": true,
    "flush_dns": true,
    "clean_registry": true,
    "clean_prefetch": true,
    "restart_explorer": false
  },
  "roblox": {
    "download_roblox": true,
    "use_past_versions": false,
    "launch_roblox_on_exit": true,
    "create_appsettings": true
  },
  "tools": {
    "run_byebanasync": true
  },
  "advanced": {
    "auto_restart_after_cleaning": false,
    "skip_confirmation_prompts": false,
    "force_file_deletion": true
  }
}
```

## File Structure

### For EXE Users:
```
Slate/
├── Slate.exe               # Precompiled executable
├── slate.config.json       # Configuration file (download from web)
├── cacert.pem              # SSL certificate bundle for secure downloads
└── README.md               # This file
```

### For Python Users:
```
Slate/
├── slate.py                # Main application script
├── slate.config.json       # Configuration file (download from web)
├── cacert.pem              # SSL certificate bundle
├── README.md               # This file
└── docs/                   # Documentation
    └── configuration.md    # Configuration guide
```

## Technologies Used

- **Python 3.7+**: Core scripting and automation
- **Windows Registry API**: System registry manipulation
- **Windows Networking**: MAC address spoofing and network management
- **Requests Library**: HTTP client for Roblox downloads
- **TQDM**: Progress bars and user feedback
- **Threading**: Asynchronous operations
- **JSON**: Configuration management
- **ZIP Archive**: Roblox package extraction

## System Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.7 or higher
- **Permissions**: Administrator (recommended)
- **Network**: Internet connection for Roblox downloads
- **Disk Space**: 500MB+ for Roblox client

## Safety & Privacy

- **Local Operation**: All data processing happens locally
- **No Telemetry**: No usage data is collected or transmitted
- **Open Source**: Full code transparency and auditability
- **Configurable**: Granular control over all operations
- **Logging**: Detailed operation logs for troubleshooting

## Security Features

- **Certificate Validation**: SSL certificate management for secure downloads
- **Process Validation**: Safe process termination with verification
- **Registry Backup**: Optional registry backup before cleanup
- **Error Handling**: Comprehensive error tracking and recovery
- **Logging**: Detailed operation logging with timestamps

## Performance Metrics

Typical operation times on modern systems:
- **Quick Clean**: 30-60 seconds
- **Full Clean**: 2-5 minutes
- **Roblox Download**: 1-3 minutes (depends on connection)
- **MAC Spoofing**: 10-30 seconds
- **Registry Cleanup**: 15-45 seconds

## Troubleshooting

### Common Issues

1. **Permission Denied**: Run as administrator
2. **Config File Missing**: Download from configuration page
3. **Network Errors**: Check internet connection and firewall
4. **Process Stuck**: Use force deletion in advanced settings

### Log Analysis

Logs are stored at `%temp%\slate\slate.log`:
- Operation timestamps
- Error details and stack traces
- File operation results
- Network adapter changes

### Support

For support and issues:
- **Discord**: midinterlude
- **GitHub Issues**: [Create new issue](https://github.com/midinterlude/Slate/issues)
- **Documentation**: (soon)

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to add features:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comprehensive error handling
- Include logging for new operations
- Update documentation for new features
- Test with various Windows versions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **centerepic**: Original ByeBanAsync implementation
- **WEAO**: Roblox version API service
- **Python Community**: Libraries and tools that make this possible
- **Beta Testers**: Feedback and testing contributions
