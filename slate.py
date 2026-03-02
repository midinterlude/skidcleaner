import threading, sys, subprocess, os , shutil, glob, json, stat, uuid

script_dir = os.path.dirname(os.path.abspath(__file__))
if hasattr(sys, "_MEIPASS"):
    slate_dir = os.path.dirname(script_dir)
else:
    slate_dir = script_dir
cert_path = os.path.join(slate_dir, "cacert.pem")
if os.path.exists(cert_path):
    os.environ["SSL_CERT_FILE"] = cert_path

LP = os.path.expandvars(r"%temp%\slate\slate.log")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "slate.config.json")
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config file: {e}")
        pass
    return get_default_config()

def get_default_config():
    return {
        "general": {
            "log_enabled": True,
            "open_log_on_exit": False,
            "clear_screen_on_sections": True,
        },
        "cleaning": {
            "kill_processes": True,
            "clean_folders": True,
            "remove_cookies": True,
            "flush_dns": True,
            "restart_explorer": False,
            "clean_registry": True,
            "clean_prefetch": True,
        },
        "roblox": {
            "download_roblox": True,
            "launch_roblox_on_exit": False,
            "create_appsettings": True,
        },
        "tools": {"run_byebanasync": True},
        "paths": {
            "temp_folders": ["%temp%", "%temp%/*", "%localappdata%\\Temp"],
            "roblox_folders": [
                "%localappdata%\\Roblox",
                "%appdata%\\Roblox",
                "%appdata%\\Local\\Roblox",
            ],
        },
        "processes": {
            "roblox_processes": ["RobloxPlayerBeta.exe", "RobloxPlayerInstaller.exe"]
        },
        "registry": {
            "registry_paths": [
                "HKCU\\Software\\Roblox",
                "HKLM\\SOFTWARE\\Roblox Corporation",
            ]
        },
        "advanced": {
            "show_command_output": True,
            "force_file_deletion": True,
            "skip_confirmation_prompts": False,
            "auto_restart_after_cleaning": False,
        },
    }


def ensure_dependencies():
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

class SlateError(Exception):

    def __init__(self, message, operation=None, details=None):
        super().__init__(message)
        self.operation = operation
        self.details = details or {}

class ConfigurationError(SlateError):

    pass

class DownloadError(SlateError):

    pass

class FileOperationError(SlateError):


    pass

class ProcessError(SlateError):


    pass

class NetworkError(SlateError):


    pass

class RegistryError(SlateError):


    pass

LP = os.path.expandvars(r"%temp%\slate\slate.log")
LOG = True
OPEN_LOG = True

def log(message):

    import sys

    is_progress_bar = any(
        char in message for char in ["█", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "│"]
    )

    if is_progress_bar:
        if "100%" in message:
            print(message, end="\r")
            print()
            return
        else:
            print(message, end="\r")
            return
    elif (
        message.endswith("downloaded and extracted")
        or message.endswith("packages")
        or "Successfully downloaded" in message
    ):
        print(message)
    else:
        print(message)

    if LOG:
        try:
            clean_message = message.replace("\r", "")
            if (
                "|" in clean_message
                and "%" in clean_message
                and any(
                    char in clean_message
                    for char in ["█", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "│"]
                )
            ):
                return
            log_dir = os.path.dirname(LP)
            os.makedirs(log_dir, exist_ok=True)
            with open(LP, "a", encoding="utf-8") as f:
                f.write(clean_message + "\n")
                f.flush()
        except Exception as e:
            print(f"Log write error: {e}")

def validate_config(config):

    try:
        required_sections = [
            "general",
            "cleaning",
            "roblox",
            "tools",
            "paths",
            "processes",
            "registry",
            "advanced",
        ]
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing configuration section: {section}")
                return False
        boolean_sections = ["general", "cleaning", "roblox", "tools", "advanced"]
        for section in boolean_sections:
            for key, value in config[section].items():
                if not isinstance(value, bool):
                    print(f"❌ Invalid boolean value in {section}.{key}: {value}")
                    return False
        list_sections = ["paths", "processes", "registry"]
        for section in list_sections:
            for key, value in config[section].items():
                if not isinstance(value, list):
                    print(f"❌ Invalid list value in {section}.{key}: {value}")
                    return False
                if not value:
                    print(f"⚠️  Empty list in {section}.{key}")
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation error: {e}")
        return False

PF = os.path.expandvars(r"C:\Windows\Prefetch\ROBLOX*.pf")
REGS = [r"HKCU\Software\Roblox", r"HKLM\SOFTWARE\Roblox Corporation"]
CK = os.path.expandvars(r"%appdata%\local\Roblox\Localstorage\RobloxCookies.dat")
PROCS = ["RobloxPlayerBeta.exe", "RobloxPlayerInstaller.exe"]
PATHS = [
    r"%temp%",
    r"%temp%/*",
    r"%localappdata%\Temp",
    r"%localappdata%\Roblox",
    r"%appdata%\Roblox",
    r"%appdata%\Local\Roblox",
]

def cleanfolders():
    from tqdm import tqdm
    import sys

    all_paths = []
    for pattern in PATHS:
        expanded = os.path.expandvars(pattern)
        matches = glob.glob(expanded)
        if not matches and not "*" in pattern and not "?" in pattern:
            if os.path.exists(expanded):
                matches = [expanded]
        if matches:
            all_paths.extend([(path, pattern) for path in matches])
    if not all_paths:
        log("  - No files or directories found to clean")
        return
    log(f"  📁 Found {len(all_paths)} items to clean")
    success_count = 0
    error_count = 0
    error_details = []
    with tqdm(
        total=len(all_paths),
        desc="Cleaning files and folders",
        unit="item",
        file=sys.stdout,
        dynamic_ncols=True,
    ) as pbar:
        for path, original_pattern in all_paths:
            pbar.set_description(f"Cleaning {os.path.basename(path)}")
            try:
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                        log(f"  ✅ Removed file: {path}")
                        success_count += 1
                    except PermissionError as e:
                        try:
                            os.chmod(path, stat.S_IWRITE)
                            os.remove(path)
                            log(f"  ✅ Force removed file: {path}")
                            success_count += 1
                        except Exception as e2:
                            error_msg = f"Failed to remove file {path}: {e2}"
                            log(f"  ❌ {error_msg}")
                            error_count += 1
                            error_details.append(
                                {"path": path, "error": str(e2), "type": "file"}
                            )
                elif os.path.isdir(path):
                    try:
                        shutil.rmtree(path)
                        log(f"  ✅ Removed directory: {path}")
                        success_count += 1
                    except PermissionError:
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
                            error_details.append(
                                {"path": path, "error": str(e2), "type": "directory"}
                            )
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
                                error_count -= 1
                            except Exception as e3:
                                final_error_msg = (
                                    f"All attempts failed for {path}: {e3}"
                                )
                                log(f"  ❌ {final_error_msg}")
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
                sys.stdout.flush()
    log(f"  📊 Cleaning summary: {success_count} successful, {error_count} errors")
    if error_count > 0:
        log("  ⚠️  Errors encountered during cleaning:")
        for i, detail in enumerate(error_details[:5], 1):
            log(f"     {i}. {detail['path']} ({detail['type']}): {detail['error']}")
        if len(error_details) > 5:
            log(f"     ... and {len(error_details) - 5} more errors")
        if error_count > len(all_paths) * 0.5:
            raise FileOperationError(
                f"High failure rate during folder cleaning: {error_count}/{len(all_paths)} items failed",
                operation="clean_folders",
                details={"total_items": len(all_paths), "errors": error_details},
            )

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
▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
▐     ▄████████  ▄█          ▄████████     ███        ▄████████  ▌
▐    ███    ███ ███         ███    ███ ▀█████████▄   ███    ███  ▌
▐    ███    █▀  ███         ███    ███    ▀███▀▀██   ███    █▀   ▌
▐    ███        ███         ███    ███     ███   ▀  ▄███▄▄▄      ▌
▐  ▀███████████ ███       ▀███████████     ███     ▀▀███▀▀▀      ▌
▐           ███ ███         ███    ███     ███       ███    █▄   ▌
▐     ▄█    ███ ███▌    ▄   ███    ███     ███       ███    ███  ▌
▐   ▄████████▀  █████▄▄██   ███    █▀     ▄████▀     ██████████  ▌
▐               ▀                                                ▌
▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌
 by: midinterlude (logs can be found in %temp%\\slate\\slate.log)
 """

def title():
    os.system("cls")
    print(BANNER)


def get_roblox_client_settings():
    try:
        import requests
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        version_url = "https://weao.xyz/api/versions/current"
        headers = {"User-Agent": "WEAO-3PService/1.0"}
        log(f"Fetching version info from: {version_url}")
        response = requests.get(version_url, headers=headers, verify=False)
        response.raise_for_status()
        version_data = response.json()
        log("WEAO Version Response:")
        log(json.dumps(version_data, indent=2))
        version_hash = version_data.get("Windows", "")
        if not version_hash:
            raise Exception("No Windows version found in WEAO response")
        log(f"Found Windows version: {version_hash}")
        base_hash = version_hash.replace("version-", "")
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
            "extracontent-places.zip": "ExtraContent/places/",
        }
        log(f"Downloading {len(extract_roots)} required packages...")
        from tqdm import tqdm

        target_dir = os.path.expandvars(
            r"%LOCALAPPDATA%\Roblox\Versions\\" + version_hash
        )
        os.makedirs(target_dir, exist_ok=True)
        temp_dir = os.path.expandvars(r"%temp%\slate")
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
        os.makedirs(temp_dir, exist_ok=True)
        success_count = 0
        failed_packages = []
        import sys

        with tqdm(
            total=len(extract_roots),
            desc="Downloading Roblox packages",
            unit="pkg",
            file=sys.stdout,
            dynamic_ncols=True,
        ) as pbar:
            for package_index, package in enumerate(extract_roots.keys()):
                package_url = f"https://setup.roblox.com/version-{base_hash}-{package}"
                pbar.set_description(f"Downloading {package}")
                try:
                    headers = {"User-Agent": "WEAO-3PService/1.0"}
                    response = requests.get(
                        package_url, stream=True, headers=headers, verify=False
                    )
                    response.raise_for_status()
                    unique_id = str(uuid.uuid4())[:8]
                    temp_file = os.path.join(temp_dir, f"{unique_id}_{package}")
                    total_size = int(response.headers.get("content-length", 0))
                    with open(temp_file, "wb") as f:
                        class CustomProgressBar:
                            def __init__(self, total, desc, package_index, total_packages):
                                self.total = total
                                self.desc = desc
                                self.current = 0
                                self.last_update = 0
                                self.package_index = package_index
                                self.total_packages = total_packages
                            
                            def update(self, chunk_size):
                                self.current += chunk_size
                                if self.current - self.last_update > 1024*1024 or self.current >= self.total:
                                    percentage = (self.current / self.total) * 100 if self.total > 0 else 0
                                    overall_percentage = ((self.package_index + (percentage / 100)) / self.total_packages) * 100
                                    
                                    bar_length = 50
                                    filled_length = int(bar_length * percentage / 100)
                                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                                    
                                    overall_filled = int(bar_length * overall_percentage / 100)
                                    overall_bar = '█' * overall_filled + '░' * (bar_length - overall_filled)
                                    
                                    print(f"\r{self.desc} {percentage:.1f}% |{bar}|\n\n  Total Progress {overall_percentage:.1f}% |{overall_bar}|", end="", flush=True)
                                    title()
                                    self.last_update = self.current
                            
                            def close(self):
                                bar_length = 50
                                overall_percentage = ((self.package_index + 1) / self.total_packages) * 100
                                overall_filled = int(bar_length * overall_percentage / 100)
                                overall_bar = '█' * overall_filled + '░' * (bar_length - overall_filled)
                                print(f"\r{self.desc} 100.0% |{'█' * bar_length}|\n\n  Total Progress {overall_percentage:.1f}% |{overall_bar}|", flush=True)
                        
                        file_pbar = CustomProgressBar(total_size, f"  {package}", package_index, len(extract_roots))
                        try:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    file_pbar.update(len(chunk))
                        finally:
                            file_pbar.close()
                    import zipfile

                    try:
                        with zipfile.ZipFile(temp_file, "r") as zip_ref:
                            extract_root = extract_roots[package]
                            for member in zip_ref.namelist():
                                if member.endswith("/") or member.endswith("\\"):
                                    continue
                                clean_member = member.replace("\\", "/")
                                if extract_root:
                                    target_path = os.path.join(
                                        target_dir, extract_root + clean_member
                                    )
                                else:
                                    target_path = os.path.join(target_dir, clean_member)
                                parent_dir = os.path.dirname(target_path)
                                if parent_dir:
                                    os.makedirs(parent_dir, exist_ok=True)
                                with zip_ref.open(member) as source:
                                    with open(target_path, "wb") as target_file:
                                        target_file.write(source.read())
                        log(f"  ✅ {package} downloaded and extracted")
                        success_count += 1
                    except zipfile.BadZipFile as e:
                        raise DownloadError(
                            f"Downloaded package {package} is corrupted or not a valid zip file",
                            operation="extract_package",
                            details={"package": package, "error": str(e)},
                        )
                    try:
                        os.remove(temp_file)
                    except:
                        import time

                        time.sleep(0.1)
                        try:
                            os.remove(temp_file)
                        except:
                            pass
                except requests.RequestException as e:
                    error_msg = f"Failed to download {package}: {e}"
                    log(f"  ❌ {error_msg}")
                    failed_packages.append(package)
                    raise DownloadError(
                        error_msg,
                        operation="download_package",
                        details={"package": package, "url": package_url},
                    )
                except Exception as e:
                    error_msg = f"Unexpected error downloading {package}: {e}"
                    log(f"  ❌ {error_msg}")
                    failed_packages.append(package)
                    raise DownloadError(
                        error_msg,
                        operation="download_package",
                        details={"package": package, "error": str(e)},
                    )
                finally:
                    pbar.update(1)
        log(f"✅ Successfully downloaded {success_count}/{len(extract_roots)} packages")
        app_settings_content = """<?xml version="1.0" encoding="UTF-8"?>
<Settings>
    <ContentFolder>content</ContentFolder>
    <BaseUrl>http://www.roblox.com</BaseUrl>
</Settings>"""
        app_settings_path = os.path.join(target_dir, "AppSettings.xml")
        try:
            with open(app_settings_path, "w", encoding="utf-8") as f:
                f.write(app_settings_content)
            log(f"  ✅ Created AppSettings.xml")
        except Exception as e:
            log(f"  ❌ Failed to create AppSettings.xml: {e}")
        if success_count < len(extract_roots):
            if failed_packages:
                log(
                    f"⚠️  Some packages failed to download: {', '.join(failed_packages)}"
                )
            else:
                log(
                    f"⚠️  Some packages failed to download, but {success_count} succeeded"
                )
        if success_count == 0:
            raise DownloadError(
                "No packages were successfully downloaded",
                operation="download_all_packages",
                details={
                    "total_packages": len(extract_roots),
                    "failed_packages": failed_packages,
                },
            )
        return f"https://setup.roblox.com/version-{base_hash}"
    except DownloadError:
        raise
    except requests.RequestException as e:
        raise DownloadError(
            f"Network error while fetching Roblox client settings: {e}",
            operation="fetch_version_info",
            details={"url": version_url},
        )
    except Exception as e:
        raise DownloadError(
            f"Unexpected error in get_roblox_client_settings: {e}",
            operation="get_roblox_client_settings",
            details={"error": str(e)},
        )


def byebanasync(wait=True):
    try:
        log("\n" + "=" * 41)
        log("ByeBanAsync v2.2 | credits to: centerepic")
        log("=" * 41)

        user_profile = os.environ.get("USERPROFILE")
        if not user_profile:
            log("[!!!] Could not get USERPROFILE environment variable.")
            return
        log("\n--- MAC Address Spoofing ---")
        change_mac = (
            input("[?] Do you want to attempt to change your MAC address? (y/n): ")
            .strip()
            .lower()
        )
        if change_mac == "y":
            adapters = list_network_adapters()
            if not adapters:
                log("[!] No suitable network adapters found to modify.")
            else:
                log("\n[i] Available network adapters:")
                for i, adapter in enumerate(adapters, 1):
                    log(f"  [{i}] {adapter['description']}")
                    log(f"     └─ Connection Name: '{adapter['connection_name']}'")

                while True:
                    try:
                        choice = int(
                            input("\n[?] Enter the number of the adapter to change: ")
                        )
                        if 1 <= choice <= len(adapters):
                            selected_adapter = adapters[choice - 1]
                            break
                        else:
                            log(
                                "[!] Invalid selection. Please enter a number from the list."
                            )
                    except ValueError:
                        log(
                            "[!] Invalid selection. Please enter a number from the list."
                        )

                random_mac = generate_random_mac_address()
                log(
                    f"[>] Attempting to set MAC for adapter: '{selected_adapter['description']}' (ID: {selected_adapter['id']})..."
                )
                try:
                    change_mac_address(selected_adapter["id"], random_mac)
                    log("[√] Successfully updated registry for MAC address.")
                    log(
                        f"[>] Attempting to restart network adapter '{selected_adapter['connection_name']}' to apply changes..."
                    )
                    try:
                        restart_network_adapter(selected_adapter["connection_name"])
                        log(
                            f"[√] Network adapter '{selected_adapter['connection_name']}' restarted. MAC address change should now be active."
                        )
                        log("[i] Verify with 'ipconfig /all' or 'getmac'.")
                    except Exception as e:
                        log(
                            f"[!!!] Error restarting network adapter: {e}. You may need to do this manually or reboot."
                        )
                except Exception as e:
                    log(f"[!!!] Error changing MAC address in registry: {e}")
        else:
            log("[i] Skipping MAC address change.")
        log("\n[...] ByeBanAsync completed!")
    except Exception as e:
        log(f"[!!!] Error in ByeBanAsync: {e}")

def generate_random_mac_address():
    import random

    mac_bytes = [0x02] + [random.randint(0, 255) for _ in range(5)]
    return "".join(f"{byte:02X}" for byte in mac_bytes)

def list_network_adapters():
    try:
        import winreg

        adapters = []
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}",
        ) as class_key:
            for i in range(10000):  

                try:
                    subkey_name = f"{i:04d}"
                    with winreg.OpenKey(class_key, subkey_name) as adapter_key:
                        try:
                            driver_desc = winreg.QueryValueEx(
                                adapter_key, "DriverDesc"
                            )[0]
                            net_cfg_instance_id = winreg.QueryValueEx(
                                adapter_key, "NetCfgInstanceID"
                            )[0]

                            try:
                                connection_path = f"SYSTEM\\CurrentControlSet\\Control\\Network\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{net_cfg_instance_id}\\Connection"
                                with winreg.OpenKey(
                                    winreg.HKEY_LOCAL_MACHINE, connection_path
                                ) as conn_key:
                                    connection_name = winreg.QueryValueEx(
                                        conn_key, "Name"
                                    )[0]
                            except:
                                connection_name = driver_desc

                            desc_lower = driver_desc.lower()
                            if not any(
                                keyword in desc_lower
                                for keyword in [
                                    "virtual",
                                    "loopback",
                                    "bluetooth",
                                    "wan miniport",
                                    "tap-windows",
                                    "pseudo",
                                ]
                            ):
                                adapters.append(
                                    {
                                        "id": subkey_name,
                                        "description": driver_desc,
                                        "connection_name": connection_name,
                                    }
                                )
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
    try:
        import winreg

        path = f"SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\{adapter_id}"
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE
        ) as adapter_key:
            log(f"[>] Setting 'NetworkAddress' to '{mac_address}'")
            winreg.SetValueEx(
                adapter_key, "NetworkAddress", 0, winreg.REG_SZ, mac_address
            )
    except ImportError:
        raise Exception("winreg module not available")
    except Exception as e:
        raise Exception(f"Registry error: {e}")

def restart_network_adapter(connection_name):
    import time

    log(f"[>] Disabling adapter: '{connection_name}'")
    disable_result = subprocess.run(
        [
            "netsh",
            "interface",
            "set",
            "interface",
            f"name={connection_name}",
            "admin=disable",
        ],
        capture_output=True,
        text=True,
    )
    if disable_result.returncode != 0:
        error_msg = disable_result.stderr.strip()
        raise Exception(f"Failed to disable network adapter. Netsh output: {error_msg}")
    time.sleep(2)
    log(f"[>] Enabling adapter: '{connection_name}'")
    enable_result = subprocess.run(
        [
            "netsh",
            "interface",
            "set",
            "interface",
            f"name={connection_name}",
            "admin=enable",
        ],
        capture_output=True,
        text=True,
    )
    if enable_result.returncode != 0:
        error_msg = enable_result.stderr.strip()
        raise Exception(f"Failed to enable network adapter. Netsh output: {error_msg}")


def run_command(cmd, capture_output=True, shell=False):
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    log(f"  🔧 Running command: {cmd_str}")
    try:
        if capture_output:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=shell)

            if result.stdout and result.stdout.strip():
                log(f"  📤 STDOUT: {result.stdout.strip()}")

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
    try:
        run_command(f'notepad "{LP}"', capture_output=False, shell=True)
    except Exception as e:
        print(f"Error opening log: {e}")

def launch_roblox():
    try:

        roblox_versions_dir = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions")
        if not os.path.exists(roblox_versions_dir):
            log("  ❌ Roblox Versions directory not found")
            return False

        version_dirs = [
            d
            for d in os.listdir(roblox_versions_dir)
            if os.path.isdir(os.path.join(roblox_versions_dir, d))
            and d.startswith("version-")
        ]
        if not version_dirs:
            log("  ❌ No Roblox version directories found")
            return False

        latest_version = sorted(version_dirs)[-1]
        roblox_exe_path = os.path.join(
            roblox_versions_dir, latest_version, "RobloxPlayerBeta.exe"
        )
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
    config = load_config()

    if not validate_config(config):
        print("Invalid configuration. Using default settings.")
        config = get_default_config()

    print(BANNER)
    print(" Slate - Roblox Cleaning Tool")

    global LOG, OPEN_LOG, LP, PROCS, PATHS, REGS
    LOG = config["general"]["log_enabled"]
    OPEN_LOG = config["general"]["open_log_on_exit"]
    PROCS = config["processes"]["roblox_processes"]
    PATHS = config["paths"]["temp_folders"] + config["paths"]["roblox_folders"]
    REGS = config["registry"]["registry_paths"]

    if LOG:
        try:
            with open(LP, "w") as f:
                f.write("=== Slate Log ===\n")
                f.write(
                    "If you experience any errors, please DM 'midinterlude' on Discord.\n"
                )
                f.write(f"Configuration loaded from slate.config.json\n")
                f.write(f"Profile: {config.get('profile', 'custom')}\n")
        except Exception:
            pass

    while True:
        proceed = (
            input(
                '\n This script will clean every file linked to roblox and may restart your computer.\n Type "confirm" to proceed or "info" for additional information: '
            )
            .strip()
            .lower()
        )
        if proceed == "info":
            print("\n" + "=" * 60)
            print("SLATE - CONFIGURATION SUMMARY")
            print("=" * 60)
            print(f"Configuration file: slate.config.json")
            print(f"Profile: {config.get('profile', 'custom')}")
            print(f"Log file: {LP}")
            print("\nCleaning Operations:")
            print(
                f"  • Process Termination: {'Enabled' if config.get('cleaning', {}).get('kill_processes', False) else 'Disabled'}"
            )
            print(
                f"  • Folder Cleaning: {'Enabled' if config.get('cleaning', {}).get('clean_folders', False) else 'Disabled'}"
            )
            print(
                f"  • Cookie Removal: {'Enabled' if config.get('cleaning', {}).get('remove_cookies', False) else 'Disabled'}"
            )
            print(
                f"  • DNS Cache Flush: {'Enabled' if config.get('cleaning', {}).get('flush_dns', False) else 'Disabled'}"
            )
            print(
                f"  • Registry Cleanup: {'Enabled' if config.get('cleaning', {}).get('clean_registry', False) else 'Disabled'}"
            )
            print(
                f"  • Prefetch Cleanup: {'Enabled' if config.get('cleaning', {}).get('clean_prefetch', False) else 'Disabled'}"
            )
            print(
                f"  • Explorer Restart: {'Enabled' if config.get('cleaning', {}).get('restart_explorer', False) else 'Disabled'}"
            )
            print(f"\nRoblox Operations:")
            print(
                f"  • Download Roblox: {'Enabled' if config.get('roblox', {}).get('download_roblox', False) else 'Disabled'}"
            )
            print(
                f"  • Launch Roblox: {'Enabled' if config.get('roblox', {}).get('launch_roblox_on_exit', False) else 'Disabled'}"
            )
            print(
                f"  • Create AppSettings: {'Enabled' if config.get('roblox', {}).get('create_appsettings', False) else 'Disabled'}"
            )
            print(f"\nAdvanced Options:")
            print(
                f"  • Auto Restart: {'Enabled' if config.get('advanced', {}).get('auto_restart_after_cleaning', False) else 'Disabled'}"
            )
            print(
                f"  • Skip Prompts: {'Enabled' if config.get('advanced', {}).get('skip_confirmation_prompts', False) else 'Disabled'}"
            )
            print(
                f"  • Force Deletion: {'Enabled' if config.get('advanced', {}).get('force_file_deletion', False) else 'Disabled'}"
            )
            print("=" * 60)
            continue
        elif proceed in ["confirm", "yes", "y"]:
            break
        else:
            print("Cancelling operation.")
            return
    errors = []
    operation_start_time = {}

    def log_operation_start(operation_name):
        import time

        operation_start_time[operation_name] = time.time()
        log(f"🚀 Starting {operation_name}...")

    def log_operation_end(operation_name, success=True, error_msg=None):
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
                result = run_command(["taskkill", "/f", "/im", process])
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
            result = run_command(["ipconfig", "/flushdns"])
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
                run_command(["taskkill", "/f", "/im", "explorer.exe"])
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
                log_operation_end(
                    "Registry cleanup",
                    False,
                    f"Some registry paths not found: {registry_errors}",
                )
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
                log_operation_end("Prefetch cleanup")
            else:
                log("  - No prefetch files found")
                log_operation_end("Prefetch cleanup")
            title()
        if config["tools"]["run_byebanasync"]:
            log_operation_start("ByeBanAsync")
            try:
                log(
                    "\nByeBanAsync's python port - original credits to @centerepic"
                )
                byebanasync(wait=True)
                log_operation_end("ByeBanAsync")
            except (NetworkError, ProcessError) as e:
                log_operation_end("ByeBanAsync", False, str(e))
                errors.append(f"ByeBanAsync failed: {e}")
                log(f"🔍 Detailed ByeBanAsync error info: {e.details}")
        
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
        
        if errors:
            log("\n⚠️  Some operations reported issues:")
            for i, e in enumerate(errors, 1):
                log(f"   {i}. {e}")

        if config["advanced"]["auto_restart_after_cleaning"]:
            if OPEN_LOG and LOG:
                log_thread = threading.Thread(target=open_log_async, daemon=True)
                log_thread.start()
            run_command("shutdown /r /t 0", capture_output=False, shell=True)
        else:
            if config["roblox"]["launch_roblox_on_exit"]:
                should_launch = True
                if not config["advanced"]["skip_confirmation_prompts"]:
                    launch_choice = input("\nDo you want to launch Roblox now? (confirm): ")
                    should_launch = launch_choice.lower().strip() in ["confirm", "yes", "y"]
                
                if should_launch:
                    title()
                    log_operation_start("Roblox launch")
                    if launch_roblox():
                        log_operation_end("Roblox launch")
                        log("✅ Roblox is starting up!")
                    else:
                        log_operation_end("Roblox launch", False, "Launch failed")
                        log("❌ Failed to launch Roblox automatically")
                        log("   You can launch it manually from the Roblox Player shortcut")
            log(
                "\nExiting without restarting. (You may want to restart manually to ensure all changes take effect.)"
            )
            print(
                "Thank you for using Slate! If you had any issues, please DM 'midinterlude' on Discord with the log file."
            )

            if LOG:
                pass
            if not config["advanced"]["skip_confirmation_prompts"]:
                input("Press Enter to exit.")
            if OPEN_LOG and LOG:
                log_thread = threading.Thread(target=open_log_async, daemon=True)
                log_thread.start()

            os._exit(0)
    except KeyboardInterrupt:
        log("\n⚠️  Operation cancelled by user")
        print("\nOperation cancelled by user.")
    except SlateError as e:
        log(f"\n❌ Slate error in {e.operation}: {e}")
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

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        exit()
    else:
        main()

