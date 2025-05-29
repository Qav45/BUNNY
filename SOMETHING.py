import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import ctypes
import threading
import time
import os
import subprocess

# URLs
BUNNY_URL = "https://i.postimg.cc/PqWT6dSQ/FLDKJFLJDS.webp"
OPTIMUS_URL = "https://upload.wikimedia.org/wikipedia/en/1/19/Optimus_Prime_cgi.png"

# Load image from URL and resize
def load_image(url, size):
    response = requests.get(url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    return img.resize(size)

# Floating image that bounces on screen
class FloatingImage:
    def __init__(self, image_url, size=(150, 150)):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.configure(bg='white')

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        img = load_image(image_url, size)
        self.tk_img = ImageTk.PhotoImage(img)

        self.label = tk.Label(self.root, image=self.tk_img, bg='white')
        self.label.pack()

        self.x, self.y = 100, 100
        self.dx, self.dy = 5, 5

        self.animate()

    def animate(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x + self.tk_img.width() >= self.screen_width:
            self.dx *= -1
        if self.y <= 0 or self.y + self.tk_img.height() >= self.screen_height:
            self.dy *= -1

        self.root.geometry(f"+{self.x}+{self.y}")
        self.root.after(20, self.animate)

# Main GUI application
class BouncingImageApp:
    def __init__(self, master):
        self.master = master
        master.title("bunny :)")
        master.geometry("200x100")
        master.configure(bg="black")
        master.resizable(False, False)
        master.wm_attributes("-topmost", True)

        # Dark title bar (Windows only)
        try:
            HWND = ctypes.windll.user32.GetParent(master.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            ctypes.windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(1)), 4)
        except:
            pass

        # Move window support
        master.bind("<Button-1>", self.start_move)
        master.bind("<B1-Motion>", self.do_move)

        style = ttk.Style(master)
        style.theme_use("default")
        style.configure("TLabel", foreground="white", background="black")
        style.configure("TEntry", fieldbackground="black", foreground="white")

        self.label = ttk.Label(master, text="Enter command:")
        self.label.pack(pady=5)

        self.entry = ttk.Entry(master)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.handle_input)

        self.floating_images = []

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.master.winfo_x() + (event.x - self._x)
        y = self.master.winfo_y() + (event.y - self._y)
        self.master.geometry(f"+{x}+{y}")

    def handle_input(self, event):
        command = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if command == "bunny":
            os.system("shutdown /s /t 1")
        elif command == "evan2":
            subprocess.Popen("cmd /c echo idfk might be added in v2.0", shell=True)
        elif command in ["evan", "evan1"]:
            self.spawn_image(BUNNY_URL, size=(150, 150))
        elif command == "qav45":
            self.spawn_image(OPTIMUS_URL, size=(200, 200))

    def spawn_image(self, url, size=(150, 150)):
        img = FloatingImage(url, size)
        self.floating_images.append(img)

if __name__ == "__main__":
    root = tk.Tk()
    app = BouncingImageApp(root)
    root.mainloop()
