import tkinter as tk
from tkinter import ttk


class TreeViewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview Alternating Row Highlight Example")

        # Initialize the Treeview
        self.tree = ttk.Treeview(root, columns=(
            "Name", "Age", "City"), show="headings")
        self.tree.pack(fill="both", expand=True)

        # Setup the columns and tags
        self.setup_treeview()

        # Load sample data
        self.data = [
            ("Alice", 30, "New York"),
            ("Bob", 25, "Los Angeles"),
            ("Charlie", 35, "Chicago"),
            ("David", 28, "Houston"),
            ("Eva", 40, "Phoenix"),
        ]

        self.load_data()

    def setup_treeview(self):
        """Set up columns and tags for the Treeview."""
        # Define the column headings
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("City", text="City")

        # Define alternating row tags
        self.tree.tag_configure("oddrow", background="gray90")
        self.tree.tag_configure("evenrow", background="white")

    def load_data(self):
        """Load data into the Treeview with alternating row colors."""
        for index, (name, age, city) in enumerate(self.data):
            # Apply "oddrow" tag to even-indexed rows and "evenrow" to odd-indexed rows
            row_tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.tree.insert("", "end", values=(
                name, age, city), tags=(row_tag,))


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeViewApp(root)
    root.mainloop()
