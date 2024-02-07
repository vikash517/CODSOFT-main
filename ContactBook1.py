import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3

class ContactBookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Contact Book")
        self.master.geometry("400x500")
        self.master.config(bg="#CCCCFF")
        self.master.resizable(False, False)
        
        
        
        
        self.contacts = []
        self.deleted_contacts = []

        
        self.conn = sqlite3.connect('contacts.db')
        self.c = self.conn.cursor()

        
        self.c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            phone TEXT,
                            email TEXT
                            )''')
        self.conn.commit()

        self.main_frame = tk.Frame(master, bg='#40E0D0')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.name_label = tk.Label(self.main_frame, text="Name:", bg='#40E0D0', font=('Forte', 12,))
        self.name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(self.main_frame, bg='#FFFFFF', font=('arial', 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.phone_label = tk.Label(self.main_frame, text="Phone:", bg='#40E0D0', font=('Forte', 12))
        self.phone_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.phone_entry = tk.Entry(self.main_frame, bg='#FFFFFF', font=('ariel', 12))
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        self.email_label = tk.Label(self.main_frame, text="Email:", bg='#40E0D0', font=('Forte', 12))
        self.email_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(self.main_frame, bg='#FFFFFF', font=('ariel', 12))
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_button = tk.Button(self.main_frame, text="Add Contact", command=self.add_contact, bg='#4CAF50', fg='#FFFFFF', font=('Forte', 12))
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.contact_listbox = tk.Listbox(self.main_frame, width=50, bg='#F0F8FF', font=('Forte', 12), relief="sunken")
        self.contact_listbox.grid(row=4, column=0, columnspan=2, pady=10)
        self.contact_listbox.bind('<<ListboxSelect>>', self.display_selected_contact)

        self.edit_button = tk.Button(self.main_frame, text="Edit Contact", command=self.edit_contact, bg='#FFC107', fg='#FFFFFF', font=('forte', 12))
        self.edit_button.grid(row=5, column=0, pady=5)

        self.delete_button = tk.Button(self.main_frame, text="Delete Contact", command=self.delete_contact, bg='#FF5722', fg='#FFFFFF', font=('forte', 12))
        self.delete_button.grid(row=5, column=1, pady=5)

        self.restore_button = tk.Button(self.main_frame, text="Restore Contact", command=self.restore_contact, bg='#2196F3', fg='#FFFFFF', font=('forte', 11))
        self.restore_button.grid(row=6, column=0, pady=5)
        
        self.clear_button = tk.Button(self.main_frame, text="Clear Contacts", command=self.clear_contacts, bg='#9C27B0', fg='#FFFFFF', font=('forte', 12))
        self.clear_button.grid(row=6, column=1, pady=5)

        self.main_frame.pack_propagate(False)

        self.load_contacts()


    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        
        check_name = name.isalpha()
        if not check_name:
            messagebox.showerror("Error", "Please enter a valid name.")
            return
        check_phone = phone.isdigit()
        if not check_phone:
            messagebox.showerror("Error", "Please enter a valid phone number.")
            return
        phone = int(phone)
        if name and phone and email:
            contact = {"name": name, "phone": phone, "email": email}
            self.contacts.append(contact)
            self.contact_listbox.insert(tk.END, name)
            self.c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact added successfully!")
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter name, phone number, and email.")

    def clear_contacts(self):
        self.contacts = []
        self.contact_listbox.delete(0, tk.END)
        self.c.execute("DELETE FROM contacts")
        self.conn.commit()
        messagebox.showinfo("Contacts Cleared", "All contacts cleared successfully.")

    def display_selected_contact(self, event):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            contact_id = selected_index[0] + 1
            self.c.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
            contact = self.c.fetchone()
            info = f"Name: {contact[1]}\nPhone: {contact[2]}\nEmail: {contact[3]}"
            messagebox.showinfo("Selected Contact", info)

    def edit_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            selected_contact = self.contacts[selected_index[0]]
            new_name = simpledialog.askstring("Edit Contact", "Enter new name:", initialvalue=selected_contact["name"])
            new_phone = simpledialog.askstring("Edit Contact", "Enter new phone number:", initialvalue=selected_contact["phone"])
            new_email = simpledialog.askstring("Edit Contact", "Enter new email:", initialvalue=selected_contact["email"])
            if new_name and new_phone and new_email:
                contact_id = selected_index[0] + 1
                self.c.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?", (new_name, new_phone, new_email, contact_id))
                self.conn.commit()
                self.contact_listbox.delete(selected_index)
                self.contact_listbox.insert(selected_index, new_name)
                messagebox.showinfo("Success", "Contact edited successfully!")

    def delete_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            contact_id = selected_index[0] + 1
            self.c.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
            contact = self.c.fetchone()
            if contact is not None and len(contact) >= 4:
                self.deleted_contacts.append({"id": contact[0], "name": contact[1], "phone": contact[2], "email": contact[3]})
            else:
                print("Invalid contact data")
                
            self.contacts.pop(selected_index[0])
            self.contact_listbox.delete(selected_index)
            self.c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Contact deleted successfully!")
        else:
            messagebox.showwarning("No Contact Selected", "Please select a contact to delete.")

    

    def restore_contact(self):
            if self.deleted_contacts:
                contact = self.deleted_contacts.pop()
                self.contacts.append(contact)
                self.contact_listbox.insert(tk.END, contact["name"])  

                self.c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (contact["name"], contact["phone"], contact["email"]))
                self.conn.commit()
                messagebox.showinfo("Success", "Contact restored successfully.")
            else:
                messagebox.showwarning("No Contacts", "No contacts to restore.")

    def load_contacts(self):
        self.contacts = []
        self.contact_listbox.delete(0, tk.END)
        self.c.execute("SELECT * FROM contacts")
        rows = self.c.fetchall()
        for row in rows:
            self.contacts.append({"name": row[1], "phone": row[2], "email": row[3]})
            self.contact_listbox.insert(tk.END, row[1])
        
    def close_window(self):
        self.conn.close()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
