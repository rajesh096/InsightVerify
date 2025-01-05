import os
import subprocess
import sys
from time import sleep

base_path = os.path.dirname(os.path.abspath(__file__))
folders = [os.path.join(base_path, 'llm'), 
           os.path.join(base_path, 'ocr'), 
           os.path.join(base_path, 'poppler'),
           os.path.join(base_path)]

def create_gitignore(folder):
    gitignore_path = os.path.join(folder, '.gitignore')
    if not os.path.exists(gitignore_path):
        print(f"Creating .gitignore in {folder}")
        with open(gitignore_path, 'w') as f:
            f.write("__pycache__/\nvenv/\n")
    else:
        print(f".gitignore already exists in {folder}")

def create_virtualenv_and_install_requirements(folder):
    venv_path = os.path.join(folder, 'venv')
    requirements_path = os.path.join(folder, 'requirements.txt')

    # Ensure folder exists
    if not os.path.exists(folder):
        print(f"Error: Folder {folder} does not exist.")
        sys.exit(1)

    # Create virtual environment if it doesn't exist
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment in {venv_path}")
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
    else:
        print(f"Virtual environment already exists in {venv_path}")

    # Determine the correct pip executable path for the virtual environment
    if sys.platform == 'win32':  # Windows
        pip_executable = os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:  # Unix-like OS (Linux/macOS)
        pip_executable = os.path.join(venv_path, 'bin', 'pip')

    # Install requirements
    try:
        print(f"Installing requirements from {requirements_path}")
        process = subprocess.Popen([pip_executable, 'install', '-r', requirements_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in process.stdout:
            print(line, end='')

        process.wait()

        if process.returncode != 0:
            for line in process.stderr:
                print(line, end='')
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        sys.exit(1)

for folder in folders:
    print(f"Processing folder: {folder}")
    create_gitignore(folder)
    create_virtualenv_and_install_requirements(folder)
    print("\n\n")
    sleep(2)

# Create .gitignore in the base directory
create_gitignore(base_path)

print("\n\nSetup completed successfully.")

# Instructions to be displayed in the popup
instructions = """
Setup Script Instructions:

This script sets up the development environment for the project by performing the following tasks:
1. Creates a `.gitignore` file in specified folders if it doesn't already exist.
2. Creates a virtual environment in each specified folder if it doesn't already exist.
3. Installs the required Python packages from `requirements.txt` in each virtual environment.

Folders processed:
- llm
- ocr
- poppler

Instructions:
1. Installing Ollama and Running Gemma2:9b Model:
    - Download Ollama from the official website: https://ollama.com/download
    - Follow the installation instructions provided on the website.
    - To run the Gemma2:9b model, use the following command: ollama run gemma2:9b

2. Installing Poppler:
    - Download Poppler from the official website: https://poppler.freedesktop.org/bin` folder of Poppler.
    - Follow the installation instructions provided on the website.
    - After installation, set the environment path to include the `bin` folder of Poppler.
    - To get the path of the `bin` folder, use the following command: dftotext
    - Add the path to your system's environment variables. the path to your system's environment variables.
"""
# Show the instructions in a popup window
print(instructions)