# Secure Deletion Tool for NGOs

A secure file and folder deletion tool designed for NGOs to safely erase sensitive data. Features include:

- File & Folder Secure Deletion (3-pass, Gutmann optional)
- Free Space Wiping
- USB / Removable Drive Detection
- PDF Reports for Audit
- GUI and CLI Interface
- Batch files for easy NGO usage

### GUI
Double-click `run_gui.bat` and use the interface to delete files or wipe free space.

### CLI
Double-click `run_cli.bat` or run commands:

```bash
list-drives --removable
wipe C:\Temp\file.txt --passes 3
wipe-free E:\ --passes 1 --preview
