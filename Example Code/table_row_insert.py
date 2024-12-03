import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview


class TableManager:
    def __init__(self, root):
        # Define columns
        self.columns = [
            {"text": "ID", "stretch": False},
            {"text": "Name", "stretch": True},
            {"text": "Age", "stretch": False},
            {"text": "City", "stretch": True}
        ]

        # Create initial data
        self.initial_data = [
            (1, "John Doe", 25, "New York"),
            (2, "Jane Smith", 30, "Los Angeles")
        ]

        # Create the Tableview
        self.table = Tableview(
            master=root,
            coldata=self.columns,
            rowdata=self.initial_data,
            paginated=False,
            searchable=True,
            bootstyle="primary"
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Create control buttons
        self.create_buttons(root)

    def create_buttons(self, root):
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=5)

        ttk.Button(
            button_frame,
            text="Insert Single Row",
            command=self.insert_single_row,
            bootstyle="success"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Insert Multiple Rows",
            command=self.insert_multiple_rows,
            bootstyle="info"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Insert at Position",
            command=self.insert_at_position,
            bootstyle="warning"
        ).pack(side="left", padx=5)

    def insert_single_row(self):
        """Insert a single row at the end of the table"""
        # Get the next ID based on existing data
        next_id = len(self.table.get_rows()) + 1

        # Create new row data
        new_row = (next_id, f"Person {next_id}",
                   20 + next_id, f"City {next_id}")

        # Insert the row
        self.table.insert_row("end", new_row)

    def insert_multiple_rows(self):
        """Insert multiple rows at once"""
        # Get the next ID
        start_id = len(self.table.get_rows()) + 1

        # Create multiple rows
        new_rows = [
            (start_id, f"Batch Person {start_id}", 25, "Chicago"),
            (start_id + 1, f"Batch Person {start_id + 1}", 28, "Houston"),
            (start_id + 2, f"Batch Person {start_id + 2}", 32, "Phoenix")
        ]

        # Insert all rows
        for row in new_rows:
            self.table.insert_row("end", row)

    def insert_at_position(self):
        """Insert a row at a specific position (index 1 in this example)"""
        # Create new row data
        new_row = (999, "Inserted At Position", 45, "Miami")

        # Insert at position 1 (second row)
        self.table.insert_row(1, new_row)

    def insert_data_from_dict(self, data_dict):
        """Insert data from a dictionary"""
        row = (
            data_dict.get('id'),
            data_dict.get('name'),
            data_dict.get('age'),
            data_dict.get('city')
        )
        self.table.insert_row("end", row)

    def insert_data_from_list(self, data_list):
        """Insert data from a list of dictionaries"""
        for item in data_list:
            self.insert_data_from_dict(item)


def main():
    root = ttk.Window(title="Tableview Data Insertion Example")
    root.geometry("600x400")

    table_manager = TableManager(root)

    # Example of inserting from dictionary
    new_person = {
        'id': 100,
        'name': 'Alice Johnson',
        'age': 28,
        'city': 'Seattle'
    }
    table_manager.insert_data_from_dict(new_person)

    # Example of inserting from list of dictionaries
    people_list = [
        {'id': 101, 'name': 'Bob Wilson', 'age': 35, 'city': 'Denver'},
        {'id': 102, 'name': 'Carol Brown', 'age': 29, 'city': 'Boston'}
    ]
    table_manager.insert_data_from_list(people_list)

    root.mainloop()


if __name__ == "__main__":
    main()
