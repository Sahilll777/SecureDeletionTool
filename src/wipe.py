from pathlib import Path
import os

def secure_delete(path: Path, passes: int = 3):
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    if path.is_file():
        size = path.stat().st_size
        with open(path, "r+b") as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(size))
        path.unlink()
        print(f"✅ Deleted file: {path}")
    else:
        for f in path.rglob("*"):
            if f.is_file():
                secure_delete(f, passes)
        path.rmdir()
        print(f"✅ Deleted folder: {path}")

def wipe_free(path: Path, passes: int = 1, preview: bool = False):
    """
    Preview or wipe free space in a folder or drive.
    """
    if not path.exists():
        # Create dummy folder if missing for testing
        print(f"⚠️ Path not found: {path}. Creating temporary test folder...")
        path.mkdir(parents=True, exist_ok=True)
        for i in range(3):
            dummy_file = path / f"test_file_{i+1}.txt"
            dummy_file.write_text(f"This is dummy file {i+1} for testing.")
        print(f"✅ Temporary folder with dummy files created at: {path}")

    if path.is_file():
        if not preview:
            secure_delete(path, passes=passes)
        else:
            print(f"File to delete: {path}")
    else:
        files = list(path.rglob("*"))
        if preview:
            print("Files to be deleted:")
            for f in files:
                print(f" - {f}")
        else:
            for f in files:
                secure_delete(f, passes=passes)
from .report import generate_report

def secure_delete_with_report(pathlike, passes=3):
    try:
        secure_delete(pathlike, passes)
        generate_report("Secure Delete", pathlike, passes, status="Success")
    except Exception as e:
        generate_report("Secure Delete", pathlike, passes, status=f"Failed: {e}")
        raise e

def wipe_free_with_report(pathlike, passes=1, preview=False):
    try:
        wipe_free(pathlike, passes=passes, preview=preview)
        if not preview:
            generate_report("Free Space Wipe", pathlike, passes, status="Success")
    except Exception as e:
        generate_report("Free Space Wipe", pathlike, passes, status=f"Failed: {e}")
        raise e
               
