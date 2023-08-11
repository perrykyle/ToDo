import os
import threading
import tkinter as tk
from datetime import datetime
from tkinter import ttk
import uuid
from pymstodo import ToDoConnection
import webbrowser
from dotenv import load_dotenv, set_key
from ManageTasks import run_functions


# Dictionary mapping day numbers to their string names
days_of_week = {
    "0": "Sun",
    "1": "Mon",
    "2": "Tue",
    "3": "Wed",
    "4": "Thu",
    "5": "Fri",
    "6": "Sat"
}


class ToDoManager(tk.Tk):
    """The main application window"""

    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("To Do Manager")
        self.geometry("350x450")
        self.iconbitmap('references/logo.ico')
        self.resizable(0, 0)

        # Set up styles
        self.style = ttk.Style()
        self.style.configure('danger.TButton', foreground='red', bordercolor='red')

        # Load the tasks
        self.tasks = self.load_tasks()
        self.upcoming_tasks = self.load_upcoming_tasks()

        # Create the widgets
        self.create_widgets()

    # Function to format date and time for display
    def format_datetime(self, datetime_string):
        time_string, date_string = datetime_string.split("-", 1)
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return f"{time_string} {date.strftime('%a - %b %d %Y')}"

    # Function to validate input time
    def validate_time(self, input):
        if input.isdigit():
            return True
        elif input == "":
            return True
        else:
            return False

    # Function to validate time range
    def validate_time_range(self, input, lower_limit, upper_limit):
        if input.isdigit():
            if lower_limit <= int(input) <= upper_limit:
                return True
        return False

    # Function to validate input string
    def validate_input(self, input):
        if ',' in input:
            return False
        return True

    # Function to load tasks from the file
    def load_tasks(self):
        tasks = []
        if os.path.exists("references/tasks.txt"):
            with open("references/tasks.txt", "r") as file:
                for line in file:
                    id, name, time, day_codes, description = line.strip().split(",")
                    days = ', '.join([days_of_week[code] for code in day_codes])
                    tasks.append(Tasks(id, name, time, days, description))
        return tasks

    # Function to load upcoming tasks from the file
    def load_upcoming_tasks(self):
        tasks = []
        if os.path.exists("references/upcoming_tasks.txt"):
            with open("references/upcoming_tasks.txt", "r") as file:
                for line in file:
                    id, name, datetime, description = line.strip().split(",")
                    tasks.append(UpcomingTasks(id, name, datetime, description))
        return tasks

    # Function to delete a task
    def delete_task(self, task_id):
        lines = []
        with open("references/tasks.txt", "r") as file:
            lines = file.readlines()

        with open("references/tasks.txt", "w") as file:
            for line in lines:
                if line.split(",")[0] != task_id:
                    file.write(line)

        print("Task deleted")
        self.show_task_list()

    # Function to delete an upcoming task
    def delete_upcoming_task(self, task_id):
        lines = []
        with open("references/upcoming_tasks.txt", "r") as file:
            lines = file.readlines()

        with open("references/upcoming_tasks.txt", "w") as file:
            for line in lines:
                if line.split(",")[0] != task_id:
                    file.write(line)

        print("Upcoming Task deleted")
        self.show_upcoming_task_list()

    # Function to create a new task
    def create_new_task(self):
        name = self.name_entry.get().strip()
        hours = self.hour_entry.get().strip().zfill(2)
        minutes = self.minute_entry.get().strip().zfill(2)
        description = self.description_text.get("1.0", tk.END).strip()

        time = f"{hours}:{minutes}"

        days = ""
        for day, checkbox in self.day_checkboxes.items():
            if checkbox.get():
                days += str(day)

        if not name:
            self.warning_label.config(text="Add a Task Name", foreground="red")
            return

        if not time:
            self.warning_label.config(text="Add a task completion time", foreground="red")
            return

        if not days:
            self.warning_label.config(text="Add days for task completion", foreground="red")
            return

        if not self.validate_time_range(hours, 0, 23) or not self.validate_time_range(minutes, 0, 59):
            self.warning_label.config(text="Invalid time input", foreground="red")
            return

        if not self.validate_input(name) or not self.validate_input(description):
            self.warning_label.config(text="Commas are not accepted characters", foreground="red")
            return

        id = str(uuid.uuid4())
        with open("references/tasks.txt", "a") as file:
            file.write(f"{id},{name},{time},{days},{description}\n")

        self.show_task_list()

        # Display success message
        self.warning_label.config(text="Task created successfully", foreground="green")
        threading.Timer(3, lambda: self.warning_label.config(text="")).start()

    # Function to create widgets for the new task form
    def create_new_task_view(self):
        for widget in self.new_task_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.new_task_tab, text="New Task", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                       pady=10, sticky="nsew")

        ttk.Label(self.new_task_tab, text="Task Name:").grid(row=1, column=0, pady=5, sticky="nsew")
        self.name_entry = ttk.Entry(self.new_task_tab, width=30)
        self.name_entry.grid(row=2, column=0, pady=5, sticky="nsew")

        ttk.Label(self.new_task_tab, text="Time (24hr):").grid(row=3, column=0, pady=5, sticky="nsew")
        validate_command = self.register(self.validate_time)
        self.hour_entry = ttk.Entry(self.new_task_tab, width=10, validate="key",
                                    validatecommand=(validate_command, '%P'))
        self.hour_entry.grid(row=4, column=0, pady=5, sticky="w")
        ttk.Label(self.new_task_tab, text=":").grid(row=4, column=0, padx=(68, 0), sticky="w")  # colon label
        self.minute_entry = ttk.Entry(self.new_task_tab, width=10, validate="key",
                                      validatecommand=(validate_command, '%P'))
        self.minute_entry.grid(row=4, column=0, pady=5, sticky="w", padx=(76, 0))

        ttk.Label(self.new_task_tab, text="Days:").grid(row=5, column=0, pady=(10, 0), sticky="nsew")

        self.day_checkboxes = {}
        days = ["Sun", "Mon", "Tues", "Wed", "Thu", "Fri", "Sat"]
        for index, day in enumerate(days):
            day_var = tk.BooleanVar()
            ttk.Checkbutton(self.new_task_tab, text=day, variable=day_var).grid(row=6, column=0, padx=(index * 45, 0),
                                                                                sticky="nsew")
            self.day_checkboxes[index] = day_var

        ttk.Label(self.new_task_tab, text="Description (optional):").grid(row=7, column=0, columnspan=2, pady=(10, 0),
                                                                          sticky="nsew")
        self.description_text = tk.Text(self.new_task_tab, width=30, height=5)
        self.description_text.grid(row=8, column=0, columnspan=2, pady=5, sticky="nsew")

        ttk.Button(self.new_task_tab, text="Create Task", command=self.create_new_task).grid(row=9, column=0, columnspan=2,
                                                                                             pady=5, sticky="nsew")
        self.warning_label = ttk.Label(self.new_task_tab, text="", foreground="red")
        self.warning_label.grid(row=10, column=0, columnspan=2, pady=5, sticky="nsew")

        for i in range(12):
            self.new_task_tab.grid_rowconfigure(i, weight=1)
        self.new_task_tab.grid_columnconfigure(0, weight=1)

    # Function to display task details
    def show_task_details(self, task):
        for widget in self.view_tab.winfo_children():
            widget.destroy()
        ttk.Label(self.view_tab, text=task.name, font=("Arial", 16, "bold"), wraplength=250).grid(row=0, column=0,
                                                                                                  pady=20)
        ttk.Label(self.view_tab, text=f"Time: {task.time}").grid(row=1, column=0)
        ttk.Label(self.view_tab, text=f"Days: {task.days}").grid(row=2, column=0)
        ttk.Label(self.view_tab, text=f"Description: {task.description}", wraplength=250).grid(row=3, column=0, pady=20)
        ttk.Button(self.view_tab, text="Back", command=self.show_task_list).grid(row=4, column=0, pady=10)
        ttk.Button(self.view_tab, text="Delete Task", command=lambda: self.delete_task(task.id),
                   style='danger.TButton').grid(row=5, column=0, pady=10)

    # Function to display upcoming task details
    def show_upcoming_task_details(self, task):
        for widget in self.upcoming_tasks_tab.winfo_children():
            widget.destroy()
        ttk.Label(self.upcoming_tasks_tab, text=task.name, font=("Arial", 16, "bold"), wraplength=250).grid(row=0, column=0, pady=20)
        ttk.Label(self.upcoming_tasks_tab, text=f"Time: {self.format_datetime(task.datetime)}").grid(row=1, column=0)
        ttk.Label(self.upcoming_tasks_tab, text=f"Description: {task.description}", wraplength=250).grid(row=2, column=0, pady=20)
        ttk.Button(self.upcoming_tasks_tab, text="Back", command=self.show_upcoming_task_list).grid(row=3, column=0, pady=10)
        ttk.Button(self.upcoming_tasks_tab, text="Delete Task", command=lambda: self.delete_upcoming_task(task.id),
                   style='danger.TButton').grid(row=4, column=0, pady=10)

    # Function to show the list of tasks
    def show_task_list(self):
        self.tasks = self.load_tasks()
        for widget in self.view_tab.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.view_tab)
        scrollbar = ttk.Scrollbar(self.view_tab, orient="vertical", command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        for index, task in enumerate(self.tasks):
            frame = ttk.Frame(scrollable_frame, width=300, height=50, relief='solid', borderwidth=1)
            frame.grid(row=index, column=0, pady=0, padx=5, sticky="ew")
            frame.columnconfigure(0, weight=1)

            label_name = ttk.Label(frame, text=task.name, font=("Arial", 12, "bold"), anchor="w")
            label_name.grid(row=0, column=0, padx=10, sticky="ew")

            label_details = ttk.Label(frame, text=f"{task.time} | {task.days}", anchor="w")
            label_details.grid(row=1, column=0, padx=10, sticky="ew")

            frame.bind("<Button-1>", lambda event, task=task: self.show_task_details(task))
            label_name.bind("<Button-1>", lambda event, task=task: self.show_task_details(task))
            label_details.bind("<Button-1>", lambda event, task=task: self.show_task_details(task))

        self.view_tab.grid_columnconfigure(0, weight=1)
        self.view_tab.grid_rowconfigure(0, weight=1)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    # Function to show the list of upcoming tasks
    def show_upcoming_task_list(self):
        self.upcoming_tasks = self.load_upcoming_tasks()
        for widget in self.upcoming_tasks_tab.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.upcoming_tasks_tab)
        scrollbar = ttk.Scrollbar(self.upcoming_tasks_tab, orient="vertical", command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        for index, task in enumerate(self.upcoming_tasks):
            frame = ttk.Frame(scrollable_frame, width=300, height=50, relief='solid', borderwidth=1)
            frame.grid(row=index, column=0, pady=0, padx=5, sticky="ew")
            frame.columnconfigure(0, weight=1)

            label_name = ttk.Label(frame, text=task.name, font=("Arial", 12, "bold"), anchor="w")
            label_name.grid(row=0, column=0, padx=10, sticky="ew")

            label_details = ttk.Label(frame, text=f"{self.format_datetime(task.datetime)}", anchor="w")
            label_details.grid(row=1, column=0, padx=10, sticky="ew")

            frame.bind("<Button-1>", lambda event, task=task: self.show_upcoming_task_details(task))
            label_name.bind("<Button-1>", lambda event, task=task: self.show_upcoming_task_details(task))
            label_details.bind("<Button-1>", lambda event, task=task: self.show_upcoming_task_details(task))

        self.upcoming_tasks_tab.grid_columnconfigure(0, weight=1)
        self.upcoming_tasks_tab.grid_rowconfigure(0, weight=1)

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    # Function to display the authentication interface
    def create_regen_key_view(self):
        # Clear the tab
        for widget in self.regen_key_tab.winfo_children():
            widget.destroy()

        # Create the "Generate Authentication URL" button
        gen_auth_url_button = ttk.Button(self.regen_key_tab, text="Generate Authentication URL",
                                         command=self.gen_auth_url)
        gen_auth_url_button.pack(pady=10)

        # Create the "Authorization Link" button (initially disabled)
        self.auth_url_button = ttk.Button(self.regen_key_tab, text="Authorization Link", state="disabled")
        self.auth_url_button.pack(pady=10)

        # Instructions
        instructions = tk.Label(self.regen_key_tab,
                                text="Sign into your Microsoft Account linked to your Microsoft ToDo Account of preference, "
                                     "and then copy the URL that you are redirected to. "
                                     "(It will not load properly in your browser, that's okay.)",
                                wraplength=300)
        instructions.pack(pady=10)

        # Create the redirect URL entry field
        self.redirect_entry = ttk.Entry(self.regen_key_tab, width=50)
        self.redirect_entry.pack(pady=10)

        # Create the "Get Token" button
        get_token_button = ttk.Button(self.regen_key_tab, text="Get Token", command=self.get_token)
        get_token_button.pack(pady=10)

        # Create the success/failure message label (initially empty)
        self.message_label = tk.Label(self.regen_key_tab, text="", foreground="green")
        self.message_label.pack(pady=10)

    # Generates authentication url to add to button
    def gen_auth_url(self):
        client_id = os.getenv("CLIENT_ID")
        auth_url = ToDoConnection.get_auth_url(client_id)

        # Update the GUI with the auth URL
        self.auth_url_button.config(text="Authorization Link", command=lambda: webbrowser.open(auth_url),
                                    state="normal")

    # Function which processes token based on redirect URL
    def get_token(self):
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        redirect_resp = self.redirect_entry.get()

        try:
            token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)
            set_key('.env', "TOKEN", str(token))
            self.message_label.config(text="Authentication Successful", foreground="green")
        except Exception:
            self.message_label.config(text="Authentication Unsuccessful", foreground="red")

    # Tab showing the refresh tasks
    def show_refresh_tasks(self):
        # Clear the tab
        for widget in self.refresh_tab.winfo_children():
            widget.destroy()

        # Create the "Refresh tasks" button
        refresh_button = ttk.Button(self.refresh_tab, text="Refresh tasks", command=self.handle_refresh)
        refresh_button.pack(pady=10)

        # Create the status message label (initially empty)
        self.refresh_status_label = tk.Label(self.refresh_tab, text="", foreground="green")
        self.refresh_status_label.pack(pady=10)

    # Function calling the refresh tasks function
    def handle_refresh(self):
        # Update the status label to "Working..."
        self.refresh_status_label.config(text="Working...", foreground="black")

        # Attempt to refresh tasks
        try:
            self.after(1750, run_functions())
            # Update the status label to "Tasks successfully refreshed!" in green
            self.refresh_status_label.config(text="Tasks successfully refreshed!", foreground="green")
        except Exception as e:
            # Update the status label to "Authentication/File Structure Error" in red
            print(e)
            self.refresh_status_label.config(text="Authentication/Task Structure Error", foreground="red")

        # Call to show upcoming tasks list
        self.show_upcoming_task_list()

        # Disapear text
        self.after(3000, lambda: self.refresh_status_label.config(text=""))


    # Function to create the main widgets
    def create_widgets(self):
        self.tab_control = ttk.Notebook(self)

        self.view_tab = ttk.Frame(self.tab_control)
        self.new_task_tab = ttk.Frame(self.tab_control)
        self.upcoming_tasks_tab = ttk.Frame(self.tab_control)
        self.regen_key_tab = ttk.Frame(self.tab_control)
        self.refresh_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.view_tab, text='Weekly Tasks')
        self.tab_control.add(self.new_task_tab, text='Add Weekly Task')
        self.tab_control.add(self.upcoming_tasks_tab, text='Upcoming Tasks')
        self.tab_control.add(self.regen_key_tab, text="\U0001F511")
        self.tab_control.add(self.refresh_tab, text="\U0001F503")

        self.tab_control.pack(expand=1, fill='both')

        self.show_task_list()
        self.create_new_task_view()
        self.show_upcoming_task_list()
        self.create_regen_key_view()
        self.show_refresh_tasks()


    # Run the application
    def run(self):
        self.mainloop()


class Tasks:
    """Class to represent a Task"""

    def __init__(self, id, name, time, days, description):
        self.id = id
        self.name = name
        self.time = time
        self.days = days
        self.description = description


class UpcomingTasks:
    """Class to represent an Upcoming Task"""

    def __init__(self, id, name, datetime, description):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.description = description


if __name__ == "__main__":
    load_dotenv()
    to_do_manager = ToDoManager()
    to_do_manager.run()
