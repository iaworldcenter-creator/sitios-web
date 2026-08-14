import os
import time

path = r"d:\Descargas\Proyecto Web"
print(f"=== Files in {path} ===")
if not os.path.exists(path):
    print("Does not exist!")
    exit(0)

for root, _, files in os.walk(path):
    for file in files:
        fpath = os.path.join(root, file)
        rel = os.path.relpath(fpath, path)
        size = os.path.getsize(fpath)
        mtime = os.path.getmtime(fpath)
        date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print(f"  {rel} - Size: {size} bytes - Modified: {date_str}")
