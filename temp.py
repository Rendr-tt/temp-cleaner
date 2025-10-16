import ctypes
import shutil
import glob
from pathlib import Path
from tqdm import tqdm

def has_admin_rights() -> bool:
    """Return True if running as Administrator."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def purge_directory(target_path: Path, label: str):
    """Remove all files and folders inside a given path."""
    if not target_path.exists():
        print(f"[{label}] ❌ Directory not found: {target_path}")
        return

    all_items = list(target_path.glob('*'))
    if not all_items:
        print(f"[{label}] ✅ Already clean.")
        return

    print(f"[{label}] Cleaning {len(all_items)} items...")

    with tqdm(total=len(all_items), desc=f"{label}", unit="item") as bar:
        for item in all_items:
            try:
                if item.is_file() or item.is_symlink():
                    item.unlink(missing_ok=True)
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
            except Exception:
                # Silently skip problematic items
                pass
            finally:
                bar.update(1)

def main():
    root_dir = Path.home().drive  # Usually 'C:\\'
    system_temp = Path(Path().joinpath(root_dir, "Windows", "Temp"))
    user_temp = Path(Path().joinpath(Path.home(), "AppData", "Local", "Temp"))
    prefetch_dir = Path(Path().joinpath(root_dir, "Windows", "Prefetch"))

    print("\n🧹 Starting cleanup...\n")

    purge_directory(system_temp, "System Temp")
    purge_directory(user_temp, "User Temp")

    if has_admin_rights():
        purge_directory(prefetch_dir, "Prefetch")
    else:
        print("[Prefetch] ⚠️ Skipped — requires administrator privileges.\n")

    input("\nCleanup finished. Press Enter to close...")

if __name__ == "__main__":
    main()
