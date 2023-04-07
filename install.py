import zipfile
import xmltodict
import os
from pathlib import Path
import shutil
from datetime import datetime
# import pandas as pd
import sqlite3
import sqlalchemy 
import argparse

def install_pack(pack_path):
    # pack is a zipped file with arcl presets, xmls, and samples
    # unpack the pack, grab the xml, and add the samples to the db
    # before doing anything, backup .db file
    shutil.copyfile("SubLab.db", f"SubLab.db.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}")
    with zipfile.ZipFile(pack_path, 'r') as zip_ref:
        zip_ref.extractall("temp")
    with open("temp/sublab-pack.xml", "r") as f:
        xml_str = f.read()
    # list arcl files and copy them to the Patches folder
    arcl_files = [f for f in os.listdir("temp") if f.endswith(".arcl")]
    
    add_pack(xml_str[8:xml_str.index("sublab_pack>") + 12], arcl_files)

    
def add_pack(pack_xml, arcl_files):
    pack = xmltodict.parse(pack_xml)
    if not os.path.exists(Path("Patches/"+pack["sublab_pack"]["@name"])):
        os.makedirs(Path("Patches/"+pack["sublab_pack"]["@name"]))
    for arcl in arcl_files:
        shutil.copyfile(os.path.join("temp", arcl),
                        os.path.join("Patches", pack["sublab_pack"]["@name"], arcl))
    shutil.copyfile(os.path.join("temp", "bank.png"),
                    os.path.join("Patches", pack["sublab_pack"]["@name"], "bank.png"))
    if type(pack["sublab_pack"]["sample"]) == dict:
        pack["sublab_pack"]["sample"] = [pack["sublab_pack"]["sample"]]
    for sample in pack["sublab_pack"]["sample"]:            
        sample = sample["VALUE"]
        print(f"Adding {sample[0]['@val']} at {sample[1]['@val']}")
        # if not os.path.exists("")
        os.makedirs("Samples"+sample[1]["@val"][:sample[1]["@val"].rfind("/")], exist_ok=True)
        # copy the sample to the Samples folder
        # print(os.path.exists(os.path.join("temp", os.path.basename(sample[1]["@val"]))))
        # print(os.path.join("Samples/", Path(sample[1]["@val"][1:])), Path(sample[1]["@val"]))
        shutil.copyfile(os.path.join("temp", os.path.basename(sample[1]["@val"])),
                        os.path.join("Samples", Path(sample[1]["@val"][1:])))
        insert_sample(pack["sublab_pack"]["@name"], sample)

def insert_sample(pack_name, sample):
    conn = sqlite3.connect("SubLab.db")
    cursor = conn.cursor()
    # check if packname is in tags table
    cursor.execute(f"SELECT name FROM tags WHERE name = '{pack_name}'")
    if cursor.fetchone() is None:
        # if not, insert it
        conn.execute(f"""INSERT INTO tags (name) VALUES ("{pack_name}")""")
        conn.commit()

    # parse the xml str for the attrs
    name = sample[0]["@val"]
    local_path = sample[1]["@val"]
    hash = sample[2]["@val"]
    uuid = sample[3]["@val"]
    midiNote = sample[4]["@val"]
    tags = sample[5]["@val"]
    type = sample[6]["@val"]
    detectedPitch = sample[7]["@val"]
    primaryTag = sample[8]["@val"]
    source = sample[10]["@val"]

    # check if sample already exists with uuid
    cursor.execute(f"SELECT uuid FROM samples WHERE uuid = '{uuid}'")
    if cursor.fetchone() is not None:
        # if so, return
        print(f"Sample with uuid {uuid} already exists")
        return
    # insert the sample
    conn.execute(f"""INSERT INTO samples (name, local_path, hash, uuid, midiNote, tags, type, detectedPitch, primaryTag, source) VALUES ("{name}", "{local_path}", "{hash}", "{uuid}", "{midiNote}", "{tags}", "{type}", "{detectedPitch}", "{primaryTag}", "{source}")""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", help="The path to the pack to install")
    args = parser.parse_args()
    install_pack(args.pack)
    shutil.rmtree("temp")

"""python install.py DECAP 808s.subpack"""
