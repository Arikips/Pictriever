import tkinter as tk
import pyperclip
import keyboard
import threading
import time
from PIL import ImageGrab
from google_lens import GoogleLens
from settings import Settings

class ScreenCaptureApp:
    def __init__(self):
        self.settings = Settings()
        self.hotkeys = self.settings.hotkeys
        self.lastText = "qweerwsasfafqw"
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selection_mode = False
        self.auto_scan_mode = False
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main tkinter window
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray", highlightthickness=0)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.lens = GoogleLens()

        keyboard.add_hotkey(self.hotkeys['select_area'], self.start_selection)
        keyboard.add_hotkey(self.hotkeys['scan_area'], self.scan_area)
        keyboard.add_hotkey(self.hotkeys['terminate_app'], self.terminate_app)
        keyboard.add_hotkey(self.hotkeys['toggle_auto_scan'], self.toggle_auto_scan)

        self.display_welcome_message()

    def display_welcome_message(self):
        print("Welcome to Pictriever")
        print("Available hotkeys:")
        print(f"--select area ({self.hotkeys['select_area']})")
        print(f"--scan area ({self.hotkeys['scan_area']})")
        print(f"--toggle autoscan ({self.hotkeys['toggle_auto_scan']})")
        print(f"--terminate app ({self.hotkeys['terminate_app']})")

    def start_selection(self):
        self.selection_mode = True
        self.root.deiconify()
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.3)  # Make the window transparent
        self.canvas.delete("all")  # Clear previous selection boxes

    def on_button_press(self, event):
        if self.selection_mode:
            self.start_x = event.x
            self.start_y = event.y
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        if self.selection_mode and self.rect:
            cur_x, cur_y = (event.x, event.y)
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        if self.selection_mode:
            self.end_x, self.end_y = (event.x, event.y)
            self.selection_mode = False
            self.root.withdraw()

    def scan_area(self):
        print("Scanning...")
        if all(v is not None for v in [self.start_x, self.start_y, self.end_x, self.end_y]):
            x1, y1, x2, y2 = min(self.start_x, self.end_x), min(self.start_y, self.end_y), max(self.start_x, self.end_x), max(self.start_y, self.end_y)
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            success, result, time_taken = self.lens(screenshot)
            if success:
                text = self.getUnique(self.lastText, result)
                pyperclip.copy(text)
                print(f"Retrieved text:\n{text}")
                print(f"Text was successfully retrieved. Time taken: {time_taken:.2f} seconds")
                self.lastText += text
            else:
                print(f"Failed to retrieve text: {result}")

    def toggle_auto_scan(self):
        self.auto_scan_mode = not self.auto_scan_mode
        if self.auto_scan_mode:
            print("Auto-scan mode enabled")
            self.start_auto_scan()
        else:
            print("Auto-scan mode disabled")

    def start_auto_scan(self):
        def auto_scan():
            while self.auto_scan_mode:
                self.scan_area()
                time.sleep(self.settings.auto_scan_interval)

        threading.Thread(target=auto_scan, daemon=True).start()

    def terminate_app(self):
        print("Terminating the application...")
        self.root.quit()
        self.root.destroy()

    def getUnique(self, str1, str2):
        # Find the common prefix of the two strings
        min_length = min(len(str1), len(str2))
        common_prefix_length = 0

        for i in range(min_length):
            if str1[i] == str2[i]:
                common_prefix_length += 1
            else:
                break

    # The unique segment of the second string
        unique_segment = str2[common_prefix_length:].strip()
        return unique_segment

if __name__ == "__main__":
    app = ScreenCaptureApp()
    tk.mainloop()
