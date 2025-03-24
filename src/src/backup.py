import shutil
import os
from datetime import datetime

def backup_state_json(source_path="data/state.json", backup_dir="data/backups"):
    """Backup state.json with a timestamped filename."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/state_{timestamp}.json"
    shutil.copy2(source_path, backup_file)
    print(f"Backed up state.json to {backup_file}")
    return backup_file