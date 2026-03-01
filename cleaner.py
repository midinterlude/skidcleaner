import threading
import sys
import subprocess
import os
import shutil
import glob
import urllib.request
import json
import stat
import uuid


def load_config():
    """Load configuration from JSON file or create defaults."""
    config_path = os.path.join(os.path.dirname(__file__), 'cleaner_config.json')
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except:
        pass
    
    # Return default config if file doesn't exist or is invalid
    return {
        "general": {
            "log_enabled": True,
            "open_log_on_exit": False,
            "capture_console_history": True,
            "clear_screen_on_sections": True
        },
        "cleaning": {
            "kill_processes": True,
            "clean_folders": True,
            "remove_cookies": True,
            "flush_dns": True,
            "restart_explorer": False,
            "clean_registry": True,
            "clean_prefetch": True
        },
        "roblox": {
            "download_roblox": True,
            "launch_roblox_on_exit": False,
            "create_appsettings": True
        },
        "tools": {
            "run_byebanasync": True
        },
        "paths": {
            "temp_folders": ["%temp%", "%temp%/*", "%localappdata%\\Temp"],
            "roblox_folders": ["%localappdata%\\Roblox", "%appdata%\\Roblox", "%appdata%\\Local\\Roblox"]
        },
        "processes": {
            "roblox_processes": ["RobloxPlayerBeta.exe", "RobloxPlayerInstaller.exe"]
        },
        "registry": {
            "registry_paths": ["HKCU\\Software\\Roblox", "HKLM\\SOFTWARE\\Roblox Corporation"]
        },
        "advanced": {
            "show_command_output": True,
            "force_file_deletion": True,
            "skip_confirmation_prompts": True,
            "auto_restart_after_cleaning": True
        }
    }

def save_config(config):
    """Save configuration to JSON file."""
    config_path = os.path.join(os.path.dirname(__file__), 'cleaner_config.json')
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except:
        return False

def edit_config_interactive(config):
    """Interactive configuration editor."""
    print("\n" + "="*60)
    print("ADVANCED CONFIGURATION EDITOR")
    print("="*60)
    
    while True:
        print("\nSelect section to edit:")
        sections = list(config.keys())
        for i, section in enumerate(sections, 1):
            print(f"{i}. {section.capitalize()}")
        print(f"{len(sections)+1}. Save and Run")
        print(f"{len(sections)+2}. Save and Exit (without running)")
        print(f"{len(sections)+3}. Exit without Saving")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == str(len(sections)+1):
            if save_config(config):
                print("✅ Configuration saved successfully!")
                print("🚀 Starting cleaning with new settings...")
                return True  # Return True to indicate we should run
            else:
                print("❌ Failed to save configuration")
                return False
        elif choice == str(len(sections)+2):
            if save_config(config):
                print("✅ Configuration saved successfully!")
            else:
                print("❌ Failed to save configuration")
            return False  # Return False to indicate we should not run
        elif choice == str(len(sections)+3):
            return None  # Return None to indicate cancel
        elif choice.isdigit() and 1 <= int(choice) <= len(sections):
            edit_section(config, sections[int(choice)-1])
        else:
            print("❌ Invalid choice")

def edit_section(config, section_name):
    """Edit a specific configuration section."""
    section = config[section_name]
    print(f"\n--- Editing {section_name.upper()} ---")
    
    for key, value in section.items():
        if isinstance(value, bool):
            current = "y" if value else "n"
            new_val = input(f"{key} (y/n, current: {current}): ").strip().lower()
            if new_val in ['y', 'n']:
                section[key] = new_val == 'y'
        elif isinstance(value, list):
            print(f"\nCurrent {key}:")
            for i, item in enumerate(value, 1):
                print(f"  {i}. {item}")
            print("Options: add, remove, done")
            while True:
                action = input(f"Action for {key}: ").strip().lower()
                if action == 'done':
                    break
                elif action == 'add':
                    new_item = input("Add item: ").strip()
                    if new_item:
                        section[key].append(new_item)
                        print(f"✅ Added: {new_item}")
                elif action == 'remove':
                    try:
                        index = int(input("Remove item number: ")) - 1
                        if 0 <= index < len(section[key]):
                            removed = section[key].pop(index)
                            print(f"✅ Removed: {removed}")
                    except:
                        print("❌ Invalid item number")
                else:
                    print("❌ Invalid action")
        else:
            new_val = input(f"{key} (current: {value}): ").strip()
            if new_val:
                try:
                    if isinstance(value, int):
                        section[key] = int(new_val)
                    else:
                        section[key] = new_val
                except:
                    print("❌ Invalid value type")
    
    config[section_name] = section

def ensure_dependencies():
    """Install any third‑party packages the script requires.

    This function is called at startup and uses pip to install missing
    packages before the rest of the script imports them.
    """
    missing = []
    for pkg in ("pyuac", "requests"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])


ensure_dependencies()

import pyuac


LP = os.path.expandvars(r"%temp%\Roblox_Cleaner_Log.txt")

LOG = True
OPEN_LOG = True

def capture_console_history():
    """Capture existing console content and add it to the log."""
    try:
        # Try to get console buffer content (Windows specific)
        import ctypes
        from ctypes import wintypes
        
        # Define the console screen buffer info structure
        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
        
        class SMALL_RECT(ctypes.Structure):
            _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short),
                       ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)]
        
        class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
            _fields_ = [("dwSize", COORD), ("dwCursorPosition", COORD),
                       ("wAttributes", ctypes.c_ushort), ("srWindow", SMALL_RECT),
                       ("dwMaximumWindowSize", COORD)]
        
        # Windows console API to get screen buffer
        kernel32 = ctypes.windll.kernel32
        h_std_out = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        
        # Get console screen buffer info
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        kernel32.GetConsoleScreenBufferInfo(h_std_out, ctypes.byref(csbi))
        
        # Calculate buffer size
        buffer_size = csbi.dwSize.X * csbi.dwSize.Y
        
        # Create buffer to read console content
        buffer = (ctypes.c_char * buffer_size)()
        chars_read = wintypes.DWORD()
        
        # Read entire console buffer
        read_coord = COORD(0, 0)
        kernel32.ReadConsoleOutputCharacterA(
            h_std_out, buffer, buffer_size, read_coord, ctypes.byref(chars_read)
        )
        
        # Convert to string and clean up
        console_content = buffer.value.decode('utf-8', errors='ignore')
        
        # Split into lines and remove empty ones
        lines = [line.rstrip() for line in console_content.split('\n') if line.strip()]
        
        if lines:
            log("=== PREVIOUS CONSOLE CONTENT ===")
            for line in lines:
                log(line)
            log("=== END PREVIOUS CONSOLE CONTENT ===\n")
            
    except Exception as e:
        # Fallback: try a simpler approach or just note that we couldn't capture
        log(f"=== Could not capture previous console content: {e} ===\n")

def log(message):
    """Print to console and optionally append to the log file."""
    print(message)
    if LOG:
        try:
            with open(LP, 'a', encoding='utf-8') as f:
                f.write(message + "\n")
                f.flush()  # Force write to disk immediately
        except Exception as e:
            print(f"Log write error: {e}")

PF = os.path.expandvars(r"C:\Windows\Prefetch\ROBLOX*.pf")
REGS = [r"HKCU\Software\Roblox", r"HKLM\SOFTWARE\Roblox Corporation"]
CK = os.path.expandvars(r"%appdata%\local\Roblox\Localstorage\RobloxCookies.dat")
PROCS = ['RobloxPlayerBeta.exe', 'RobloxPlayerInstaller.exe']
PATHS = [r"%temp%", r"%temp%/*", r"%localappdata%\Temp", r"%localappdata%\Roblox", r"%appdata%\Roblox", r"%appdata%\Local\Roblox"]
BAPI = "https://api.github.com/repos/centerepic/ByeBanAsync/releases/latest"

def cleanfolders():
    """Remove files and directories matching the PATHS patterns."""
    for pattern in PATHS:
        expanded = os.path.expandvars(pattern)
        
        # First try glob pattern matching
        matches = glob.glob(expanded)
        
        # If no matches and pattern looks like a directory path, check if it exists directly
        if not matches and not '*' in pattern and not '?' in pattern:
            if os.path.exists(expanded):
                matches = [expanded]
        
        if not matches:
            log(f"  - No matches for pattern: {pattern}")
            continue
            
        for path in matches:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"  ✅ Removed file: {path}")
                elif os.path.isdir(path):
                    # Try multiple approaches to delete directory
                    try:
                        shutil.rmtree(path)
                        log(f"  ✅ Removed directory: {path}")
                    except PermissionError:
                        # Try to remove read-only attribute and delete again
                        try:
                            for root, dirs, files in os.walk(path):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    try:
                                        os.chmod(file_path, stat.S_IWRITE)
                                        os.remove(file_path)
                                    except:
                                        pass
                                for dir in dirs:
                                    dir_path = os.path.join(root, dir)
                                    try:
                                        os.chmod(dir_path, stat.S_IWRITE)
                                    except:
                                        pass
                            shutil.rmtree(path, ignore_errors=True)
                            log(f"  ✅ Force removed directory: {path}")
                        except Exception as e2:
                            log(f"  ❌ Failed to remove directory {path} even with force: {e2}")
                            # Last resort: try to delete contents individually
                            try:
                                for item in os.listdir(path):
                                    item_path = os.path.join(path, item)
                                    try:
                                        if os.path.isfile(item_path):
                                            os.remove(item_path)
                                        elif os.path.isdir(item_path):
                                            shutil.rmtree(item_path, ignore_errors=True)
                                    except:
                                        pass
                                os.rmdir(path)
                                log(f"  ✅ Manually cleaned directory: {path}")
                            except Exception as e3:
                                log(f"  ❌ All attempts failed for {path}: {e3}")
            except Exception as e:
                log(f"  ❌ Error cleaning {path}: {e}")

def removecookies():
    if os.path.exists(CK):
        try:
            os.remove(CK)
            shutil.rmtree(os.path.dirname(CK), ignore_errors=True)
            log(f"  ✅ Roblox cookies removed: {CK}")
        except Exception as e:
            log(f"  ❌ Error removing Roblox cookies: {e}")
    else:
        log(f"  - Cookie file not found: {CK}")

BANNER = r"""
      _    _     _      _                            
     | |  (_)   | |    | |                           
  ___| | ___  __| | ___| | ___  __ _ _ __   ___ _ __ 
 / __| |/ / |/ _` |/ __| |/ _ \/ _` | '_ \ / _ \ '__|
 \__ \   <| | (_| | (__| |  __/ (_| | | | |  __/ |_  
 |___/_|\_\_|\__,_|\___|_|\___|\__,_|_| |_|\___|_(_) 
 by: midinterlude.
                                                     
logs can be found in %temp%/robloxcleaner.log"""

def title():
    # Capture current console content before clearing
    capture_console_history()
    
    os.system('cls')
    print(BANNER)

def get_roblox_client_settings():
    """Fetch Roblox client settings from WEAO API and construct download URL"""
    try:
        # Import requests after ensuring it's installed
        import requests
        import urllib3
        
        # Disable SSL warnings since we're intentionally disabling verification for setup.roblox.com
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Get current version from WEAO API
        version_url = "https://weao.xyz/api/versions/current"
        headers = {'User-Agent': 'WEAO-3PService/1.0'}
        
        log(f"Fetching version info from: {version_url}")
        response = requests.get(version_url, headers=headers)
        response.raise_for_status()
        version_data = response.json()
        
        log("WEAO Version Response:")
        log(json.dumps(version_data, indent=2))
        
        # Extract version hash
        version_hash = version_data.get("Windows", "")
        if not version_hash:
            raise Exception("No Windows version found in WEAO response")
        
        log(f"Found Windows version: {version_hash}")
        
        # Try to access the deployment packages directly
        # Based on the RDD source code, we need to download multiple packages
        base_hash = version_hash.replace('version-', '')
        
        # RDD-style extraction mapping for WindowsPlayer
        extract_roots = {
            "RobloxApp.zip": "",
            "shaders.zip": "shaders/",
            "ssl.zip": "ssl/",
            "WebView2.zip": "",
            "WebView2RuntimeInstaller.zip": "WebView2RuntimeInstaller/",
            "content-avatar.zip": "content/avatar/",
            "content-configs.zip": "content/configs/",
            "content-fonts.zip": "content/fonts/",
            "content-sky.zip": "content/sky/",
            "content-sounds.zip": "content/sounds/",
            "content-textures2.zip": "content/textures/",
            "content-models.zip": "content/models/",
            "content-platform-fonts.zip": "PlatformContent/pc/fonts/",
            "content-platform-dictionaries.zip": "PlatformContent/pc/shared_compression_dictionaries/",
            "content-terrain.zip": "PlatformContent/pc/terrain/",
            "content-textures3.zip": "PlatformContent/pc/textures/",
            "extracontent-luapackages.zip": "ExtraContent/LuaPackages/",
            "extracontent-translations.zip": "ExtraContent/translations/",
            "extracontent-models.zip": "ExtraContent/models/",
            "extracontent-textures.zip": "ExtraContent/textures/",
            "extracontent-places.zip": "ExtraContent/places/"
        }
        
        log(f"Downloading {len(extract_roots)} required packages...")
        
        # Create target directory once
        target_dir = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\\" + version_hash)
        os.makedirs(target_dir, exist_ok=True)
        
        # Ensure temp directory exists and is clean
        temp_dir = os.path.expandvars(r"%temp%\skidcleaner")
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
        os.makedirs(temp_dir, exist_ok=True)
        
        success_count = 0
        for package in extract_roots.keys():
            package_url = f"https://setup.roblox.com/version-{base_hash}-{package}"
            log(f"Downloading {package}...")
            
            try:
                # Download the package
                headers = {'User-Agent': 'WEAO-3PService/1.0'}
                response = requests.get(package_url, stream=True, headers=headers, verify=False)
                response.raise_for_status()
                
                # Use unique filename with timestamp to avoid conflicts
                unique_id = str(uuid.uuid4())[:8]
                temp_file = os.path.join(temp_dir, f"{unique_id}_{package}")
                
                # Save to temp file first
                with open(temp_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Extract the package using RDD format
                import zipfile
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    # Get the extraction root for this package
                    extract_root = extract_roots[package]
                    
                    for member in zip_ref.namelist():
                        if member.endswith('/') or member.endswith('\\'):
                            # Skip directories
                            continue
                        
                        # Convert Windows paths to Unix paths and get the relative path
                        clean_member = member.replace('\\', '/')
                        
                        # Extract to the correct subdirectory based on RDD format
                        if extract_root:
                            target_path = os.path.join(target_dir, extract_root + clean_member)
                        else:
                            target_path = os.path.join(target_dir, clean_member)
                        
                        # Create parent directories if needed
                        parent_dir = os.path.dirname(target_path)
                        if parent_dir:
                            os.makedirs(parent_dir, exist_ok=True)
                        
                        # Extract the file
                        with zip_ref.open(member) as source:
                            with open(target_path, 'wb') as target_file:
                                target_file.write(source.read())
                
                # Clean up temp file - ensure it's closed and not locked
                try:
                    os.remove(temp_file)
                except:
                    # If immediate deletion fails, try again after a short delay
                    import time
                    time.sleep(0.1)
                    try:
                        os.remove(temp_file)
                    except:
                        pass  # Will be cleaned up when temp dir is removed
                
                log(f"  ✅ {package} downloaded and extracted")
                success_count += 1
                
            except Exception as e:
                log(f"  ❌ Failed to download {package}: {e}")
        
        log(f"✅ Successfully downloaded {success_count}/{len(extract_roots)} packages")
        
        # Create AppSettings.xml file (required by Roblox)
        app_settings_content = """<?xml version="1.0" encoding="UTF-8"?>
<Settings>
    <ContentFolder>content</ContentFolder>
    <BaseUrl>http://www.roblox.com</BaseUrl>
</Settings>"""
        
        app_settings_path = os.path.join(target_dir, "AppSettings.xml")
        try:
            with open(app_settings_path, 'w', encoding='utf-8') as f:
                f.write(app_settings_content)
            log(f"  ✅ Created AppSettings.xml")
        except Exception as e:
            log(f"  ❌ Failed to create AppSettings.xml: {e}")
        
        if success_count < len(extract_roots):
            log(f"⚠️  Some packages failed to download, but {success_count} succeeded")
        
        return f"https://setup.roblox.com/version-{base_hash}"
        
    except Exception as e:
        log(f"Error fetching WEAO client settings: {e}")
        return None

def download_and_extract_rdd(rdd_url, version_hash):
    """Download file from RDD URL and extract to Roblox Versions directory"""
    try:
        log("\nDownloading Roblox client from RDD...")
        
        # Import requests after ensuring it's installed
        import requests
        
        # Create temp directory
        temp_dir = os.path.expandvars(r"%temp%\skidcleaner")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Download the file
        headers = {'User-Agent': 'WEAO-3PService/1.0'}
        # Disable SSL verification for setup.roblox.com due to certificate issues
        verify_ssl = not rdd_url.startswith('https://setup.roblox.com')
        response = requests.get(rdd_url, stream=True, headers=headers, verify=verify_ssl)
        response.raise_for_status()
        
        log(f"  📡 Response status: {response.status_code}")
        log(f"  📋 Content type: {response.headers.get('content-type', 'Unknown')}")
        log(f"  📏 Content length: {response.headers.get('content-length', 'Unknown')}")
        
        # Get filename from URL or use default
        filename = "roblox_client.zip"
        if 'Content-Disposition' in response.headers:
            import re
            cd = response.headers['Content-Disposition']
            fname = re.findall('filename=(.+)', cd)
            if fname:
                filename = fname[0].strip('"')
        
        download_path = os.path.join(temp_dir, filename)
        
        with open(download_path, 'wb') as f:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
        
        # Verify download completed successfully
        if total_size > 0 and downloaded != total_size:
            raise Exception(f"Incomplete download: {downloaded}/{total_size} bytes")
        
        if not os.path.exists(download_path) or os.path.getsize(download_path) == 0:
            raise Exception("Download failed - file is empty or missing")
        
        log(f"  ✅ Downloaded to: {download_path}")
        
        # Debug: Check what we actually downloaded
        file_size = os.path.getsize(download_path)
        log(f"  📄 Downloaded file size: {file_size} bytes")
        
        # Check first few bytes to identify file type
        with open(download_path, 'rb') as f:
            header = f.read(10)
        
        if header.startswith(b'PK'):
            log("  📦 File appears to be a valid ZIP archive")
        elif header.startswith(b'<!DOCTYPE') or header.startswith(b'<html'):
            log("  ⚠️  RDD service returned HTML - looking for download link...")
            with open(download_path, 'r', errors='ignore') as f:
                content = f.read()
            
            # Look for download link in the HTML
            import re
            download_link = None
            
            # Common patterns for download links
            patterns = [
                r'blob:https://[^"\']+',  # Blob URLs
                r'href=["\']([^"\']*\.zip)["\']',
                r'href=["\']([^"\']*download[^"\']*)["\']',
                r'["\']([^"\']*roblox[^"\']*\.zip)["\']',
                r'location\.href\s*=\s*["\']([^"\']+)["\']',
                r'["\']([^"\']*WEAO-[^"\']*\.zip)["\']',  # WEAO specific pattern
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    download_link = matches[0]
                    log(f"  🔍 Found potential download link: {download_link}")
                    break
            
            if download_link:
                # Handle blob URLs (can't be accessed directly)
                if download_link.startswith('blob:'):
                    log("  ⚠️  Found blob URL - these are temporary and can't be accessed programmatically")
                    log("  🔄 Trying alternative approach...")
                    
                    # Try to construct a direct download URL based on the pattern
                    expected_filename = f"WEAO-LIVE-WindowsPlayer-{version_hash}.zip"
                    direct_url = f"https://rdd.weao.gg/download/{expected_filename}"
                    
                    log(f"  📥 Attempting direct download: {direct_url}")
                    
                    try:
                        file_response = requests.get(direct_url, stream=True)
                        file_response.raise_for_status()
                        
                        log(f"  📋 File response content-type: {file_response.headers.get('content-type', 'Unknown')}")
                        
                        # Save the actual file
                        with open(download_path, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        
                        log(f"  ✅ Downloaded actual file to: {download_path}")
                    except Exception as e:
                        log(f"  ❌ Direct download failed: {e}")
                        raise Exception("Blob URLs cannot be accessed programmatically and direct download failed")
                else:
                    # Make the link absolute if it's relative
                    if download_link.startswith('/'):
                        download_link = f"https://rdd.weao.gg{download_link}"
                    elif not download_link.startswith('http'):
                        download_link = f"https://rdd.weao.gg/{download_link}"
                    
                    log(f"  📥 Attempting to download from: {download_link}")
                    
                    # Download the actual file
                    file_response = requests.get(download_link, stream=True)
                    file_response.raise_for_status()
                    
                    log(f"  📋 File response content-type: {file_response.headers.get('content-type', 'Unknown')}")
                    
                    # Save the actual file
                    with open(download_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    log(f"  ✅ Downloaded actual file to: {download_path}")
            else:
                log("  ❌ No download link found in HTML response")
                log(f"  📄 HTML content preview: {content[:500]}...")
                raise Exception("RDD service returned HTML page instead of file, and no download link found")
        else:
            log(f"  ❓ Unknown file type. Header: {header}")
        
        # Create target directory and extract the file
        target_dir = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\\" + version_hash)
        os.makedirs(target_dir, exist_ok=True)
        
        import zipfile
        try:
            # Test if zip file is valid before extraction
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.testzip()  # This will raise BadZipFile if corrupted
                zip_ref.extractall(target_dir)
        except zipfile.BadZipFile:
            raise Exception("Downloaded file is corrupted or not a valid zip file")
        except Exception as e:
            raise Exception(f"Failed to extract zip file: {e}")
        
        log(f"  ✅ Extracted to: {target_dir}")
        
        # Clean up downloaded file
        try:
            os.remove(download_path)
        except Exception:
            pass
        
    except Exception as e:
        log(f"  ❌ Error downloading/extracting RDD file: {e}")

def byebanasync(wait=True):
    """Python implementation of ByeBanAsync functionality."""
    try:
        log("\n" + "="*41)
        log("ByeBanAsync v2.2 | credits to: centerepic")
        log("="*41)
        log("[!] Ensure you are logged out of the banned account before running this program!")
        
        # Get user profile and cookie path
        user_profile = os.environ.get('USERPROFILE')
        if not user_profile:
            log("[!!!] Could not get USERPROFILE environment variable.")
            return
        
        cookie_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "RobloxCookies.dat")
        
        # Delete Roblox cookie file
        if not os.path.exists(cookie_path):
            log(f"[!!!] Roblox cookie file not found at {cookie_path}!")
        else:
            try:
                os.remove(cookie_path)
                log("[√] Roblox cookie file has been deleted!")
            except Exception as e:
                log(f"[!!!] Failed to delete Roblox cookie file! Err: {e}")
        
        # MAC address spoofing
        log("\n--- MAC Address Spoofing ---")
        change_mac = input("[?] Do you want to attempt to change your MAC address? (y/n): ").strip().lower()
        
        if change_mac == 'y':
            adapters = list_network_adapters()
            if not adapters:
                log("[!] No suitable network adapters found to modify.")
            else:
                log("\n[i] Available network adapters:")
                for i, adapter in enumerate(adapters, 1):
                    log(f"  [{i}] {adapter['description']}")
                    log(f"     └─ Connection Name: '{adapter['connection_name']}'")
                
                # Select adapter
                while True:
                    try:
                        choice = int(input("\n[?] Enter the number of the adapter to change: "))
                        if 1 <= choice <= len(adapters):
                            selected_adapter = adapters[choice - 1]
                            break
                        else:
                            log("[!] Invalid selection. Please enter a number from the list.")
                    except ValueError:
                        log("[!] Invalid selection. Please enter a number from the list.")
                
                # Generate random MAC address
                random_mac = generate_random_mac_address()
                log(f"[>] Attempting to set MAC for adapter: '{selected_adapter['description']}' (ID: {selected_adapter['id']})...")
                
                try:
                    change_mac_address(selected_adapter['id'], random_mac)
                    log("[√] Successfully updated registry for MAC address.")
                    log(f"[>] Attempting to restart network adapter '{selected_adapter['connection_name']}' to apply changes...")
                    
                    try:
                        restart_network_adapter(selected_adapter['connection_name'])
                        log(f"[√] Network adapter '{selected_adapter['connection_name']}' restarted. MAC address change should now be active.")
                        log("[i] Verify with 'ipconfig /all' or 'getmac'.")
                    except Exception as e:
                        log(f"[!!!] Error restarting network adapter: {e}. You may need to do this manually or reboot.")
                except Exception as e:
                    log(f"[!!!] Error changing MAC address in registry: {e}")
        else:
            log("[i] Skipping MAC address change.")
        
        log("\n[...] ByeBanAsync completed!")
        
    except Exception as e:
        log(f"[!!!] Error in ByeBanAsync: {e}")

def generate_random_mac_address():
    """Generate a random MAC address starting with 02 for wireless compatibility."""
    import random
    mac_bytes = [0x02] + [random.randint(0, 255) for _ in range(5)]
    return ''.join(f"{byte:02X}" for byte in mac_bytes)

def list_network_adapters():
    """List available network adapters using Windows registry."""
    try:
        import winreg
        adapters = []
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                           r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}") as class_key:
            
            for i in range(10000):  # Reasonable limit
                try:
                    subkey_name = f"{i:04d}"
                    with winreg.OpenKey(class_key, subkey_name) as adapter_key:
                        try:
                            driver_desc = winreg.QueryValueEx(adapter_key, "DriverDesc")[0]
                            net_cfg_instance_id = winreg.QueryValueEx(adapter_key, "NetCfgInstanceID")[0]
                            
                            # Get connection name
                            try:
                                connection_path = f"SYSTEM\\CurrentControlSet\\Control\\Network\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{net_cfg_instance_id}\\Connection"
                                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, connection_path) as conn_key:
                                    connection_name = winreg.QueryValueEx(conn_key, "Name")[0]
                            except:
                                connection_name = driver_desc
                            
                            # Filter out virtual/loopback adapters
                            desc_lower = driver_desc.lower()
                            if not any(keyword in desc_lower for keyword in 
                                      ["virtual", "loopback", "bluetooth", "wan miniport", "tap-windows", "pseudo"]):
                                adapters.append({
                                    'id': subkey_name,
                                    'description': driver_desc,
                                    'connection_name': connection_name
                                })
                        except (FileNotFoundError, OSError):
                            continue
                except FileNotFoundError:
                    break
        
        return adapters
    except ImportError:
        log("[!!!] winreg module not available. Cannot list network adapters.")
        return []
    except Exception as e:
        log(f"[!!!] Error listing network adapters: {e}")
        return []

def change_mac_address(adapter_id, mac_address):
    """Change MAC address in Windows registry."""
    try:
        import winreg
        
        path = f"SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\{adapter_id}"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE) as adapter_key:
            log(f"[>] Setting 'NetworkAddress' to '{mac_address}'")
            winreg.SetValueEx(adapter_key, "NetworkAddress", 0, winreg.REG_SZ, mac_address)
    
    except ImportError:
        raise Exception("winreg module not available")
    except Exception as e:
        raise Exception(f"Registry error: {e}")

def restart_network_adapter(connection_name):
    """Restart network adapter using netsh."""
    import time
    
    log(f"[>] Disabling adapter: '{connection_name}'")
    disable_result = subprocess.run([
        "netsh", "interface", "set", "interface", 
        f"name={connection_name}", "admin=disable"
    ], capture_output=True, text=True)
    
    if disable_result.returncode != 0:
        error_msg = disable_result.stderr.strip()
        raise Exception(f"Failed to disable network adapter. Netsh output: {error_msg}")
    
    time.sleep(2)
    
    log(f"[>] Enabling adapter: '{connection_name}'")
    enable_result = subprocess.run([
        "netsh", "interface", "set", "interface", 
        f"name={connection_name}", "admin=enable"
    ], capture_output=True, text=True)
    
    if enable_result.returncode != 0:
        error_msg = enable_result.stderr.strip()
        raise Exception(f"Failed to enable network adapter. Netsh output: {error_msg}")

def byebanasync_original(wait=True):
    """Original ByeBanAsync function for fallback."""
    try:
        log("\nDownloading ByeBanAsync...")
        temp_dir = os.path.expandvars(r"%temp%\ByeBanAsync")
        
        os.makedirs(temp_dir, exist_ok=True)
        
        url = BAPI
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
        
        download_url = None
        for asset in data.get('assets', []):
            if asset['name'].endswith('.exe'):
                download_url = asset['browser_download_url']
                break
        
        if download_url:
            exe_path = os.path.join(temp_dir, "ByeBanAsync.exe")
            log(f"  ✅ Found executable, downloading...")
            urllib.request.urlretrieve(download_url, exe_path)
            log(f"  ✅ Downloaded to {exe_path}")
            
            log("  ✅ Launching ByeBanAsync...")
            if wait:
                cmd_line = f'start "" /wait "{exe_path}"'
                subprocess.run(cmd_line, shell=True)
            else:
                subprocess.Popen(exe_path)
        else:
            log("  ❌ Could not find executable in latest release")
    except Exception as e:
        log(f"  ❌ Error downloading/running ByeBanAsync: {e}")

def run_command(cmd, capture_output=True, shell=False):
    """Run a command and log it with full output."""
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
    log(f"  🔧 Running command: {cmd_str}")
    
    try:
        if capture_output:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
            
            # Log stdout if there's any output
            if result.stdout and result.stdout.strip():
                log(f"  📤 STDOUT: {result.stdout.strip()}")
            
            # Log stderr if there's any output
            if result.stderr and result.stderr.strip():
                log(f"  📥 STDERR: {result.stderr.strip()}")
        else:
            result = subprocess.run(cmd, shell=shell)
        
        if result.returncode == 0:
            log(f"  ✅ Command completed successfully (exit code: {result.returncode})")
        else:
            log(f"  ⚠️  Command exited with code: {result.returncode}")
        
        return result
    except Exception as e:
        log(f"  ❌ Error running command: {e}")
        return None

def open_log_async():
    """Open log file in a separate thread."""
    try:
        run_command(f'notepad "{LP}"', capture_output=False, shell=True)
    except Exception as e:
        print(f"Error opening log: {e}")

def launch_roblox():
    """Launch Roblox Player after cleaning is complete"""
    try:
        # Find the latest Roblox version directory
        roblox_versions_dir = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions")
        if not os.path.exists(roblox_versions_dir):
            log("  ❌ Roblox Versions directory not found")
            return False
        
        # Get the most recent version directory
        version_dirs = [d for d in os.listdir(roblox_versions_dir) 
                      if os.path.isdir(os.path.join(roblox_versions_dir, d)) 
                      and d.startswith("version-")]
        
        if not version_dirs:
            log("  ❌ No Roblox version directories found")
            return False
        
        # Sort to get the latest version (assuming version names are sortable)
        latest_version = sorted(version_dirs)[-1]
        roblox_exe_path = os.path.join(roblox_versions_dir, latest_version, "RobloxPlayerBeta.exe")
        
        if not os.path.exists(roblox_exe_path):
            log(f"  ❌ RobloxPlayerBeta.exe not found in {latest_version}")
            return False
        
        log(f"  🚀 Launching Roblox from: {roblox_exe_path}")
        subprocess.Popen([roblox_exe_path])
        log("  ✅ Roblox launched successfully!")
        return True
        
    except Exception as e:
        log(f"  ❌ Error launching Roblox: {e}")
        return False

def main():
    # Load configuration
    config = load_config()
    
    # Ask user what mode they want
    print("\n" + "="*53)
    print(BANNER)
    print("="*53)
    print("\n1. Standard Run (recommended)")
    print("2. Advanced Run (edit configuration)")
    print("3. Exit")
    
    mode_choice = input("\nSelect mode (1-3): ").strip()
    
    if mode_choice == "3":
        print("Exiting...")
        return
    elif mode_choice == "2":
        result = edit_config_interactive(config)
        if result is True:
            # User chose to save and run
            print("\nStarting cleaning with new settings...")
        elif result is False:
            # User chose to save and exit without running
            print("\nConfiguration saved. Exiting...")
            return
        elif result is None:
            # User chose to exit without saving
            print("\nExiting without saving...")
            return
        else:
            # Fallback - just run with current settings
            print("\nStarting cleaning with current settings...")
    elif mode_choice == "1":
        print("\nStarting standard cleaning...")
    else:
        print("Invalid choice. Exiting...")
        return
    
    # Clear screen after mode selection to avoid duplicate display
    os.system('cls')
    
    # Update global variables based on config
    global LOG, OPEN_LOG, LP, PROCS, PATHS, REGS
    
    LOG = config["general"]["log_enabled"]
    OPEN_LOG = config["general"]["open_log_on_exit"]
    PROCS = config["processes"]["roblox_processes"]
    PATHS = config["paths"]["temp_folders"] + config["paths"]["roblox_folders"]
    REGS = config["registry"]["registry_paths"]
    
    try:
        open(LP, 'w').close()
    except Exception:
        pass
    
    # Capture existing console content before starting
    if config["general"]["capture_console_history"]:
        capture_console_history()
    
    log(f"Logging to: {LP}")
    log(BANNER)
    log("=== Roblox Cleaner Log ===")
    log("If you experience any errors, please DM 'midinterlude' on Discord.")

    if not config["advanced"]["skip_confirmation_prompts"]:
        proceed = input("\nThis script will clean Roblox-related temporary files and may restart your computer. Continue? (y/n): ")
        if proceed.lower().strip() != 'y':
            print("Aborting.")
            return

    errors = []

    if config["cleaning"]["kill_processes"]:
        log("Cleaning up Roblox processes...")
        for process in PROCS:
            result = run_command(["taskkill","/f","/im", process])
            if result and result.returncode == 0:
                log(f"  ✅ Terminated: {process}")
            else:
                log(f"  - {process} not running or already terminated")
    
    if config["cleaning"]["clean_folders"]:
        log("\nCleaning up Roblox files...")
        cleanfolders()
    
    if config["cleaning"]["remove_cookies"]:
        log("\nRemoving Tainted Roblox Cookies...")
        removecookies()
    
    if config["cleaning"]["flush_dns"]:
        log("\nFlushing DNS cache...")
        result = run_command(["ipconfig","/flushdns"])
        if result and result.returncode == 0:
            log("  ✅ DNS cache flushed")
        else:
            log("  ❌ Error flushing DNS cache")
            errors.append("DNS flush failed")
    
    if config["general"]["clear_screen_on_sections"]:
        title()
    
    if config["cleaning"]["restart_explorer"]:
        log("\nRestarting Explorer...")
        run_command(["taskkill","/f","/im","explorer.exe"])
        log("  ✅ Explorer terminated")
        run_command(["explorer.exe"])
        log("  ✅ Explorer restarted")
        title()
    
    if config["cleaning"]["clean_registry"]:
        log("\nWiping Registry entries...")
        for path in REGS:
            result = run_command(["reg", "delete", path, "/f"])
            if result and result.returncode == 0:
                log(f"  ✅ Deleted registry: {path}")
            else:
                log(f"  - Registry path not found or already deleted: {path}")
        title()
    
    if config["cleaning"]["clean_prefetch"]:
        log("\nRemoving Windows Prefetch files...")
        prefetch_files = glob.glob(PF)
        if prefetch_files:
            for file in prefetch_files:
                try:
                    os.remove(file)
                    log(f"  ✅ Removed prefetch: {os.path.basename(file)}")
                except Exception as e:
                    log(f"  ❌ Error removing prefetch file {file}: {e}")
                    errors.append(f"prefetch {file} deletion failed: {e}")
        else:
            log("  - No Roblox prefetch files found")
        title()
    
    if config["roblox"]["download_roblox"]:
        log("\nFetching Roblox client settings...")
        rdd_url = get_roblox_client_settings()
    
    log("\nCleaning complete!")
    
    if config["tools"]["run_byebanasync"]:
        log("\nLaunching ByeBanAsync in its own window; please wait for it to close...")
        byebanasync(wait=True)
    
    if errors:
        log("\nNote: some operations reported issues:")
        for e in errors:
            log(f"   - {e}")
    
    # Handle exit based on configuration
    if config["advanced"]["auto_restart_after_cleaning"]:
        if OPEN_LOG and LOG:
            log_thread = threading.Thread(target=open_log_async, daemon=True)
            log_thread.start()
        run_command("shutdown /r /t 0", capture_output=False, shell=True)
    else:
        if config["roblox"]["launch_roblox_on_exit"]:
            if not config["advanced"]["skip_confirmation_prompts"]:
                launch_choice = input("\nDo you want to launch Roblox now? (y/n): ")
                if launch_choice.lower().strip() == 'y':
                    title()
                    log("\nLaunching Roblox...")
                    if launch_roblox():
                        log("✅ Roblox is starting up!")
                    else:
                        log("❌ Failed to launch Roblox automatically")
                        log("   You can launch it manually from the Roblox Player shortcut")
            else:
                title()
                log("\nLaunching Roblox...")
                if launch_roblox():
                    log("✅ Roblox is starting up!")
                else:
                    log("❌ Failed to launch Roblox automatically")
        
        log("\nExiting without restarting. (You may want to restart manually to ensure all changes take effect.)")
        print("Thank you for using Roblox Cleaner! If you had any issues, please DM 'midinterlude' on Discord with the log file.")
        
        # Ensure log is written before opening notepad
        if LOG:
            try:
                with open(LP, 'a', encoding='utf-8') as f:
                    f.flush()
            except:
                pass
        
        if not config["advanced"]["skip_confirmation_prompts"]:
            input("Press Enter to exit.")
        
        if OPEN_LOG and LOG:
            log_thread = threading.Thread(target=open_log_async, daemon=True)
            log_thread.start()
        
        # Force exit immediately
        os._exit(0)


if __name__ == '__main__':
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        exit()
    else:
        main()
