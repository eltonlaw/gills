from sys import platform
import subprocess

user = subprocess.check_output(['whoami']).decode().strip()
if platform == "linux" or platform == "linux2":
    DEFAULT_DATA_DIR = f"/home/{user}"
elif platform == "darwin":
    DEFAULT_DATA_DIR = f"/Users/{user}"
elif platform == "win32":
    DEFAULT_DATA_DIR = None
