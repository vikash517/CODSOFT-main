import tkinter as tk
from tkinter import ttk #importing ttk module from the tkinter library
from tkinter import messagebox
import sqlite3 as sql # importing sqlite3 module

#defining an empty list
tasks = []

#defining a function to add tasks into list
def add_task():
    task_string = task_field.get()
    if len(task_string)==0:
        messagebox.showinfo("Error", "Task box is Empty")
    else:
        tasks.append(task_string) #adding tasks to task list
        #using execute() statement to execute a sql statement
        the_cursor.execute('insert into tasks values(?)',(task_string,))
        list_update()
        task_field.delete(0,"end")

def delete_task():
    try:
        index = task_listbox.curselection()[0]
        task, completed = tasks[index]
        if task in [t[0] for t in tasks]:
            tasks.pop(index)
            list_update()
            the_cursor.execute("delete from tasks where title = ?", (task,))
    except IndexError:
        messagebox.showinfo("Error", "Please select a task to delete")

def mark_task_as_completed():
    try:
        index = task_listbox.curselection()[0]
        task_tuple = tasks[index]
        task, completed = task_tuple[0], task_tuple[1] if len(task_tuple) > 1 else 0
        if not completed:
            tasks[index] = (task, 1)  # Mark task as completed
            the_cursor.execute("update tasks set completed = 1 where title = ?", (task,))
            list_update()
            update_completed_list()
            messagebox.showinfo("Task Completed" , f"task {task} has been marked as completed.")
    except IndexError:
        messagebox.warning("Error", "Please select a task to mark as completed")

def update_completed_list():
    completed_tasks.clear()
    for task, completed in tasks:
        if completed:
            completed_tasks.append((task, completed))
    completed_listbox.delete(0, "end")
    for task, completed in completed_tasks:
        completed_listbox.insert("end", f"[Completed] {task}")


#defining function to update new tasks in the list
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert("end",task) #using insert method to insert task into the list

#defining a function to delete tasks form the list
def delete_task():
    #suing try-except method
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            #using execute() method to execute a sql statement
            the_cursor.execute("delete form tasks where title = ?", (the_value))

    except:
        messagebox.showinfo("Error" , "Please select a task to delete")

#defining a function to delete all tasks form the list

def delete_all_tasks():
    message_box = messagebox.askyesno("Delete All", "Are you Sure?" )

    if message_box==True:
        while(len(tasks)!=0):
            tasks.pop()
        the_cursor.execute("delete from tasks")

        list_update()

#defining a function to clear the list

def clear_list():
    task_listbox.delete(0,"end")

#defining a function to close the application

def close():
    print(tasks)

    guiWindow.destroy()

#defining a function to restore data from the database

def restore_database():
    #iterating elements in the list
    while(len(tasks)!=0):
        #pop method to pop elements form the list
        tasks.pop()
        #iterrating through the rows in the database table
    for row in the_cursor.execute("select title from tasks"):
        tasks.append(row[0])


#---------->MAIN FUNCTION<-----------

if __name__ == "__main__":
    guiWindow = tk.Tk()
    #title for the window
    guiWindow.title("To-DO list -- Codesoft")
    guiWindow.geometry("500x500")
    guiWindow.resizable(False,False)
    guiWindow.configure(bg = "#E6E6FA")


    #using connect method too connect to the database
    the_connection = sql.connect('listOfTasks.db')  
# creating an object of the cursor class  
    the_cursor = the_connection.cursor()  
# using the execute() method to execute a SQL statement  
    the_cursor.execute('create table if not exists tasks (title text)')  
    
    #defining frames 

    header_frame = tk.Frame(guiWindow, bg = "#2F4F4F")
    header_frame.pack(fill = "both")
    function_frame = tk.Frame(guiWindow, bg = "#BC8F8F" )
    function_frame.pack(side = "left", expand = True, fill = "both")
    listbox_frame = tk.Frame(guiWindow, bg = "#00FFFF")
    listbox_frame.pack(side = "right", expand = True, fill = "both")

    #defining label using ttk.label() widget
    header_label = ttk.Label(
        header_frame, text = "To-Do List",
        font=("Algerian", 40),
        background = "#FAEBD7",
        foreground = "#8B4513"
    )
    header_label.pack(padx = 20, pady = 20)

    task_label = ttk.Label(
        function_frame,
        text = "Enter Tasks:",
        font = ("Ariel","12","bold"),
        background = "#FAEBD7",  
        foreground = "#000000"  
    )
    task_label.place(x = 30 , y = 40)

#defining entry field
    task_field = ttk.Entry(
        function_frame,
        font = ("Ariel","12"),
        width = 18,
        
        background = "#FFF8DC",
        foreground = "#A52A2A" 

    )

    task_field.place(x = 30, y = 80)


    #defining buttons
    add_button = ttk.Button(
        function_frame,
        text = "Add Text",
        width  = 24,
        command = add_task
    )
    add_button.place(x = 30, y = 120)

    del_button = ttk.Button(
        function_frame,
        text = "Delete Task",
        width = 24,
        command = delete_task
    )
    del_button.place(x=30, y= 160)

    mark_completed_button = ttk.Button(
        function_frame,
        text = "Mark Completed",
        width = 24,
        command = mark_task_as_completed
    )

    mark_completed_button.place(x=30, y=200)
    
    del_all_button = ttk.Button(
        function_frame,
        text = "Delete All Tasks",
        width = 24,
        command = delete_all_tasks
    )
    del_all_button.place(x=30, y=240)

    exit_button = ttk.Button(
        function_frame,
        text = "Exit",
        width = 24,
        command = close
    )
    exit_button.place(x=30, y=280)


    #defining list box
    task_listbox = tk.Listbox(
        listbox_frame,
        width = 37,
        height = 21,
        selectmode = "SINGLE",
        bg = "#FFFFFF", 
        fg =  "#000000", 
        selectbackground = "#CD853F",
        selectforeground = "#FFFFFF"
    )

    task_listbox.place(x=10,y=20)


    restore_database()
    list_update()


    guiWindow.mainloop()
    
    the_connection.commit()
    the_cursor.close()

#.........................Author-->Gyan Ranjan..................
