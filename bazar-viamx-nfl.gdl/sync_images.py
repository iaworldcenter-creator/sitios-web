import os
import shutil

def sync_images():
    workspace_dir = r"d:\Downloads\Proyecto Web\images"
    public_dir = r"C:\Users\nflgd\.claude\ViaMX_Global_Publico\images"
    
    os.makedirs(workspace_dir, exist_ok=True)
    os.makedirs(public_dir, exist_ok=True)
    
    # 1. Rename human-readable user folders to product IDs in the public directory (C:)
    rename_map = {
        "refrigerador": "LUX-2026-091",
        "lavadora": "LUX-2026-092",
        "Performance defined by design": "LUX-2026-097"
    }
    
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(public_dir, old_name)
        new_path = os.path.join(public_dir, new_name)
        if os.path.exists(old_path):
            if os.path.exists(new_path):
                print(f"Merging {old_name} folder into {new_name} in public directory")
                for fn in os.listdir(old_path):
                    shutil.move(os.path.join(old_path, fn), os.path.join(new_path, fn))
                shutil.rmtree(old_path)
            else:
                os.rename(old_path, new_path)
                print(f"Renamed {old_name} folder to {new_name} in public directory")

    # 2. Sync from public (C:) to workspace (D:)
    copied_folders_to_workspace = 0
    copied_files_to_workspace = 0
    for item in os.listdir(public_dir):
        pub_item_path = os.path.join(public_dir, item)
        if os.path.isdir(pub_item_path) and item.startswith("LUX-2026-"):
            work_item_path = os.path.join(workspace_dir, item)
            if not os.path.exists(work_item_path):
                os.makedirs(work_item_path, exist_ok=True)
                copied_folders_to_workspace += 1
            for fn in os.listdir(pub_item_path):
                src = os.path.join(pub_item_path, fn)
                dest = os.path.join(work_item_path, fn)
                if not os.path.exists(dest):
                    shutil.copy2(src, dest)
                    copied_files_to_workspace += 1
                    
    # 3. Sync from workspace (D:) to public (C:)
    copied_folders_to_public = 0
    copied_files_to_public = 0
    for item in os.listdir(workspace_dir):
        work_item_path = os.path.join(workspace_dir, item)
        if os.path.isdir(work_item_path) and item.startswith("LUX-2026-"):
            pub_item_path = os.path.join(public_dir, item)
            if not os.path.exists(pub_item_path):
                os.makedirs(pub_item_path, exist_ok=True)
                copied_folders_to_public += 1
            for fn in os.listdir(work_item_path):
                src = os.path.join(work_item_path, fn)
                dest = os.path.join(pub_item_path, fn)
                if not os.path.exists(dest):
                    shutil.copy2(src, dest)
                    copied_files_to_public += 1
                    
    # Also sync flat files (legacy single images)
    copied_flat_to_workspace = 0
    for fn in os.listdir(public_dir):
        if fn.startswith("prod_LUX-2026-") and fn.endswith(".jpg"):
            src = os.path.join(public_dir, fn)
            dest = os.path.join(workspace_dir, fn)
            if not os.path.exists(dest):
                shutil.copy2(src, dest)
                copied_flat_to_workspace += 1
                
    copied_flat_to_public = 0
    for fn in os.listdir(workspace_dir):
        if fn.startswith("prod_LUX-2026-") and fn.endswith(".jpg"):
            src = os.path.join(workspace_dir, fn)
            dest = os.path.join(public_dir, fn)
            if not os.path.exists(dest):
                shutil.copy2(src, dest)
                copied_flat_to_public += 1

    print("Image synchronization report:")
    print(f"  Folders synced to Workspace: {copied_folders_to_workspace} (files: {copied_files_to_workspace})")
    print(f"  Folders synced to Public: {copied_folders_to_public} (files: {copied_files_to_public})")
    print(f"  Legacy flat images synced to Workspace: {copied_flat_to_workspace}")
    print(f"  Legacy flat images synced to Public: {copied_flat_to_public}")

if __name__ == "__main__":
    sync_images()
