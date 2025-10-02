import argparse
from pathlib import Path
from .wipe import secure_delete_with_report, wipe_free_with_report
from .utils import list_drives

def main():
    parser = argparse.ArgumentParser(description="Secure Deletion Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Secure delete file/folder
    parser_wipe = subparsers.add_parser("wipe", help="Securely delete a file or folder")
    parser_wipe.add_argument("path", help="File or folder to delete")
    parser_wipe.add_argument("--passes", type=int, default=3, help="Number of overwrite passes")

    # Wipe-free / preview
    parser_wipe_free = subparsers.add_parser("wipe-free", help="Preview or wipe free space in a folder/drive")
    parser_wipe_free.add_argument("path", help="Folder or drive to wipe free space")
    parser_wipe_free.add_argument("--passes", type=int, default=1, help="Number of overwrite passes")
    parser_wipe_free.add_argument("--preview", action="store_true", help="Preview only, no deletion")

    # List drives
    parser_list = subparsers.add_parser("list-drives", help="List mounted drives")
    parser_list.add_argument("--removable", action="store_true", help="Show only removable/USB drives")

    args = parser.parse_args()

    try:
        if args.command == "wipe":
            secure_delete_with_report(Path(args.path), passes=args.passes)
            print(f"✅ Successfully deleted: {args.path}")

        elif args.command == "wipe-free":
            wipe_free_with_report(Path(args.path), passes=args.passes, preview=args.preview)

        elif args.command == "list-drives":
            drives = list_drives(only_removable=getattr(args, "removable", False))
            if not drives:
                print("No drives found.")
            else:
                print("Available drives:")
                for d in drives:
                    if isinstance(d, dict):
                        print(f"{d['device']} ({d['mountpoint']}) - Free: {d['free']/(1024**3):.2f} GB")
                    else:
                        print(f" - {d}")

    except FileNotFoundError as e:
        print(f"❌ File/Folder not found: {e}")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
