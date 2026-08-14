import os
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse
import sys
import subprocess

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(WORKSPACE_DIR, "data", "catalog.json")
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Install Pillow if not present for image optimization
try:
    from PIL import Image
    print("Pillow is already installed.")
except ImportError:
    print("Pillow is not installed. Installing Pillow...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image
    except Exception as e:
        print(f"Could not install Pillow: {e}. Fallback to direct downloads.")
        Image = None

def optimize_image(temp_path, dest_path):
    if Image is None:
        # Fallback to copy/rename directly if Pillow is not available
        import shutil
        shutil.copy2(temp_path, dest_path)
        return True
    
    try:
        with Image.open(temp_path) as img:
            # Convert to RGB if PNG/RGBA to save as JPEG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize if too large (e.g. max width 600px)
            max_size = 600
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Save optimized JPEG
            img.save(dest_path, "JPEG", quality=85, optimize=True)
            return True
    except Exception as e:
        print(f"Error optimizing image: {e}")
        # Final fallback: copy directly
        try:
            import shutil
            shutil.copy2(temp_path, dest_path)
            return True
        except:
            return False

def download_all():
    if not os.path.exists(CATALOG_PATH):
        print(f"Catalog {CATALOG_PATH} not found!")
        return

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    print(f"Processing {len(products)} products...")
    
    updated = False
    for i, p in enumerate(products):
        p_id = p["id"]
        image_url = p["image"]
        
        # If already local, skip downloading unless forced
        if image_url.startswith("images/") and os.path.exists(os.path.join(WORKSPACE_DIR, image_url)):
            print(f"Product {p_id} image already local: {image_url}")
            continue

        # Check if URL looks valid
        if not image_url.startswith("http"):
            print(f"Skipping non-http URL for product {p_id}: {image_url}")
            continue

        ext = ".jpg" # Default extension
        dest_filename = f"prod_{p_id}{ext}"
        dest_file = os.path.join(IMAGES_DIR, dest_filename)

        if os.path.exists(dest_file):
            p["image"] = f"images/{dest_filename}"
            updated = True
            print(f"Product {p_id} image already exists locally: images/{dest_filename}")
            continue

        print(f"[{i+1}/{len(products)}] Downloading image for product {p_id} ({p['title']})...")
        
        temp_file = os.path.join(IMAGES_DIR, f"temp_{p_id}")
        dest_filename = f"prod_{p_id}{ext}"
        dest_file = os.path.join(IMAGES_DIR, dest_filename)
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            req = urllib.request.Request(image_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response, open(temp_file, "wb") as out_file:
                out_file.write(response.read())
            
            # Optimize and save
            success = optimize_image(temp_file, dest_file)
            
            # Remove temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            if success:
                p["image"] = f"images/{dest_filename}"
                updated = True
                print(f"  Saved and optimized as images/{dest_filename}")
            else:
                print(f"  Failed to process/optimize image for {p_id}")
        except Exception as e:
            print(f"  Error downloading image for {p_id}: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

    if updated:
        # Save updated catalog back to all files
        paths = [
            CATALOG_PATH,
            os.path.join(WORKSPACE_DIR, "docs", "data", "catalog.json"),
            r"C:\Users\nflgd\.claude\ViaMX_Global_Publico\data\catalog.json",
            r"C:\Users\nflgd\.claude\ViaMX_Global_Publico\docs\data\catalog.json"
        ]
        
        for path in paths:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(products, f, indent=2, ensure_ascii=False)
                print(f"Catalog database updated with local image paths at: {path}")
            except Exception as e:
                print(f"Failed to update catalog {path}: {e}")
                
        # Also copy all images to the public directory
        public_images_dir = r"C:\Users\nflgd\.claude\ViaMX_Global_Publico\images"
        os.makedirs(public_images_dir, exist_ok=True)
        print("Synchronizing images directory with the public folder...")
        import shutil
        for fn in os.listdir(IMAGES_DIR):
            if fn.startswith("prod_") and fn.endswith(".jpg"):
                shutil.copy2(os.path.join(IMAGES_DIR, fn), os.path.join(public_images_dir, fn))
        print("Images directory synchronized successfully.")

if __name__ == "__main__":
    download_all()
