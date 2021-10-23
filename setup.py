import os
import sys
from pathlib import Path
from shutil import rmtree


# Requires 'python' in your path variables

VENV_NAME = ".venv"
BASE_DIR = "\\".join(sys.executable.split("\\")[:-1])


def create_symlink(source: str, link_name: str):
    """Create a symbolic link between two files

    Args:
        source (str): source file
        link_name (str): link name
    """
    if os.path.exists(link_name):
        os.remove(link_name)
    os.symlink(source, link_name)


def main(*args, **kwargs):
    """Main flow for setup

    Raises:
        Exception: python wasn't found in your path variables
    """
    os.system(f"python -m venv {os.path.join(BASE_DIR, VENV_NAME)}")

    if not Path(os.path.join(BASE_DIR, VENV_NAME)).exists():
        raise Exception(
            "It wasn't possible to find the virtualenv. Please verify if you have 'python' in your system path variables"
        )

    os.system(
        os.path.join(BASE_DIR, VENV_NAME, "Scripts", "activate")
        + f"&& pip install -r {os.path.join(BASE_DIR, 'usr', 'requirements', 'requirements.txt')}"
        + f"&& pip install {os.path.join(BASE_DIR, 'usr', 'requirements', 'PyOpenGL-3.1.5-cp39-cp39-win_amd64.whl')}"
        + f"&& pyinstaller {os.path.join(BASE_DIR, 'usr', 'main.py')} --onefile --paths={os.path.join(BASE_DIR, VENV_NAME, 'Lib', 'site-packages')} --paths={os.path.join(BASE_DIR, 'usr')}"
    )

    rmtree(Path(os.path.join(BASE_DIR, VENV_NAME)))

    create_symlink(
        os.path.join(BASE_DIR, "dist", "main.exe"),
        os.path.join(BASE_DIR, "OpenGL-Figures.exe"),
    )


if __name__ == "__main__":
    main()
