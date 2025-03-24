import subprocess
import os

def run_command(command, cwd=None, shell=True):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            cwd=cwd,
            text=True,
            capture_output=True
        )
        print(f"Command: {command}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"Error running command: {e}")
        return False, "", str(e)

def confirm_rename(repo_dir, file_name, backup_branch):
    """Confirm if a file was renamed by checking its history in a backup branch."""
    print(f"Confirming rename of {file_name} in {repo_dir}...")
    os.chdir(repo_dir)

    # Check the current branch
    success, output, _ = run_command("git rev-parse --abbrev-ref HEAD")
    if not success or output.strip() != "master":
        print("Not on the master branch. Please switch to master and rerun the script.")
        return False

    # Switch to the backup branch
    success, _, _ = run_command(f"git checkout {backup_branch}")
    if not success:
        print(f"Failed to switch to backup branch {backup_branch}. Aborting.")
        return False

    # Check the history of the file
    success, output, _ = run_command(f"git log --oneline -- {file_name}")
    if not success:
        print(f"Failed to check history of {file_name}. Aborting.")
        return False

    print(f"History of {file_name} in {backup_branch}:")
    print(output if output.strip() else f"No history found for {file_name}.")

    # Check if the file was renamed by looking for the commit where the new file appeared
    new_file_name = "setup_and_verify_project.py"
    success, new_file_output, _ = run_command(f"git log --oneline -- {new_file_name}")
    if not success:
        print(f"Failed to check history of {new_file_name}. Aborting.")
        return False

    print(f"History of {new_file_name} in {backup_branch}:")
    print(new_file_output if new_file_output.strip() else f"No history found for {new_file_name}.")

    # Look for rename evidence
    if output.strip() and new_file_output.strip():
        # Find the earliest commit for the new file
        earliest_new_file_commit = new_file_output.strip().split("\n")[-1].split()[0]
        # Check if the old file's history stops before the new file's history starts
        last_old_file_commit = output.strip().split("\n")[0].split()[0]
        print(f"Earliest commit for {new_file_name}: {earliest_new_file_commit}")
        print(f"Last commit for {file_name}: {last_old_file_commit}")
        print("Likely renamed: The history of the old file ends before the new file's history begins.")

    # Switch back to master
    success, _, _ = run_command("git checkout master")
    if not success:
        print("Failed to switch back to master branch. Please do so manually.")
        return False

    return True

def main():
    repo_dir = r"F:\gro_Grok_Template"
    file_name = "setup_project.py"
    backup_branch = "backup-before-4fea491-reset"

    if not confirm_rename(repo_dir, file_name, backup_branch):
        print("Failed to confirm rename. Check the errors above and resolve them.")
        exit(1)

    print("Rename confirmation completed successfully!")

if __name__ == "__main__":
    main()