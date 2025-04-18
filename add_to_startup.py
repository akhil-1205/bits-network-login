import os
import sys
import win32com.client

def add_to_startup():
    # Get Startup folder path
    startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")

    # Get the folder where setup_startup.exe is located (i.e., the install directory)
    install_dir = os.path.dirname(sys.executable)

    # Define the path to the quick_login.exe
    target = os.path.join(install_dir, "quick_login.exe")

    # Define shortcut name and location
    shortcut_path = os.path.join(startup_folder, "BITSLogin.lnk")

    # Create the shortcut using Windows Shell
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = install_dir
    shortcut.IconLocation = target
    shortcut.save()

if __name__ == "__main__":
    add_to_startup()
