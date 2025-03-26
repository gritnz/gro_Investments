# Lessons Learned

## Switching VS Code Folders with Environments
- **Date**: 2025-03-26
- **Project**: gro_Investments
- **Issue**: When switching between projects (e.g., from gro_Grok_Template to gro_Investments), I didn’t change the VS Code folder to match the active Conda environment. Since the folder structures are identical (both from the template), I worked in the wrong directory, causing confusion and a day-long debugging session.
- **Cause**: Identical folder structures made it easy to miss the mismatch between the environment and the VS Code folder.
- **Impact**: Grok went into hallucination loops and lost memory context due to mismatched state and history files.
- **Solution**: Always align the VS Code folder with the active environment:
  1. Activate the correct Conda environment (e.g., `conda activate gro_Investments`).
  2. Open the matching project folder in VS Code (e.g., `F:\gro_Investments`).
  3. Verify the Python interpreter in VS Code matches the environment.
- **Prevention**: Add a checklist for project switches to confirm folder and environment alignment.