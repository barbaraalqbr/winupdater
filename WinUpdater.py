import os
import subprocess
import ctypes
from datetime import datetime

class WinUpdater:
    def __init__(self):
        self.update_command = "powershell.exe -Command \"& {Start-Process -FilePath 'powershell.exe' -ArgumentList '-Command Install-WindowsUpdate -AcceptAll -AutoReboot' -Verb RunAs}\""

    def check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def check_for_updates(self):
        print("Checking for updates...")
        result = subprocess.run(["powershell", "Get-WindowsUpdate"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Updates available:")
            print(result.stdout)
        else:
            print("Failed to check for updates.")
            print(result.stderr)

    def install_updates(self):
        print("Installing updates...")
        if self.check_admin():
            try:
                os.system(self.update_command)
            except Exception as e:
                print(f"Failed to install updates: {e}")
        else:
            print("Administrator privileges are required to install updates.")

    def log_update_check(self):
        with open("update_log.txt", "a") as log_file:
            log_file.write(f"Checked for updates on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    updater = WinUpdater()
    updater.log_update_check()
    updater.check_for_updates()
    user_input = input("Do you want to install updates? (yes/no): ").strip().lower()
    if user_input == "yes":
        updater.install_updates()