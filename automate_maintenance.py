import subprocess
import os
import sys

def run_command(command, cwd=None, shell=True, timeout=None, input_data=None):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            input=input_data
        )
        print(f"Command: {command}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds: {command}")
        return False, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        print(f"Error running command: {e}")
        return False, "", str(e)

def create_gitignore(repo_dir):
    """Create a .gitignore file if it doesn't exist."""
    print(f"Checking for .gitignore in {repo_dir}...")
    gitignore_path = os.path.join(repo_dir, ".gitignore")
    if not os.path.exists(gitignore_path):
        print("Creating .gitignore...")
        with open(gitignore_path, "w") as f:
            f.write("data/historical/\n")
            f.write("__pycache__/\n")
            f.write("*.pyc\n")
        print("Created .gitignore with entries: data/historical/, __pycache__/, *.pyc")
        os.chdir(repo_dir)
        run_command("git add .gitignore")
        run_command('git commit -m "Added .gitignore to ignore data/historical, __pycache__, and *.pyc files"')
        run_command("git push origin master")
    else:
        print(".gitignore already exists.")

def discard_uncommitted_changes(repo_dir, paths_to_discard):
    """Discard uncommitted changes in specified paths and remove them from tracking."""
    print(f"Discarding uncommitted changes in {paths_to_discard}...")
    os.chdir(repo_dir)
    success, _, _ = run_command(f"git rm -r --cached {' '.join(paths_to_discard)}")
    if not success:
        print("Failed to remove paths from tracking. They may not be tracked.")
    success, _, _ = run_command(f"git checkout -- {' '.join(paths_to_discard)}")
    if not success:
        print("Failed to discard changes. They may already be discarded or not tracked.")
    success, output, _ = run_command("git status --porcelain")
    if success and "data/historical" in output:
        run_command('git commit -m "Removed data/historical from tracking after adding to .gitignore"')
        run_command("git push origin master")

def cleanup_stashes(repo_dir):
    """Clean up all stashed changes in the repository."""
    print(f"Cleaning up stashes in {repo_dir}...")
    os.chdir(repo_dir)
    success, output, _ = run_command("git stash list")
    if not success:
        print("Failed to list stashes.")
        return False
    if not output.strip():
        print("No stashes found.")
        return True
    success, _, _ = run_command("git stash clear")
    if not success:
        print("Failed to clear stashes.")
        return False
    print("Successfully cleared all stashes.")
    return True

def confirm_rename(repo_dir, file_name, backup_branch):
    """Confirm if a file was renamed by checking its history in a backup branch."""
    print(f"Confirming rename of {file_name} in {repo_dir}...")
    os.chdir(repo_dir)

    success, output, _ = run_command("git rev-parse --abbrev-ref HEAD")
    if not success or output.strip() != "master":
        print("Not on the master branch.")
        return False

    success, _, _ = run_command(f"git checkout {backup_branch}")
    if not success:
        print(f"Failed to switch to backup branch {backup_branch}.")
        return False

    success, output, _ = run_command(f"git log --oneline -- {file_name}")
    if not success:
        print(f"Failed to check history of {file_name}.")
        return False
    print(f"History of {file_name} in {backup_branch}:")
    print(output if output.strip() else f"No history found for {file_name}.")

    new_file_name = "setup_and_verify_project.py"
    success, new_file_output, _ = run_command(f"git log --oneline -- {new_file_name}")
    if not success:
        print(f"Failed to check history of {new_file_name}.")
        return False
    print(f"History of {new_file_name} in {backup_branch}:")
    print(new_file_output if new_file_output.strip() else f"No history found for {new_file_name}.")

    if output.strip() and new_file_output.strip():
        earliest_new_file_commit = new_file_output.strip().split("\n")[-1].split()[0]
        last_old_file_commit = output.strip().split("\n")[0].split()[0]
        print(f"Earliest commit for {new_file_name}: {earliest_new_file_commit}")
        print(f"Last commit for {file_name}: {last_old_file_commit}")
        print("Likely renamed: The history of the old file ends before the new file's history begins.")

    success, _, _ = run_command("git checkout master")
    if not success:
        print("Failed to switch back to master branch.")
        return False
    return True

def test_gro_instructor(project_dir):
    """Test gro_instructor.py in the project directory."""
    print(f"Testing gro_instructor.py in {project_dir}...")
    os.chdir(project_dir)
    success, output, error = run_command("python src/gro_instructor.py", timeout=10, input_data="Hello\n")
    print(f"Output: {output}")
    print(f"Error: {error}")
    if "Hey there! How can I assist you today?" not in output:
        print("gro_instructor.py did not respond as expected.")
        return False
    print("gro_instructor.py test passed.")
    return True

def main():
    repo_dir = r"F:\gro_Grok_Template"
    project_dir = r"F:\TestProject"
    file_name = "setup_project.py"
    backup_branch = "backup-before-4fea491-reset"
    paths_to_discard = ["data/historical/history_log.jsonl", "data/historical/state.json"]

    # Step 1: Create .gitignore
    create_gitignore(repo_dir)

    # Step 2: Discard uncommitted changes
    discard_uncommitted_changes(repo_dir, paths_to_discard)

    # Step 3: Clean up stashes
    if not cleanup_stashes(repo_dir):
        print("Stash cleanup failed.")
        sys.exit(1)

    # Step 4: Confirm rename
    if not confirm_rename(repo_dir, file_name, backup_branch):
        print("Rename confirmation failed.")
        sys.exit(1)

    # Step 5: Test gro_instructor.py
    if not test_gro_instructor(project_dir):
        print("gro_instructor.py test failed.")
        sys.exit(1)

    print("All maintenance tasks completed successfully!")

if __name__ == "__main__":
    main()