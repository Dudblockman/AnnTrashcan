import os
import re

# Paths to mods and config folders
mods_folder = "/home/lwp/web_interface/AnnTrashcanBeta/mods"
config_folder = "/home/lwp/web_interface/AnnTrashcanBeta/config"

# Function to clean names by removing special characters and common suffixes
def clean_name(name):
    name = re.sub(r'[^a-z0-9]', '', name.lower())  # Remove special characters
    return re.sub(r'(mod|mods)$', '', name)  # Remove common suffixes like "mod" or "mods"

# Extract mod names from .pw.toml files
installed_mods = set()
for file in os.listdir(mods_folder):
    if file.endswith(".pw.toml"):
        mod_name = clean_name(file.replace(".pw.toml", ""))
        installed_mods.add(mod_name)

# Check config files and folders against installed mods
unused_configs = []
for root, dirs, files in os.walk(config_folder):
    # Check if folder name matches any mod name
    folder_name = clean_name(os.path.basename(root))
    if any(mod in folder_name or folder_name in mod for mod in installed_mods):
        continue  # Skip this folder if it matches or is a subset of a mod name

    for file in files:
        config_name = clean_name(file.split('.')[0])  # Clean base name of config file
        # Check if any mod name matches the cleaned config name
        if not any(mod in config_name or config_name in mod for mod in installed_mods):
            unused_configs.append(os.path.join(root, file))

# Output unused config files
print("Unused Config Files:")
for config in unused_configs:
    print(config)