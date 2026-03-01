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
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Global status tracking for web GUI
status_updates = []
server_running = False

class StatusHandler(BaseHTTPRequestHandler):
    """HTTP request handler for status updates."""
    
    def do_GET(self):
        global status_updates
        
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Return status updates as JSON
            response = {
                'updates': status_updates[-50:],  # Last 50 updates
                'timestamp': time.time()
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "running"}')
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/config':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                config = json.loads(post_data.decode())
                config_path = os.path.join(os.path.dirname(__file__), 'cleaner_config.json')
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=4)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status": "saved"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass

def start_status_server(port=8765):
    """Start HTTP server for status updates in a separate thread."""
    global server_running
    
    def run_server():
        global server_running
        try:
            server = HTTPServer(('localhost', port), StatusHandler)
            server_running = True
            server.serve_forever()
        except Exception as e:
            print(f"Status server error: {e}")
        finally:
            server_running = False
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    return port

def add_status_update(message, level='info'):
    """Add a status update for web GUI."""
    global status_updates
    status_updates.append({
        'message': message,
        'level': level,
        'timestamp': time.time()
    })
    
    # Keep only last 100 updates to prevent memory issues
    if len(status_updates) > 100:
        status_updates = status_updates[-100:]

def enhanced_log(message):
    """Enhanced log function that also updates web GUI status."""
    # Call original log function
    log(message)
    
    # Add to status updates for web GUI
    add_status_update(message, 'info')

def load_config():
    """Load configuration from JSON file or create defaults."""
    config_path = os.path.join(os.path.dirname(__file__), 'cleaner_config.json')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config file: {e}")
        pass
    # Return default config if file doesn't exist or is invalid
    return get_default_config()

def get_default_config():
    """Get the default configuration."""
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
            "skip_confirmation_prompts": False,
            "auto_restart_after_cleaning": False
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


def ensure_dependencies():
    """Install any third‑party packages the script requires.
    This function is called at startup and uses pip to install missing
    packages before the rest of the script imports them.
    """
    missing = []
    for pkg in ("pyuac", "requests", "tqdm"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
ensure_dependencies()
import pyuac
# Custom exception classes for better error handling
class RobloxCleanerError(Exception):
    """Base exception for skidcleaner operations."""

    def __init__(self, message, operation=None, details=None):
        super().__init__(message)
        self.operation = operation
        self.details = details or {}
class ConfigurationError(RobloxCleanerError):
    """Raised when there's an issue with configuration."""
    pass
class DownloadError(RobloxCleanerError):
    """Raised when download operations fail."""
    pass
class FileOperationError(RobloxCleanerError):
    """Raised when file operations fail."""
    pass
class ProcessError(RobloxCleanerError):
    """Raised when process operations fail."""
    pass
class NetworkError(RobloxCleanerError):
    """Raised when network operations fail."""
    pass
class RegistryError(RobloxCleanerError):
    """Raised when registry operations fail."""
    pass
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
        # Read line by line instead of entire buffer at once
        lines = []
        buffer_width = csbi.dwSize.X
        buffer_height = csbi.dwSize.Y
        for y in range(buffer_height):
            # Read each line separately
            line_buffer = (ctypes.c_char * buffer_width)()
            chars_read = wintypes.DWORD()
            read_coord = COORD(0, y)
            kernel32.ReadConsoleOutputCharacterA(
                h_std_out, line_buffer, buffer_width, read_coord, ctypes.byref(chars_read)
            )
            # Convert to string and clean up
            line_content = line_buffer.value.decode('utf-8', errors='ignore').rstrip()
            # Skip empty lines and progress bar lines
            if line_content.strip():
                # Skip lines that look like progress bars
                if ('|' in line_content and '%' in line_content and 
                    any(char in line_content for char in ['█', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '│'])):
                    continue  # Skip progress bar lines
                # Skip lines that are just progress bar characters
                if any(char in line_content for char in ['█', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '│']) and len(line_content.strip()) < 100:
                    continue  # Skip short lines with only progress bar characters
                lines.append(line_content)
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
    # Check if tqdm is active and handle accordingly
    import sys
    
    # Check if this is a progress bar
    is_progress_bar = any(char in message for char in ['█', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '│'])
    
    if is_progress_bar:
        # Check if this is a 100% complete progress bar
        if '100%' in message:
            print(message, end='\r')  # Print the final progress bar
            print()  # Add newline to move to next line
            return
        else:
            # This is an intermediate progress bar, overwrite the line
            print(message, end='\r')
            return
    elif message.endswith('downloaded and extracted') or message.endswith('packages') or 'Successfully downloaded' in message:
        # This is a completion message, print normally (should already be on new line)
        print(message)
    else:
        # Regular message, print normally
        print(message)
    if LOG:
        try:
            # Clean up the message for log file (remove progress bar artifacts)
            clean_message = message.replace('\r', '')
            # Only filter out actual progress bar patterns, not regular messages with %
            if ('|' in clean_message and '%' in clean_message and 
                any(char in clean_message for char in ['█', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '│'])):
                # This looks like a progress bar line, skip logging it
                return
            with open(LP, 'a', encoding='utf-8') as f:
                f.write(clean_message + "\n")
                f.flush()  # Force write to disk immediately
        except Exception as e:
            print(f"Log write error: {e}")

def validate_config(config):
    """Validate configuration structure and values."""
    try:
        required_sections = ["general", "cleaning", "roblox", "tools", "paths", "processes", "registry", "advanced"]
        # Check all required sections exist
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing configuration section: {section}")
                return False
        # Validate boolean values
        boolean_sections = ["general", "cleaning", "roblox", "tools", "advanced"]
        for section in boolean_sections:
            for key, value in config[section].items():
                if not isinstance(value, bool):
                    print(f"❌ Invalid boolean value in {section}.{key}: {value}")
                    return False
        # Validate list values
        list_sections = ["paths", "processes", "registry"]
        for section in list_sections:
            for key, value in config[section].items():
                if not isinstance(value, list):
                    print(f"❌ Invalid list value in {section}.{key}: {value}")
                    return False
                if not value:  # Empty list
                    print(f"⚠️  Empty list in {section}.{key}")
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation error: {e}")
        return False
PF = os.path.expandvars(r"C:\Windows\Prefetch\ROBLOX*.pf")
REGS = [r"HKCU\Software\Roblox", r"HKLM\SOFTWARE\Roblox Corporation"]
CK = os.path.expandvars(r"%appdata%\local\Roblox\Localstorage\RobloxCookies.dat")
PROCS = ['RobloxPlayerBeta.exe', 'RobloxPlayerInstaller.exe']
PATHS = [r"%temp%", r"%temp%/*", r"%localappdata%\Temp", r"%localappdata%\Roblox", r"%appdata%\Roblox", r"%appdata%\Local\Roblox"]
BAPI = "https://api.github.com/repos/centerepic/ByeBanAsync/releases/latest"

def cleanfolders():
    """Remove files and directories matching the PATHS patterns."""
    from tqdm import tqdm
    import sys
    # First, collect all files and directories to be processed
    all_paths = []
    for pattern in PATHS:
        expanded = os.path.expandvars(pattern)
        # First try glob pattern matching
        matches = glob.glob(expanded)
        # If no matches and pattern looks like a directory path, check if it exists directly
        if not matches and not '*' in pattern and not '?' in pattern:
            if os.path.exists(expanded):
                matches = [expanded]
        if matches:
            all_paths.extend([(path, pattern) for path in matches])
    if not all_paths:
        log("  - No files or directories found to clean")
        return
    log(f"  📁 Found {len(all_paths)} items to clean")
    # Process with progress bar
    success_count = 0
    error_count = 0
    error_details = []
    # Use tqdm with file=sys.stdout to avoid conflicts with logging
    with tqdm(total=len(all_paths), desc="Cleaning files and folders", unit="item", file=sys.stdout, dynamic_ncols=True) as pbar:
        for path, original_pattern in all_paths:
            pbar.set_description(f"Cleaning {os.path.basename(path)}")
            try:
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                        log(f"  ✅ Removed file: {path}")
                        success_count += 1
                    except PermissionError as e:
                        # Try to remove read-only attribute and delete again
                        try:
                            os.chmod(path, stat.S_IWRITE)
                            os.remove(path)
                            log(f"  ✅ Force removed file: {path}")
                            success_count += 1
                        except Exception as e2:
                            error_msg = f"Failed to remove file {path}: {e2}"
                            log(f"  ❌ {error_msg}")
                            error_count += 1
                            error_details.append({"path": path, "error": str(e2), "type": "file"})
                elif os.path.isdir(path):
                    # Try multiple approaches to delete directory
                    try:
                        shutil.rmtree(path)
                        log(f"  ✅ Removed directory: {path}")
                        success_count += 1
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
                            success_count += 1
                        except Exception as e2:
                            error_msg = f"Failed to remove directory {path} even with force: {e2}"
                            log(f"  ❌ {error_msg}")
                            error_count += 1
                            error_details.append({"path": path, "error": str(e2), "type": "directory"})
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
                                success_count += 1
                                error_count -= 1  # Remove from error count since we succeeded
                            except Exception as e3:
                                final_error_msg = f"All attempts failed for {path}: {e3}"
                                log(f"  ❌ {final_error_msg}")
                                # Update the last error with more details
                                if error_details:
                                    error_details[-1]["final_error"] = str(e3)
                                    error_details[-1]["attempts"] = "multiple"
            except Exception as e:
                error_msg = f"Unexpected error cleaning {path}: {e}"
                log(f"  ❌ {error_msg}")
                error_count += 1
                error_details.append({"path": path, "error": str(e), "type": "unknown"})
            finally:
                pbar.update(1)
                # Force a flush to ensure progress bar updates properly
                sys.stdout.flush()
    # Summary
    log(f"  📊 Cleaning summary: {success_count} successful, {error_count} errors")
    if error_count > 0:
        log("  ⚠️  Errors encountered during cleaning:")
        for i, detail in enumerate(error_details[:5], 1):  # Show first 5 errors
            log(f"     {i}. {detail['path']} ({detail['type']}): {detail['error']}")
        if len(error_details) > 5:
            log(f"     ... and {len(error_details) - 5} more errors")
        # Raise exception if too many errors
        if error_count > len(all_paths) * 0.5:  # More than 50% failed
            raise FileOperationError(f"High failure rate during folder cleaning: {error_count}/{len(all_paths)} items failed", 
                                   operation="clean_folders", details={"total_items": len(all_paths), "errors": error_details})

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
 logs can be found in %temp%/skidcleaner.log"""

def title():
    """Clear screen and display title."""
    # Don't capture console history here since it's done in main
    os.system('cls')
    print(BANNER)

def clear_screen():
    """Clear screen without showing banner."""
    os.system('cls')

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
        # Import tqdm for progress bars
        from tqdm import tqdm
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
        failed_packages = []
        # Create progress bar for package downloads
        import sys
        with tqdm(total=len(extract_roots), desc="Downloading Roblox packages", unit="pkg", file=sys.stdout, dynamic_ncols=True) as pbar:
            for package in extract_roots.keys():
                package_url = f"https://setup.roblox.com/version-{base_hash}-{package}"
                pbar.set_description(f"Downloading {package}")
                try:
                    # Download the package
                    headers = {'User-Agent': 'WEAO-3PService/1.0'}
                    response = requests.get(package_url, stream=True, headers=headers, verify=False)
                    response.raise_for_status()
                    # Use unique filename with timestamp to avoid conflicts
                    unique_id = str(uuid.uuid4())[:8]
                    temp_file = os.path.join(temp_dir, f"{unique_id}_{package}")
                    # Get total file size for progress tracking
                    total_size = int(response.headers.get('content-length', 0))
                    # Save to temp file first with progress bar
                    with open(temp_file, 'wb') as f:
                        with tqdm(total=total_size, desc=f"  {package}", unit='B', unit_scale=True, leave=False, file=sys.stdout, dynamic_ncols=True) as file_pbar:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    file_pbar.update(len(chunk))
                    # Extract the package using RDD format
                    import zipfile
                    try:
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
                        log(f"  ✅ {package} downloaded and extracted")
                        success_count += 1
                    except zipfile.BadZipFile as e:
                        raise DownloadError(f"Downloaded package {package} is corrupted or not a valid zip file", 
                                         operation="extract_package", details={"package": package, "error": str(e)})
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
                except requests.RequestException as e:
                    error_msg = f"Failed to download {package}: {e}"
                    log(f"  ❌ {error_msg}")
                    failed_packages.append(package)
                    raise DownloadError(error_msg, operation="download_package", details={"package": package, "url": package_url})
                except Exception as e:
                    error_msg = f"Unexpected error downloading {package}: {e}"
                    log(f"  ❌ {error_msg}")
                    failed_packages.append(package)
                    raise DownloadError(error_msg, operation="download_package", details={"package": package, "error": str(e)})
                finally:
                    pbar.update(1)
                    title()  # Clear screen between package downloads
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
            if failed_packages:
                log(f"⚠️  Some packages failed to download: {', '.join(failed_packages)}")
            else:
                log(f"⚠️  Some packages failed to download, but {success_count} succeeded")
        if success_count == 0:
            raise DownloadError("No packages were successfully downloaded", operation="download_all_packages", 
                              details={"total_packages": len(extract_roots), "failed_packages": failed_packages})
        return f"https://setup.roblox.com/version-{base_hash}"
    except DownloadError:
        # Re-raise DownloadError as-is
        raise
    except requests.RequestException as e:
        raise DownloadError(f"Network error while fetching Roblox client settings: {e}", 
                          operation="fetch_version_info", details={"url": version_url})
    except Exception as e:
        raise DownloadError(f"Unexpected error in get_roblox_client_settings: {e}", 
                          operation="get_roblox_client_settings", details={"error": str(e)})

def download_and_extract_rdd(rdd_url, version_hash):
    """Download file from RDD URL and extract to Roblox Versions directory"""
    from tqdm import tqdm
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
        try:
            response = requests.get(rdd_url, stream=True, headers=headers, verify=verify_ssl)
            response.raise_for_status()
        except requests.RequestException as e:
            raise DownloadError(f"Failed to initiate download from {rdd_url}: {e}", 
                              operation="download_initiate", details={"url": rdd_url, "ssl_verify": verify_ssl})
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
        # Get total size for progress tracking
        total_size = int(response.headers.get('content-length', 0))
        # Download with progress bar
        with open(download_path, 'wb') as f:
            with tqdm(total=total_size, desc="Downloading Roblox client", unit='B', unit_scale=True, file=sys.stdout, dynamic_ncols=True) as pbar:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        pbar.update(len(chunk))
        # Verify download completed successfully
        if total_size > 0 and downloaded != total_size:
            raise DownloadError(f"Incomplete download: {downloaded}/{total_size} bytes", 
                              operation="download_verify", details={"expected": total_size, "actual": downloaded})
        if not os.path.exists(download_path) or os.path.getsize(download_path) == 0:
            raise DownloadError("Download failed - file is empty or missing", 
                              operation="download_verify", details={"path": download_path})
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
                        # Save the actual file with progress bar
                        file_total_size = int(file_response.headers.get('content-length', 0))
                        with open(download_path, 'wb') as f:
                            with tqdm(total=file_total_size, desc="  Downloading actual file", unit='B', unit_scale=True, leave=False, file=sys.stdout, dynamic_ncols=True) as file_pbar:
                                for chunk in file_response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                                        file_pbar.update(len(chunk))
                        log(f"  ✅ Downloaded actual file to: {download_path}")
                    except requests.RequestException as e:
                        raise DownloadError(f"Direct download failed: {e}", 
                                          operation="direct_download", details={"url": direct_url})
                else:
                    # Make the link absolute if it's relative
                    if download_link.startswith('/'):
                        download_link = f"https://rdd.weao.gg{download_link}"
                    elif not download_link.startswith('http'):
                        download_link = f"https://rdd.weao.gg/{download_link}"
                    log(f"  📥 Attempting to download from: {download_link}")
                    # Download the actual file
                    try:
                        file_response = requests.get(download_link, stream=True)
                        file_response.raise_for_status()
                        log(f"  📋 File response content-type: {file_response.headers.get('content-type', 'Unknown')}")
                        # Save the actual file with progress bar
                        file_total_size = int(file_response.headers.get('content-length', 0))
                        with open(download_path, 'wb') as f:
                            with tqdm(total=file_total_size, desc="  Downloading actual file", unit='B', unit_scale=True, leave=False, file=sys.stdout, dynamic_ncols=True) as file_pbar:
                                for chunk in file_response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                                        file_pbar.update(len(chunk))
                        log(f"  ✅ Downloaded actual file to: {download_path}")
                    except requests.RequestException as e:
                        raise DownloadError(f"Failed to download from found link: {e}", 
                                          operation="link_download", details={"url": download_link})
            else:
                log("  ❌ No download link found in HTML response")
                log(f"  📄 HTML content preview: {content[:500]}...")
                raise DownloadError("RDD service returned HTML page instead of file, and no download link found", 
                                  operation="parse_html", details={"content_preview": content[:500]})
        else:
            log(f"  ❓ Unknown file type. Header: {header}")
            raise DownloadError(f"Unknown file type downloaded: {header}", 
                              operation="file_type_check", details={"header": header.hex()})
        # Create target directory and extract the file
        target_dir = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions\\" + version_hash)
        os.makedirs(target_dir, exist_ok=True)
        import zipfile
        try:
            # Test if zip file is valid before extraction
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.testzip()  # This will raise BadZipFile if corrupted
                # Count files for progress tracking
                file_count = len(zip_ref.namelist())
                log(f"  📦 Extracting {file_count} files...")
                # Extract with progress bar
                with tqdm(total=file_count, desc="Extracting files", unit="file", file=sys.stdout, dynamic_ncols=True) as extract_pbar:
                    for member in zip_ref.namelist():
                        if not member.endswith('/') and not member.endswith('\\'):  # Skip directories
                            zip_ref.extract(member, target_dir)
                        extract_pbar.update(1)
        except zipfile.BadZipFile as e:
            raise DownloadError(f"Downloaded file is corrupted or not a valid zip file: {e}", 
                              operation="extract_zip", details={"path": download_path})
        except Exception as e:
            raise DownloadError(f"Failed to extract zip file: {e}", 
                              operation="extract_zip", details={"path": download_path, "error": str(e)})
        log(f"  ✅ Extracted to: {target_dir}")
        # Clean up downloaded file
        try:
            os.remove(download_path)
        except Exception:
            pass
    except DownloadError:
        # Re-raise DownloadError as-is
        raise
    except Exception as e:
        raise DownloadError(f"Unexpected error in download_and_extract_rdd: {e}", 
                          operation="download_and_extract_rdd", details={"url": rdd_url, "error": str(e)})

def byebanasync(wait=True):
    """Python implementation of ByeBanAsync functionality."""
    try:
        log("\n" + "="*41)
        log("ByeBanAsync v2.2 | credits to: centerepic")
        log("="*41)
        # Get user profile and cookie path
        user_profile = os.environ.get('USERPROFILE')
        if not user_profile:
            log("[!!!] Could not get USERPROFILE environment variable.")
            return
        cookie_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "RobloxCookies.dat")
        # Delete Roblox cookie file
        if not os.path.exists(cookie_path):
            # Cookie file doesn't exist, that's fine
            pass
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
    """Main execution function - optimized for web GUI configuration."""
    # Start status server for web GUI integration
    try:
        status_port = start_status_server()
    except Exception as e:
        print(f"Could not start status server: {e}")
        status_port = None
    
    # Load configuration
    config = load_config()
    
    # Validate configuration
    if not validate_config(config):
        print("Invalid configuration. Using default settings.")
        config = get_default_config()
    
    # Display banner
    print("\n" + "="*53)
    print(BANNER)
    print("="*53)
    
    # Update global variables based on config
    global LOG, OPEN_LOG, LP, PROCS, PATHS, REGS
    LOG = config["general"]["log_enabled"]
    OPEN_LOG = config["general"]["open_log_on_exit"]
    PROCS = config["processes"]["roblox_processes"]
    PATHS = config["paths"]["temp_folders"] + config["paths"]["roblox_folders"]
    REGS = config["registry"]["registry_paths"]
    
    # Initialize logging (quiet startup)
    if LOG:
        try:
            with open(LP, 'w') as f:
                f.write("=== skidcleaner Log ===\n")
                f.write("If you experience any errors, please DM 'midinterlude' on Discord.\n")
                f.write(f"Configuration loaded from cleaner_config.json\n")
                f.write(f"Profile: {config.get('profile', 'custom')}\n")
        except Exception:
            pass
    
    # Get user confirmation with info option
    while True:
        proceed = input("\nThis script will clean every file linked to roblox and may restart your computer.\nFor additional information type \"info\". (y/n/info): ").strip().lower()
        if proceed == 'info':
            print("\n" + "="*60)
            print("ROBLOX CLEANER - CONFIGURATION SUMMARY")
            print("="*60)
            print(f"Web GUI integration: {f'http://localhost:{status_port}' if status_port else 'Not available'}")
            print(f"Configuration file: cleaner_config.json")
            print(f"Profile: {config.get('profile', 'custom')}")
            print(f"Log file: {LP}")
            print("\nCleaning Operations:")
            print(f"  • Process Termination: {'Enabled' if config.get('cleaning', {}).get('kill_processes', False) else 'Disabled'}")
            print(f"  • Folder Cleaning: {'Enabled' if config.get('cleaning', {}).get('clean_folders', False) else 'Disabled'}")
            print(f"  • Cookie Removal: {'Enabled' if config.get('cleaning', {}).get('remove_cookies', False) else 'Disabled'}")
            print(f"  • DNS Cache Flush: {'Enabled' if config.get('cleaning', {}).get('flush_dns', False) else 'Disabled'}")
            print(f"  • Registry Cleanup: {'Enabled' if config.get('cleaning', {}).get('clean_registry', False) else 'Disabled'}")
            print(f"  • Prefetch Cleanup: {'Enabled' if config.get('cleaning', {}).get('clean_prefetch', False) else 'Disabled'}")
            print(f"  • Explorer Restart: {'Enabled' if config.get('cleaning', {}).get('restart_explorer', False) else 'Disabled'}")
            print(f"\nRoblox Operations:")
            print(f"  • Download Roblox: {'Enabled' if config.get('roblox', {}).get('download_roblox', False) else 'Disabled'}")
            print(f"  • Launch Roblox: {'Enabled' if config.get('roblox', {}).get('launch_roblox_on_exit', False) else 'Disabled'}")
            print(f"  • Create AppSettings: {'Enabled' if config.get('roblox', {}).get('create_appsettings', False) else 'Disabled'}")
            print(f"\nAdvanced Options:")
            print(f"  • Auto Restart: {'Enabled' if config.get('advanced', {}).get('auto_restart_after_cleaning', False) else 'Disabled'}")
            print(f"  • Skip Prompts: {'Enabled' if config.get('advanced', {}).get('skip_confirmation_prompts', False) else 'Disabled'}")
            print(f"  • Force Deletion: {'Enabled' if config.get('advanced', {}).get('force_file_deletion', False) else 'Disabled'}")
            print("="*60)
            continue
        elif proceed in ['y', 'yes']:
            break
        elif proceed in ['n', 'no']:
            print("Aborting.")
            return
        else:
            print("Invalid option. Please enter 'y', 'n', or 'info'.")
            continue
    errors = []
    operation_start_time = {}

    def log_operation_start(operation_name):
        """Log the start of an operation with timestamp."""
        import time
        operation_start_time[operation_name] = time.time()
        log(f"🚀 Starting {operation_name}...")

    def log_operation_end(operation_name, success=True, error_msg=None):
        """Log the end of an operation with duration."""
        import time
        if operation_name in operation_start_time:
            duration = time.time() - operation_start_time[operation_name]
            if success:
                log(f"✅ {operation_name} completed successfully in {duration:.2f}s")
            else:
                log(f"❌ {operation_name} failed after {duration:.2f}s: {error_msg}")
    try:
        if config["cleaning"]["kill_processes"]:
            log_operation_start("Process termination")
            for process in PROCS:
                result = run_command(["taskkill","/f","/im", process])
                if result and result.returncode == 0:
                    log(f"  ✅ Terminated: {process}")
                else:
                    log(f"  - {process} not running or already terminated")
            log_operation_end("Process termination")
        if config["cleaning"]["clean_folders"]:
            log_operation_start("Folder cleaning")
            try:
                cleanfolders()
                log_operation_end("Folder cleaning")
            except FileOperationError as e:
                log_operation_end("Folder cleaning", False, str(e))
                errors.append(f"Folder cleaning failed: {e}")
                log(f"🔍 Detailed error info: {e.details}")
        if config["cleaning"]["remove_cookies"]:
            log_operation_start("Cookie removal")
            try:
                removecookies()
                log_operation_end("Cookie removal")
            except FileOperationError as e:
                log_operation_end("Cookie removal", False, str(e))
                errors.append(f"Cookie removal failed: {e}")
        if config["cleaning"]["flush_dns"]:
            log_operation_start("DNS cache flush")
            result = run_command(["ipconfig","/flushdns"])
            if result and result.returncode == 0:
                log_operation_end("DNS cache flush")
            else:
                log_operation_end("DNS cache flush", False, "Command failed")
                log("  ❌ Error flushing DNS cache")
                errors.append("DNS flush failed")
        if config["general"]["clear_screen_on_sections"]:
            title()
        if config["cleaning"]["restart_explorer"]:
            log_operation_start("Explorer restart")
            try:
                run_command(["taskkill","/f","/im","explorer.exe"])
                log("  ✅ Explorer terminated")
                run_command(["explorer.exe"])
                log("  ✅ Explorer restarted")
                log_operation_end("Explorer restart")
                title()
            except ProcessError as e:
                log_operation_end("Explorer restart", False, str(e))
                errors.append(f"Explorer restart failed: {e}")
        if config["cleaning"]["clean_registry"]:
            log_operation_start("Registry cleanup")
            registry_errors = []
            for path in REGS:
                result = run_command(["reg", "delete", path, "/f"])
                if result and result.returncode == 0:
                    log(f"  ✅ Deleted registry: {path}")
                else:
                    log(f"  - Registry path not found or already deleted: {path}")
                    registry_errors.append(path)
            if registry_errors:
                log_operation_end("Registry cleanup", False, f"Some registry paths not found: {registry_errors}")
            else:
                log_operation_end("Registry cleanup")
            title()
        if config["cleaning"]["clean_prefetch"]:
            log_operation_start("Prefetch cleanup")
            prefetch_files = glob.glob(PF)
            if prefetch_files:
                prefetch_errors = []
                for file in prefetch_files:
                    try:
                        os.remove(file)
                        log(f"  ✅ Removed prefetch: {os.path.basename(file)}")
                    except Exception as e:
                        error_msg = f"Error removing prefetch file {file}: {e}"
                        log(f"  ❌ {error_msg}")
                        prefetch_errors.append({"file": file, "error": str(e)})
                        errors.append(f"prefetch {file} deletion failed: {e}")
                if prefetch_errors:
                    log_operation_end("Prefetch cleanup", False, f"{len(prefetch_errors)} files failed")
                else:
                    log_operation_end("Prefetch cleanup")
            else:
                log("  - No Roblox prefetch files found")
                log_operation_end("Prefetch cleanup")
            title()
        if config["roblox"]["download_roblox"]:
            log_operation_start("Roblox client download")
            try:
                rdd_url = get_roblox_client_settings()
                log_operation_end("Roblox client download")
            except DownloadError as e:
                log_operation_end("Roblox client download", False, str(e))
                errors.append(f"Roblox download failed: {e}")
                log(f"🔍 Detailed download error info: {e.details}")
            except Exception as e:
                log_operation_end("Roblox client download", False, str(e))
                errors.append(f"Roblox download failed with unexpected error: {e}")
        log("\n🎉 Cleaning complete!")
        if config["tools"]["run_byebanasync"]:
            log_operation_start("ByeBanAsync")
            try:
                log("\nLaunching ByeBanAsync in its own window; please wait for it to close...")
                byebanasync(wait=True)
                log_operation_end("ByeBanAsync")
            except (NetworkError, ProcessError) as e:
                log_operation_end("ByeBanAsync", False, str(e))
                errors.append(f"ByeBanAsync failed: {e}")
                log(f"🔍 Detailed ByeBanAsync error info: {e.details}")
        if errors:
            log("\n⚠️  Some operations reported issues:")
            for i, e in enumerate(errors, 1):
                log(f"   {i}. {e}")
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
                        log_operation_start("Roblox launch")
                        if launch_roblox():
                            log_operation_end("Roblox launch")
                            log("✅ Roblox is starting up!")
                        else:
                            log_operation_end("Roblox launch", False, "Launch failed")
                            log("❌ Failed to launch Roblox automatically")
                            log("   You can launch it manually from the Roblox Player shortcut")
                else:
                    title()
                    log_operation_start("Roblox launch")
                    if launch_roblox():
                        log_operation_end("Roblox launch")
                        log("✅ Roblox is starting up!")
                    else:
                        log_operation_end("Roblox launch", False, "Launch failed")
                        log("❌ Failed to launch Roblox automatically")
            log("\nExiting without restarting. (You may want to restart manually to ensure all changes take effect.)")
            print("Thank you for using skidcleaner! If you had any issues, please DM 'midinterlude' on Discord with the log file.")
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
    except KeyboardInterrupt:
        log("\n⚠️  Operation cancelled by user")
        print("\nOperation cancelled by user.")
    except RobloxCleanerError as e:
        log(f"\n❌ skidcleaner error in {e.operation}: {e}")
        log(f"🔍 Error details: {e.details}")
        print(f"\n❌ Error in {e.operation}: {e}")
        if config["general"]["log_enabled"]:
            print(f"📋 Check log file for details: {LP}")
    except Exception as e:
        log(f"\n💥 Unexpected error: {e}")
        import traceback
        log(f"🔍 Full traceback: {traceback.format_exc()}")
        print(f"\n💥 Unexpected error: {e}")
        if config["general"]["log_enabled"]:
            print(f"📋 Check log file for details: {LP}")
if __name__ == '__main__':
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        exit()
    else:
        main()
