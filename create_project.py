import os
import subprocess
import sys
import shutil
import stat

def run_command(command, cwd=None, shell=True):
    result = subprocess.run(command, cwd=cwd, shell=shell, text=True, capture_output=True)
    print(f"Running: {command}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with return code {result.returncode}")
    return True

def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def create_project(project_name, project_dir, github_username, python_version="3.11.11"):
    # Step 1: Clone the new repository
    repo_url = f"https://github.com/{github_username}/{project_name}.git"
    if os.path.exists(project_dir):
        print(f"Directory {project_dir} already exists. Attempting to remove it...")
        try:
            shutil.rmtree(project_dir, onerror=remove_readonly)
        except Exception as e:
            print(f"Failed to remove directory {project_dir}: {e}")
            print("Please manually delete the directory and try again.")
            print("You can use: rmdir /s /q " + project_dir)
            print("If that fails, try running the command prompt as Administrator or rebooting your system.")
            sys.exit(1)

    print(f"Cloning {repo_url} to {project_dir}...")
    try:
        run_command(f"git clone {repo_url} {project_dir}")
    except RuntimeError as e:
        print(f"Failed to clone repository: {e}")
        sys.exit(1)

    # Step 2: Create Conda environment
    env_name = f"{project_name.lower()}_env"
    print(f"Creating Conda environment {env_name} with Python {python_version}...")
    try:
        run_command(f"conda create -n {env_name} python={python_version} -y")
    except RuntimeError as e:
        print(f"Failed to create Conda environment: {e}")
        sys.exit(1)

    # Step 3: Activate environment and run setup
    print("Activating environment and running setup...")
    setup_script = os.path.join(project_dir, "setup_and_verify_project.py")
    if not os.path.exists(setup_script):
        print(f"Setup script {setup_script} not found.")
        sys.exit(1)
    activate_cmd = f"conda activate {env_name} && python setup_and_verify_project.py {project_dir}"
    try:
        run_command(activate_cmd, cwd=project_dir)
    except RuntimeError as e:
        print(f"Failed to run setup script: {e}")
        sys.exit(1)

    print(f"Project {project_name} set up successfully at {project_dir}!")
    print(f"To start working, run:")
    print(f"cd {project_dir}")
    print(f"conda activate {env_name}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_project.py <project_name> <project_dir> <github_username>")
        sys.exit(1)
    project_name, project_dir, github_username = sys.argv[1], sys.argv[2], sys.argv[3]
    create_project(project_name, project_dir, github_username)