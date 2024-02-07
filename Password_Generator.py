import tkinter as tk 
from tkinter import StringVar, IntVar
import random 
import string
import pyperclip 
import zxcvbn  


def generate_password():
    length = int(length_var.get())
    use_special_characters = special_char_var.get() == 1

    if use_special_characters:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    password = ''.join(random.choice(characters) for _ in range(length))
    password_var.set(password)
    pyperclip.copy(password)

    
    password_strength = zxcvbn.zxcvbn(password)
    strength_label.configure(text=f"Strength : {password_strength}/4")



window = tk.Tk()
window.title("Password Generator")
window.geometry("500x350")
window.resizable(False, False)
window.configure(bg="#1e3d59")


title_label = tk.Label(window, text="Password Generator", font=("Helvetica", 20, "bold"), bg="#1e3d59", fg="#ffffff")
title_label.pack(pady=10)


length_label = tk.Label(window, text="Password Length:", font=("Helvetica", 12), bg="#1e3d59", fg="#ffffff")
length_label.pack()

length_var = StringVar()
length_entry = tk.Entry(window, textvariable=length_var, font=("Helvetica", 12), width=4, bd=5)
length_entry.pack(pady=5)


special_char_var = IntVar()
special_char_checkbox = tk.Checkbutton(window, text="Include Special Characters", variable=special_char_var, font=("Helvetica", 12), bg="#1e3d59", fg="#ffffff")
special_char_checkbox.pack(pady=5)


generate_button = tk.Button(window, text="Generate Password", command=generate_password, font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", bd=5)
generate_button.pack(pady=20)


password_var = StringVar()
password_entry = tk.Entry(window, textvariable=password_var, font=("Helvetica", 16), state="readonly", readonlybackground="#ffffff", bd=5)
password_entry.pack(pady=10)


copy_button = tk.Button(window, text="Copy Password", command=lambda: pyperclip.copy(password_var.get()), font=("Helvetica", 12), bg="#2196F3", fg="#ffffff", bd=5)
copy_button.pack(pady=10)


strength_label = tk.Label(window, text="Strength: N/A", font=("Helvetica", 12), bg="#1e3d59", fg="#ffffff")
strength_label.pack(pady=5)


window.mainloop()
