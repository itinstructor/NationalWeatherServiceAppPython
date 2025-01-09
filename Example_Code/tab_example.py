import tkinter as tk
from tkinter import ttk

class TabExampleApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tabbed Interface Example")
        self.geometry("400x300")

        # Create a Notebook widget
        notebook = ttk.Notebook(self)
        notebook.pack(expand=1, fill='both')

        # Create frames for each tab
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)

        # Add tabs to the notebook
        notebook.add(tab1, text='Tab 1')
        notebook.add(tab2, text='Tab 2')
        notebook.add(tab3, text='Tab 3')

        # Add content to Tab 1
        label1 = ttk.Label(tab1, text="This is Tab 1")
        label1.pack(pady=20, padx=20)

        # Add content to Tab 2
        label2 = ttk.Label(tab2, text="This is Tab 2")
        label2.pack(pady=20, padx=20)

        # Add content to Tab 3
        label3 = ttk.Label(tab3, text="This is Tab 3")
        label3.pack(pady=20, padx=20)

if __name__ == "__main__":
    app = TabExampleApp()
    app.mainloop()