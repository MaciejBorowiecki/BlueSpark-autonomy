import os

target_dir = './todo/'

image_extensions = ('.jpg', '.jpeg')

try:
    all_files = os.listdir(target_dir)
except FileNotFoundError:
    print(f"CRITICAL ERROR: Directory '{target_dir}' not found.")
    print("Please make sure the script is run from the correct location.")
    exit()  # Exit the script if the folder is missing

image_files = [f for f in all_files
               if os.path.isfile(os.path.join(target_dir, f))
               and f.lower().endswith(image_extensions)]

image_files.sort()

print(f"Found {len(image_files)} files to rename in '{target_dir}'.")

counter = 1

for old_name in image_files:
    _root, ext = os.path.splitext(old_name)

    # Normalise extension
    ext_lower = ext.lower()

    if ext_lower == '.jpeg':
        final_ext = '.jpg'  # Convert .jpeg to .jpg
    else:
        final_ext = ext_lower

    # This is just the new FILENAME, e.g., '0001.jpg'
    new_name_only = f"{counter:04d}{final_ext}"

    # e.g., ./todo/vacation.jpg
    old_path = os.path.join(target_dir, old_name)
    new_path = os.path.join(target_dir, new_name_only)  # e.g., ./todo/0001.jpg

    try:
        # Use the full paths
        os.rename(old_path, new_path)
        # We also change the printout to show the full paths
        print(f"Renamed: {old_path}  ->  {new_path}")
        counter += 1
    except OSError as e:
        print(f"ERROR: Could not rename {old_path} to {new_path}. Reason: {e}")
    except FileExistsError:
        print(
            f"ERROR: File named {new_path} already exists. Skipping {old_path}.")


print(f"\nDone. Renamed {counter - 1} files.")
