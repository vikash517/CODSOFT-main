import tkinter as tk
from tkinter import font

def on_button_click(value):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current_text + value)

def clear_entry():
    entry.delete(0, tk.END)


def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")


window = tk.Tk()
window.title("Calculator")
window.geometry("400x550")
window.resizable(False, False)
window.configure(bg="grey")


entry_font = font.Font(family="FORTY", size=20)
entry = tk.Entry(window, width=14, font=entry_font, justify="right", bd=10, insertwidth=4, bg="#d9d9d9")
entry.grid(row=0, column=0, columnspan=4, pady=20)


buttons = [
    '9', '8', '7', '/',
    '6', '5', '4', '*',
    '3', '2', '1', '-',
    '0', '.', '=', '+'
]

row_val = 1
col_val = 0

button_font = font.Font(family="Lucida Calligraphy", size=18)


for button in buttons:
    tk.Button(window, text=button, padx=20, pady=20, font=button_font,
              command=lambda btn=button: on_button_click(btn) if btn != '=' else calculate(),
              bg="orange", bd=5).grid(row=row_val, column=col_val, sticky="nsew")
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1


tk.Button(window, text="C", padx=20, pady=20, font=button_font, command=clear_entry, bg="sky blue", bd=5).grid(row=row_val, column=col_val, sticky="nsew")

for i in range(1, 6):
    window.grid_rowconfigure(i, weight=1)
    window.grid_columnconfigure(i-1, weight=1)


window.mainloop()