# src/utils.py
import string
import ctypes
import shutil
import platform

def list_drives(only_removable: bool = False):
    """
    List all available drives on Windows (or fallback for other OSes).
    Returns a list of dicts: {'device': 'C:', 'mountpoint': 'C:\\', 'free': free_bytes}
    """
    drives_list = []

    if platform.system() == "Windows":
        # Get bitmask of logical drives
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i, letter in enumerate(string.ascii_uppercase):
            if bitmask & (1 << i):
                drive_path = f"{letter}:\\"
                if only_removable:
                    # Check if drive is removable
                    drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
                    if drive_type != 2:  # 2 = DRIVE_REMOVABLE
                        continue
                try:
                    total, used, free = shutil.disk_usage(drive_path)
                    drives_list.append({
                        "device": letter + ":",
                        "mountpoint": drive_path,
                        "free": free
                    })
                except PermissionError:
                    continue
    else:
        # Non-Windows fallback: just return root
        total, used, free = shutil.disk_usage("/")
        drives_list.append({"device": "/", "mountpoint": "/", "free": free})

    return drives_list
