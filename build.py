import json
import uuid
import os
import zipfile
import requests

with open('manifest.json', 'r') as file:
    data = json.load(file)

# replace uuids in manifest file
data['header']['uuid'] = str(uuid.uuid4())
data['modules'][0]['uuid'] = str(uuid.uuid4())

with open('manifest.json', 'w') as file:
    json.dump(data, file, indent=2)

# create and replace item_texture.json
def save_data(data, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

# copy data from each json
with open('json/plushies.json', 'r') as pfile, open('json/food.json', 'r') as ffile, open('json/items.json', 'r') as ifile:
    plushies = json.load(pfile)
    food = json.load(ffile)
    item = json.load(ifile)

# combine data
combined_items = {**plushies['items'], **food['items'], **item['items']}

# create new file
combined_data = {
    "resource_pack_name": "Plushies!",
    "texture_name": "atlas.items",
    "texture_data": combined_items
}

save_data(combined_data, 'textures/item_texture.json')

# get server icon
def get_icon():
    with open("pack_icon.png", "wb") as f:
        f.write(requests.get(f"https://api.mcstatus.io/v2/icon/akoot.co").content)

get_icon()

# zip everything
def zip_directory(src_dir, zip_name, exclude_folders=[], exclude_files=[]):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_dir):
            # exclude the specified folders
            dirs[:] = [d for d in dirs if d not in exclude_folders]

            for file in files:
                # skip the zip file being created
                if file == zip_name:
                    continue

                if file in exclude_files:
                    continue

                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, src_dir))

folders_to_exclude = ['json', '.git', ".idea"]
files_to_exclude = ['build.py', 'build.bat']

zip_directory('./', 'bedrock_pack.zip', folders_to_exclude, files_to_exclude)