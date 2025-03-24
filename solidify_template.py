import os
import shutil
import json
from datetime import datetime

# Base directory
BASE_DIR = "F:/gro_Grok_Template"
TEMPLATE_DIR = os.path.join(BASE_DIR, "template_data")
DATA_DIR = os.path.join(BASE_DIR, "data", "historical")
NOTES_FILE = os.path.join(BASE_DIR, "notes.md")

def check_and_tidy():
    """Step 1: Tidy up with verification."""
    print("Checking for files to tidy...")
    files = os.listdir(BASE_DIR)
    potential_deletes = [f for f in files if f.startswith("statebk") or f.endswith((".log", ".txt"))]
    if not potential_deletes:
        print("No redundant files found.")
        return True

    print("Potential files to delete:")
    for f in potential_deletes:
        print(f" - {f}")
    confirm = input("Delete these files? (yes/no): ").strip().lower()
    if confirm == "yes":
        for f in potential_deletes:
            path = os.path.join(BASE_DIR, f)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            print(f"Deleted {f}")
        return True
    else:
        print("No files deleted—skipping tidy step.")
        return False

def finalize_state_json():
    """Step 2: Finalize state.json template."""
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    state_file = os.path.join(TEMPLATE_DIR, "state.json")
    template = {
        "chat_summaries": [],
        "wip": {"current_task": "", "notes": ""},
        "related_data": {"prompts": "docs/prompts.md"},
        "history": [],
        "input_count": 0
    }
    
    # Check existing state.json
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            current = json.load(f)
        print("Current state.json:", json.dumps(current, indent=2))
        confirm = input("Replace with clean template? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Keeping existing state.json.")
            return False

    with open(state_file, "w") as f:
        json.dump(template, f, indent=2)
    print(f"Created/updated {state_file}")

    # Empty history_log.jsonl
    history_file = os.path.join(TEMPLATE_DIR, "history_log.jsonl")
    open(history_file, "w").close()
    print(f"Created/updated empty {history_file}")
    return True

def polish_setup_md():
    """Step 3: Polish SETUP.md."""
    setup_file = os.path.join(BASE_DIR, "SETUP.md")
    content = """# gro_Grok_Template Setup
1. **Clone Repository**
   - `git clone https://github.com/gritnz/gro_Grok_Template.git <project-name>`
   - `cd <project-name>`
2. **Set Up Environment**
   - `conda create -n <env-name> python=3.11 && conda activate <env-name>`
3. **Initialize Data**
   - `xcopy template_data data\\historical /E /H /C /I`
4. **Run Template**
   - `python src/gro_instructor.py`
   - Test with: "Hello #e5"
"""
    # Check existing SETUP.md
    if os.path.exists(setup_file):
        with open(setup_file, "r") as f:
            current = f.read()
        print("Current SETUP.md:\n", current)
        confirm = input("Replace with updated version? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Keeping existing SETUP.md.")
            return False

    with open(setup_file, "w") as f:
        f.write(content)
    print(f"Updated {setup_file}")
    return True

def log_progress(steps_completed):
    """Log actions to notes.md."""
    with open(NOTES_FILE, "a") as f:
        f.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Phase 1 Progress\n")
        for step, success in steps_completed.items():
            f.write(f"- {step}: {'Completed' if success else 'Skipped'}\n")
    print(f"Logged progress to {NOTES_FILE}")

def main():
    print("Solidifying gro_Grok_template - Phase 1")
    steps_completed = {}

    # Step 1: Tidy Up
    steps_completed["Tidy Up"] = check_and_tidy()

    # Step 2: Finalize state.json
    steps_completed["Finalize state.json"] = finalize_state_json()

    # Step 3: Polish SETUP.md
    steps_completed["Polish SETUP.md"] = polish_setup_md()

    # Log results
    log_progress(steps_completed)

    # Suggest Git commit
    print("\nNext: Commit changes to Git?")
    confirm = input("(yes/no): ").strip().lower()
    if confirm == "yes":
        subprocess.run(["git", "add", "."], cwd=BASE_DIR)
        subprocess.run(["git", "commit", "-m", "Phase 1: Solidified core template"], cwd=BASE_DIR)
        subprocess.run(["git", "push", "origin", "master"], cwd=BASE_DIR)
        print("Changes committed and pushed.")

if __name__ == "__main__":
    import subprocess
    main()