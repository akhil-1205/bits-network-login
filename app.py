import tkinter as tk
from tkinter import messagebox
import json
import os
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageTk

# === CONFIG ===
CREDENTIALS_FILE = "credentials.json"
LOGO_PATH = "logo.png"
 
# === Save & Load Credentials ===
def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump({"username": username, "password": password}, f)

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            data = json.load(f)
            return data.get("username", ""), data.get("password", "")
    return "", ""

# === Login to Website ===
def login_to_website(username, password):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://172.16.0.30:8090/httpclient.html")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.ID, "loginbutton").click()
        driver.quit()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI Handlers ===
def on_login_button_click():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Missing Input", "Please fill both fields.")
        return

    save_credentials(username, password)
    login_to_website(username, password)

def on_minimize(event):
    if root.state() == "iconic":
        hide_window()

def hide_window():
    root.withdraw()

def show_window(icon=None, item=None):
    root.after(0, root.deiconify)

def on_exit(icon=None, item=None):
    if tray_icon:
        tray_icon.stop()  # Stop the tray icon
    root.quit()  # Close the Tkinter window and stop the mainloop
    root.destroy()  # Make sure resources are freed and the window is destroyed

# === Tray Icon Actions ===
def tray_login_action(icon, item):
    username, password = load_credentials()
    if not username or not password:
        messagebox.showwarning("Missing Credentials", "No credentials found. Open the GUI to set them.")
    else:
        threading.Thread(target=login_to_website, args=(username, password), daemon=True).start()

def create_image():
    image = Image.open(LOGO_PATH).resize((64, 64)).convert("RGBA")
    return image

def run_tray_icon():
    global tray_icon
    tray_icon = Icon("LoginApp", icon=create_image(), title="Network Login",
                     menu=Menu(
                         MenuItem("Login", tray_login_action),
                         MenuItem("Show Window", show_window),
                         MenuItem("Exit", on_exit)
                     ))
    tray_icon.run()

# === GUI Setup ===
root = tk.Tk()
root.title("BITS Internet Login")
root.geometry("400x300")
root.resizable(False, False)

# App Icon
try:
    root.iconbitmap("logo.ico")
except:
    try:
        logo_img = Image.open(LOGO_PATH)
        logo_tk = ImageTk.PhotoImage(logo_img)
        root.iconphoto(True, logo_tk)
    except:
        pass

# GUI Content
frame = tk.Frame(root)
frame.pack(expand=True)

tk.Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_username = tk.Entry(frame, width=25)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_password = tk.Entry(frame, show="*", width=25)
entry_password.grid(row=1, column=1, padx=10, pady=10)

saved_user, saved_pass = load_credentials()
entry_username.insert(0, saved_user)
entry_password.insert(0, saved_pass)

tk.Button(frame, text="Login", width=20, height=2, command=on_login_button_click, bg="#4CAF50", fg="white",
          activebackground="#45A049").grid(row=2, column=0, columnspan=2, pady=20)

# Bind minimize to system tray
root.bind("<Unmap>", on_minimize)

# === Start Tray Thread ===
tray_icon = None
threading.Thread(target=run_tray_icon, daemon=True).start()

# === Mainloop ===
root.mainloop()