import requests
import psutil
import time
import threading
import tkinter as tk
from tkinter import messagebox
import platform

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Checker and Chrome Closer")
        self.root.geometry("300x200")  # Set window size
        self.running = False

        self.start_button = tk.Button(root, text="Start", command=self.start, width=15, height=2)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop, state=tk.DISABLED, width=15, height=2)
        self.stop_button.pack(pady=20)

        self.status_label = tk.Label(root, text="Status: Stopped", font=("Helvetica", 12))
        self.status_label.pack(pady=20)

    def get_ip_address(self):
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            response.raise_for_status()
            ip = response.json()['ip']
            print(f"Retrieved IP address: {ip}")
            return ip
        except requests.exceptions.RequestException as e:
            print(f"Error getting IP address: {e}")
            return None

    def get_geolocation(self, ip):
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            response.raise_for_status()
            geo_info = response.json()
            print(f"Geolocation info: {geo_info}")
            return geo_info
        except requests.exceptions.RequestException as e:
            print(f"Error getting geolocation: {e}")
            return None

    def is_chrome_running(self):
        chrome_process_names = {
            'Windows': ['chrome.exe', 'Google Chrome'],
            'Linux': ['chrome', 'chrome-browser', 'google-chrome'],
            'Darwin': ['Google Chrome']
        }
        current_os = platform.system()
        try:
            for process in psutil.process_iter(['name']):
                process_name = process.info.get('name')
                if process_name:
                    print(f"Checking process: {process_name}")
                    if process_name in chrome_process_names.get(current_os, []):
                        print(f"Found Chrome process: {process_name}")
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Error accessing process information: {e}")
        return False

    def close_chrome(self):
        chrome_process_names = {
            'Windows': ['chrome.exe', 'Google Chrome'],
            'Linux': ['chrome', 'chrome-browser', 'google-chrome'],
            'Darwin': ['Google Chrome']
        }
        current_os = platform.system()
        try:
            for process in psutil.process_iter(['name', 'pid']):
                process_name = process.info.get('name')
                if process_name and process_name in chrome_process_names.get(current_os, []):
                    pid = process.info.get('pid')
                    if pid:
                        try:
                            print(f"Attempting to terminate process: {process_name} with PID {pid}")
                            proc = psutil.Process(pid)
                            proc.terminate()
                            try:
                                proc.wait(timeout=5)  # Ensure process is terminated
                            except psutil.TimeoutExpired:
                                print(f"Timeout expired while waiting for process {process_name} with PID {pid} to terminate.")
                                proc.kill()
                                proc.wait(timeout=5)
                            if not proc.is_running():
                                print(f"Terminated process {process_name} with PID {pid}")
                            else:
                                print(f"Failed to terminate process {process_name} with PID {pid}")
                        except psutil.NoSuchProcess:
                            print(f"Process {process_name} with PID {pid} no longer exists")
                        except psutil.AccessDenied:
                            print(f"Access denied when trying to terminate process {process_name} with PID {pid}")
                        except Exception as e:
                            print(f"Error terminating process {process_name} with PID {pid}: {e}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Error accessing process information: {e}")

    def check_ip(self):
        while self.running:
            print("Checking IP address...")
            ip = self.get_ip_address()
            if ip:
                print("Checking geolocation...")
                geo_info = self.get_geolocation(ip)
                if geo_info and geo_info.get('country') in ['Iran']:
                    print(f"IP is from {geo_info.get('country')}. Checking if Google Chrome is running.")
                    if self.is_chrome_running():
                        print("Google Chrome is running. Closing Google Chrome.")
                        self.close_chrome()
                    else:
                        print("Google Chrome is not running. No action taken.")
                else:
                    print(f"IP is from {geo_info.get('country') if geo_info else 'Unknown'}. No action taken.")
            else:
                print("Failed to retrieve IP address. Check your internet connection.")
            
            time.sleep(10)
        
    def start(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Running")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.thread = threading.Thread(target=self.check_ip)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Stopped")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.thread.join()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
