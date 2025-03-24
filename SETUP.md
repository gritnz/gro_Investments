# gro_Grok_Template Setup
1. **Clone Repository**
   - `git clone https://github.com/gritnz/gro_Grok_Template.git <project-name>`
   - `cd <project-name>`
2. **Set Up Environment**
   - `conda create -n <env-name> python=3.11 && conda activate <env-name>`
3. **Initialize Data**
   - `xcopy template_data data\historical /E /H /C /I`
4. **Run Template**
   - `python src/gro_instructor.py`
   - Test with: "Hello #e5"
