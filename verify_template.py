import os
import json
import subprocess

# Base directory
BASE_DIR = "F:/gro_Grok_Template"
TEMPLATE_DIR = os.path.join(BASE_DIR, "template_data")

def check_tidy():
    """Step 1: Check for redundant files."""
    print("Step 1: Checking for redundant files...")
    files_to_check = ["dir_output.txt", "requirements.txt"]
    for f in files_to_check:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            print(f" - {f} EXISTS (should it be deleted?)")
        else:
            print(f" - {f} not found (already tidied or never existed)")
    print("Expect: If 'EXISTS', rerun solidify_template.py to delete.")

def check_state_files():
    """Step 2: Verify state.json and history_log.jsonl."""
    print("\nStep 2: Checking state files...")
    state_file = os.path.join(TEMPLATE_DIR, "state.json")
    history_file = os.path.join(TEMPLATE_DIR, "history_log.jsonl")

    # Check state.json
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            content = json.load(f)
        expected = {
            "chat_summaries": [],
            "wip": {"current_task": "", "notes": ""},
            "related_data": {"prompts": "docs/prompts.md"},
            "history": [],
            "input_count": 0
        }
        print(f" - {state_file} contents:", json.dumps(content, indent=2))
        if content == expected:
            print("   Matches expected template—GOOD")
        else:
            print("   Differs from expected—check if intentional")
    else:
        print(f" - {state_file} missing—ERROR")

    # Check history_log.jsonl
    if os.path.exists(history_file):
        size = os.path.getsize(history_file)
        print(f" - {history_file} size: {size} bytes")
        if size == 0:
            print("   Empty as expected—GOOD")
        else:
            print("   Not empty—check contents")
    else:
        print(f" - {history_file} missing—ERROR")
    print("Expect: state.json matches template, history_log.jsonl is 0 bytes.")

def check_setup_md():
    """Step 3: Verify SETUP.md contents."""
    print("\nStep 3: Checking SETUP.md...")
    setup_file = os.path.join(BASE_DIR, "SETUP.md")
    if os.path.exists(setup_file):
        with open(setup_file, "r") as f:
            content = f.read()
        print(f" - {setup_file} contents:\n{content}")
        if "gro_Grok_Template" in content and "git clone" in content:
            print("   Looks like your original—UNCHANGED due to bug")
        else:
            print("   Unexpected content—check if updated manually")
    else:
        print(f" - {setup_file} missing—ERROR")
    print("Expect: Matches your original SETUP.md from last output.")

def check_git_status():
    """Step 4: Check Git status."""
    print("\nStep 4: Checking Git status...")
    try:
        result = subprocess.run(["git", "status"], cwd=BASE_DIR, capture_output=True, text=True)
        print(f" - Git status:\n{result.stdout}")
        if "Your branch is up to date" in result.stdout:
            print("   Up to date—GOOD")
        elif "nothing to commit" in result.stdout:
            print("   No changes pending—GOOD")
        else:
            print("   Changes pending—review output")
    except subprocess.CalledProcessError as e:
        print(f" - Git error: {e}")
    print("Expect: 'up to date' or 'nothing to commit' if last push worked.")

def main():
    print("Verifying gro_Grok_template - Phase 1 State")
    check_tidy()
    check_state_files()
    check_setup_md()
    check_git_status()
    print("\nNext: Rerun solidify_template.py with fixes if needed.")

if __name__ == "__main__":
    main()
    