import csv
import shutil
import sys
import time
from pathlib import Path

from hash_all import hash_all
sequence='0'

# [backup]
def backup(source_dir, backup_dir):
    global sequence
    manifest = hash_all(source_dir)
    sequence = str((int(sequence))+1)
    
    write_manifest(backup_dir, sequence, manifest)
    copy_files(source_dir, backup_dir, manifest)
    return manifest
# [/backup]

# [copy]
def copy_files(source_dir, backup_dir, manifest):
    for (filename, hash_code) in manifest:
        source_path = Path(source_dir, filename)
        backup_path = Path(backup_dir, f"{hash_code}.bck")
        if not backup_path.exists():
            shutil.copy(source_path, backup_path)
# [/copy]

# [time]
def current_time():
    return f"{time.time()}".split(".")[0]
# [/time]

# [write]
def write_manifest(backup_dir, sequence, manifest):
    while len(sequence)<9:
        sequence="0"+sequence
    print(sequence)
    backup_dir = Path(backup_dir)
    if not backup_dir.exists():
        backup_dir.mkdir()
    manifest_file = Path(backup_dir, f"{sequence}.csv")
    with open(manifest_file, "w") as raw:
        writer = csv.writer(raw)
        writer.writerow(["filename", "hash"])
        writer.writerows(manifest)
# [/write]

if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: backup.py source_dir backup_dir"
    backup(sys.argv[1], sys.argv[2])
