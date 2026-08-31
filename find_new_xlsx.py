import os
import glob

print("Checking XLSX files across directories:")
for d in [r"E:\sitios web\pc-custom-lab\data", r"E:\sitios web\data", r"E:\sitios web", r"C:\Users\nflgd\Downloads"]:
    if os.path.exists(d):
        print(f"\nDirectory: {d}")
        files = glob.glob(os.path.join(d, "*.xlsx"))
        for f in sorted(files, key=os.path.getmtime, reverse=True):
            mtime = os.path.getmtime(f)
            size = os.path.getsize(f)
            print(f"  - {os.path.basename(f)} ({size} bytes, mtime: {mtime})")
