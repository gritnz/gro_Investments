import os
import json

def update_gro_instructor():
    """Update gro_instructor.py to use template_data/ for state and history files."""
    file_path = os.path.join("src", "gro_instructor.py")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the file paths
    content = content.replace(
        'self.state_file = os.path.join(project_dir, "data", "historical", "state.json")',
        'self.state_file = os.path.join(project_dir, "template_data", "state.json")'
    )
    content = content.replace(
        'self.log_file = os.path.join(project_dir, "data", "historical", "history_log.jsonl")',
        'self.log_file = os.path.join(project_dir, "template_data", "history_log.jsonl")'
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {file_path} to use template_data/ for state and history files.")

def update_gitignore():
    """Ensure .gitignore includes __pycache__/ and data/historical/."""
    gitignore_path = ".gitignore"
    required_entries = ["__pycache__/", "data/historical/*", "!data/historical/state.json", "!data/historical/history_log.jsonl"]

    # Read existing .gitignore
    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read().splitlines()
    except FileNotFoundError:
        content = []

    # Add missing entries
    updated = False
    for entry in required_entries:
        if entry not in content:
            content.append(entry)
            updated = True

    if updated:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content) + "\n")
        print(f"Updated {gitignore_path} with required entries.")
    else:
        print(f"{gitignore_path} already up to date.")

def update_state_json():
    """Update state.json with the project name based on the current directory."""
    state_file = os.path.join("template_data", "state.json")
    if not os.path.exists(state_file):
        print(f"Error: {state_file} not found.")
        return

    # Get the project name from the current directory
    project_name = os.path.basename(os.getcwd())

    # Read the state.json file
    with open(state_file, "r", encoding="utf-8") as f:
        state_data = json.load(f)

    # Replace <project-name> with the actual project name
    state_data["history"][0]["input"] = f"Setup initialized for project {project_name}"
    state_data["wip"]["notes"] = f"User has cloned the repository ({project_name}) and opened the project in VS Code."
    state_data["latest_input"] = f"Setup initialized for project {project_name}"
    state_data["setup_context"]["project_name"] = project_name
    state_data["setup_context"]["greeting"] = f"Hi, welcome to setting up ‘{project_name}’! I’m your wise-cracking assistant, how can I help today?"

    # Write the updated state back to the file
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state_data, f, indent=4)
    print(f"Updated {state_file} with project name: {project_name}")

if __name__ == "__main__":
    print("Setting up project...")
    update_gro_instructor()
    update_gitignore()
    update_state_json()
    print("Setup complete. Follow the remaining steps in SETUP.md.")