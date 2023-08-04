import tkinter as tk
import pandas as pd
from itertools import zip_longest


def submit_name():
    name = entry.get()
    entry.delete(0, tk.END)
    selected = var.get()
    if selected == 1:
        add_to_dict("Crucial", name)
    elif selected == 2:
        add_to_dict("High", name)
    elif selected == 3:
        add_to_dict("Medium", name)
    elif selected == 4:
        add_to_dict("Low", name)


def add_to_dict(priority, name):
    priority_dict[priority].append(name)


def send_to_excel():
    zl = list(zip_longest(*priority_dict.values()))
    df = pd.DataFrame(zl, columns=priority_dict.keys())
    df.to_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/names.xlsx', index=False)


priority_dict = {
    'Crucial': [],
    'High': [],
    'Medium': [],
    'Low': []
}

root = tk.Tk()
root.title("Name Input")
label = tk.Label(root, text="Enter their name:")
label.pack()

entry = tk.Entry(root)
entry.pack()

var = tk.IntVar()

R1 = tk.Radiobutton(root, text="Crucial", variable=var, value=1)
R1.pack()
R2 = tk.Radiobutton(root, text="High", variable=var, value=2)
R2.pack()
R3 = tk.Radiobutton(root, text="Medium", variable=var, value=3)
R3.pack()
R4 = tk.Radiobutton(root, text="Low", variable=var, value=4)
R4.pack()

submit_button = tk.Button(root, text="Submit", command=submit_name)
submit_button.pack()

root.mainloop()
send_to_excel()
