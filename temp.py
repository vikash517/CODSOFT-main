import tkinter as tk
from PIL import Image, ImageTk

class CustomTitleBarApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove the default title bar

        # Load the image
        self.image = Image.open("contacts.png")
        self.image = self.image.resize((16, 16))  # Adjust size as needed
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a custom title bar
        self.title_bar = tk.Frame(root, bg="blue", relief="raised", bd=2)
        self.title_bar.pack(fill="x")

        # Add a label with the image to the title bar
        self.image_label = tk.Label(self.title_bar, image=self.photo, bg="blue")
        self.image_label.pack(side="left", padx=5, pady=2)

        # Add a close button (you can add more buttons as needed)
        self.close_button = tk.Button(self.title_bar, text="X", command=self.close_window)
        self.close_button.pack(side="right", padx=5, pady=2)

        # Bind events to allow moving the window by dragging the title bar
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_move)
        self.title_bar.bind("<B1-Motion>", self.on_motion)

    def start_move(self, event):
        self.root.x = event.x
        self.root.y = event.y

    def stop_move(self, event):
        self.root.x = None
        self.root.y = None

    def on_motion(self, event):
        deltax = event.x - self.root.x
        deltay = event.y - self.root.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry("+%s+%s" % (x, y))

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomTitleBarApp(root)
    root.mainloop()
