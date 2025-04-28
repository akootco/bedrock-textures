import json
import uuid
import os
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

# generate sound_definitions.json
def generate_sound_definitions(folder, output_file):
    sounds = {
        f"plushies:{os.path.splitext(f)[0]}": {
            "category": "record",
            "max_distance": 64.0,
            "sounds": [{
                "name": f"sounds/{os.path.splitext(f)[0]}",
                "stream": True
            }]
        }
        for f in os.listdir(folder)
        if f.endswith('.ogg')
    }

    with open(output_file, "w") as f:
        json.dump({"format_version": "1.14.0", "sound_definitions": sounds}, f, indent=2)

# Call it (change folder path if needed)
generate_sound_definitions("sounds", "sounds/sound_definitions.json")

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