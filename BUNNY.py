import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random
import threading
import time
import subprocess
import sys
import os

# Your app version:
CURRENT_VERSION = "1.0.0"

# URLs for auto-update:
VERSION_URL = "https://raw.githubusercontent.com/Qav45/BUNNY/main/version.txt"
UPDATE_URL = "https://github.com/Qav45/BUNNY/releases/download/v1.0.0/BUNNY.exe"
UPDATE_FILE = "BUNNY_new.exe"

class BouncingImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("bunny :)")
        self.root.geometry("300x200")  # smaller main GUI
        self.root.configure(bg="black")

        # Make window draggable by mouse
        self._offsetx = 0
        self._offsety = 0
        self.root.bind('<Button-1>', self.click_win)
        self.root.bind('<B1-Motion>', self.drag_win)

        # Entry and button
        self.entry = tk.Entry(root, bg="#222", fg="white", insertbackground='white')
        self.entry.pack(pady=20)
        self.entry.focus()

        self.button = tk.Button(root, text="Submit", command=self.handle_submit, bg="#444", fg="white")
        self.button.pack()

        # Load image
        self.bunny_img = self.load_image("https://i.postimg.cc/PqWT6dSQ/FLDKJFLJDS.webp", (120, 120))

        # Canvas to show bunny
        self.canvas = tk.Toplevel(root)
        self.canvas.attributes('-topmost', True)
        self.canvas.overrideredirect(True)  # No window decorations
        self.canvas.configure(bg='black')
        self.screen_width = self.canvas.winfo_screenwidth()
        self.screen_height = self.canvas.winfo_screenheight()

        self.bunny_label = tk.Label(self.canvas, image=self.bunny_img, bg='black')
        self.bunny_label.pack()
        self.canvas.geometry(f"120x120+{random.randint(0, self.screen_width-120)}+{random.randint(0, self.screen_height-120)}")

        # For bouncing
        self.dx = 5
        self.dy = 5
        self.bounce()

        # Start auto-update check in background
        threading.Thread(target=self.auto_update_check, daemon=True).start()

    def click_win(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def drag_win(self, event):
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f'+{x}+{y}')

    def load_image(self, url, size):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def bounce(self):
        # Move the bunny_label around the screen
        x = self.canvas.winfo_x()
        y = self.canvas.winfo_y()

        if x + self.dx < 0 or x + self.dx + 120 > self.screen_width:
            self.dx = -self.dx
        if y + self.dy < 0 or y + self.dy + 120 > self.screen_height:
            self.dy = -self.dy

        self.canvas.geometry(f"+{x + self.dx}+{y + self.dy}")
        self.canvas.after(30, self.bounce)

    def handle_submit(self):
        text = self.entry.get().lower()
        if text == "chez":
            self.shutdown_pc()
        elif text == "evan":
            messagebox.showinfo("Info", "Evan command recognized - bouncing bunny")
            # Here you can add your special evan behavior
        elif text == "evan2":
            self.open_cmd()
        elif text == "bunny":
            self.shutdown_pc()
        elif text == "qav45":
            messagebox.showinfo("Info", "Qav45 command recognized - bouncing Optimus Prime")
            # You could add bouncing optimus prime here if you want
        else:
            messagebox.showinfo("Info", "Unknown command")

    def shutdown_pc(self):
        if messagebox.askyesno("Shutdown", "Are you sure you want to shutdown the PC?"):
            if sys.platform == "win32":
                os.system("shutdown /s /t 1")
            else:
                os.system("shutdown now")

    def open_cmd(self):
        if sys.platform == "win32":
            subprocess.Popen("cmd.exe /k echo idfk might be added in v2.0", shell=True)
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", "echo idfk might be added in v2.0"])

    def auto_update_check(self):
        try:
            r = requests.get(VERSION_URL, timeout=10)
            r.raise_for_status()
            latest_version = r.text.strip()
            print(f"Current version: {CURRENT_VERSION}, Latest version: {latest_version}")
            if latest_version > CURRENT_VERSION:
                if messagebox.askyesno("Update Available", f"A new version ({latest_version}) is available. Update now?"):
                    self.download_and_restart()
        except Exception as e:
            print(f"Auto-update check failed: {e}")

    def download_and_restart(self):
        try:
            r = requests.get(UPDATE_URL, stream=True)
            r.raise_for_status()
            with open(UPDATE_FILE, "wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)
            messagebox.showinfo("Update", "Update downloaded. Restarting...")
            subprocess.Popen([UPDATE_FILE])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download update: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingImageApp(root)
    root.mainloop()

