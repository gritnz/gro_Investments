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

def cleanup_stashes(repo_dir):
    """Clean up all stashed changes in the repository."""
    print(f"Cleaning up stashes in {repo_dir}...")
    os.chdir(repo_dir)

    # Check if there are any stashes
    success, output, _ = run_command("git stash list")
    if not success:
        print("Failed to list stashes. Aborting.")
        return False
    if not output.strip():
        print("No stashes found. Nothing to clean up.")
        return True

    # Drop all stashes
    success, _, _ = run_command("git stash clear")
    if not success:
        print("Failed to clear stashes. Please check the error and resolve manually.")
        return False

    print("Successfully cleared all stashes.")
    return True

def main():
    repo_dir = r"F:\gro_Grok_Template"

    if not cleanup_stashes(repo_dir):
        print("Stash cleanup failed. Check the errors above and resolve them.")
        exit(1)

    print("Stash cleanup completed successfully!")

if __name__ == "__main__":
    main()