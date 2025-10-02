from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path

def generate_report(action_type, target_path, passes=1, status="Success", filename="wipe_report.pdf"):
    """
    Generates a PDF report for secure delete or free space wipe.
    :param action_type: "Secure Delete" or "Free Space Wipe"
    :param target_path: Path of file/folder/drive
    :param passes: Number of overwrite passes
    :param status: Operation status
    :param filename: PDF filename
    """
    target_path = str(target_path)
    filename = Path(filename)
    
    c = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Secure Deletion Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 120, f"Action: {action_type}")
    c.drawString(50, height - 140, f"Target Path: {target_path}")
    c.drawString(50, height - 160, f"Overwrite Passes: {passes}")
    c.drawString(50, height - 180, f"Status: {status}")
    
    c.save()
    print(f"📄 Report generated: {filename.resolve()}")
