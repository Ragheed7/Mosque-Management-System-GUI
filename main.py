import difflib
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import sqlite3
import folium
import webbrowser

class MosqueManagementSystem:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1100x250")
        self.root.title("Mosques Management System")

        # Database Initialization
        self.database = sqlite3.connect('MosquesData.db')
        self.database.row_factory = sqlite3.Row
        self.database.execute(
            "CREATE TABLE IF NOT EXISTS `Mosque` (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT,"
            " Type TEXT,Coordinate TEXT,Address TEXT,Imam_Name TEXT)")
        self.database.commit()

        # Widgets Initialization
        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        # Frames Initialization
        self.frame_left = Frame(self.root)
        self.frame_left.grid(row=0, column=0, padx=(5, 10), pady=(0, 5))

        self.frame_top = Frame(self.frame_left)
        self.frame_top.grid(row=0, column=0, pady=(0, 15))

        self.frame_right = Frame(self.root)
        self.frame_right.grid(row=0, column=2, padx=(10, 5))

        self.frame_bottom_left = Frame(self.frame_left)
        self.frame_bottom_left.grid(row=1, column=0, pady=(15, 0), sticky="e")

        # StringVars
        self.entry_id = StringVar()
        self.entry_name = StringVar()
        self.selected_type = StringVar(self.root)
        self.selected_type.set("Arabic")
        self.entry_coordinate = StringVar()
        self.entry_address = StringVar()
        self.entry_imam_name = StringVar()

        # Font Settings
        label_font = ('Times New Roman', 12, 'bold')
        entry_font = ('Times New Roman', 12)
        button_font = ('Times New Roman', 10, 'bold')

        # Widgets
        self.label_id = Label(self.frame_top, font=label_font, text="ID")
        self.label_id.grid(row=0, column=0)
        self.entry_id_widget = Entry(self.frame_top, width=20, font=entry_font, textvariable=self.entry_id)
        self.entry_id_widget.grid(row=0, column=1, pady=2)
        self.entry_id_widget.focus()

        self.label_name = Label(self.frame_top, font=label_font, text="Name")
        self.label_name.grid(row=0, column=2)
        self.entry_name_widget = Entry(self.frame_top, width=20, font=entry_font, textvariable=self.entry_name)
        self.entry_name_widget.grid(row=0, column=3, pady=2)

        options_list = ["Arabic", "Persian", "Turkish", "Indian"]
        self.label_type = Label(self.frame_top, font=label_font, text="Type")
        self.label_type.grid(row=1, column=0)
        self.type_menu = OptionMenu(self.frame_top, self.selected_type, *options_list)
        self.type_menu.config(width=20)
        self.type_menu.grid(row=1, column=1, pady=2)

        self.label_coordinate = Label(self.frame_top, font=label_font, text="Coordinate")
        self.label_coordinate.grid(row=2, column=0)
        self.entry_coordinate_widget = Entry(self.frame_top, width=20, font=entry_font, textvariable=self.entry_coordinate)
        self.entry_coordinate_widget.grid(row=2, column=1, pady=2)

        self.label_address = Label(self.frame_top, font=label_font, text="Address")
        self.label_address.grid(row=1, column=2)
        self.entry_address_widget = Entry(self.frame_top, width=20, font=entry_font, textvariable=self.entry_address)
        self.entry_address_widget.grid(row=1, column=3, pady=2)

        self.label_imam_name = Label(self.frame_top, font=label_font, text="Imam name")
        self.label_imam_name.grid(row=2, column=2)
        self.entry_imam_name_widget = Entry(self.frame_top, width=20, font=entry_font, textvariable=self.entry_imam_name)
        self.entry_imam_name_widget.grid(row=2, column=3, pady=2)

        self.button_display_all = Button(self.frame_bottom_left, height=1, width=15, padx=5, pady=5, font=button_font,
                                         text="Display All", command=self.display_all)
        self.button_display_all.grid(row=3, column=1)

        self.button_add_entry = Button(self.frame_bottom_left, height=1, width=15, padx=5, pady=5,
                                       font=button_font, text="Add Entry", command=self.insert_entry)
        self.button_add_entry.grid(row=4, column=1)

        self.button_delete_entry = Button(self.frame_bottom_left, height=1, width=15, padx=5, pady=5,
                                          font=button_font, text="Delete entry", command=self.delete_entry)
        self.button_delete_entry.grid(row=4, column=2)

        self.button_update_entry = Button(self.frame_bottom_left, height=1, width=15, padx=5, pady=5,
                                          font=button_font, text="Update Entry", command=self.update_entry)
        self.button_update_entry.grid(row=3, column=2)

        self.button_display_on_map = Button(self.frame_bottom_left, height=1, width=15, padx=5, pady=5,
                                            font=button_font, text="Display on Map", command=self.display_on_map)
        self.button_display_on_map.grid(row=4, column=3)

        self.button_search = Button(self.frame_bottom_left, height=1, width=15, padx=5, pady=5,
                                            font=button_font, text="Search", command=self.search_records)
        self.button_search.grid(row=3, column=3)

        self.clear = Button(self.frame_bottom_left, height=1, width=15, padx=5, pady=5,
                                    font=button_font, text="Clear Fields", command=self.clear_entries)
        self.clear.grid(row=4, column=4)

        # dropdown menu for search criteria
        search_criteria_options = ["Name", "Imam Name", "Address", "Type"]
        self.selected_search_criteria = StringVar(self.root)
        self.selected_search_criteria.set(search_criteria_options[0])
        self.search_criteria_menu = OptionMenu(self.frame_bottom_left, self.selected_search_criteria, *search_criteria_options)
        self.search_criteria_menu.config(width=13)
        self.search_criteria_menu.grid(row=3, column=4, pady=5,padx=5)

        # Treeview
        self.treeview = Treeview(self.frame_right)
        self.treeview.grid(row=0, column=0)
        self.treeview.configure(column=('#Name', '#Imam Name', '#Type', '#Address', '#Coordinate'))
        self.treeview.heading('#0', text='ID')
        self.treeview.heading('#Name', text='Name')
        self.treeview.heading('#Type', text='Type')
        self.treeview.heading('#Address', text='Address')
        self.treeview.heading('#Coordinate', text='Coordinate')
        self.treeview.heading('#Imam Name', text='Imam Name')
        self.treeview.column('#0', width=50, anchor='center')
        self.treeview.column('#Name', width=100, anchor='center')
        self.treeview.column('#Type', width=80, anchor='center')
        self.treeview.column('#Address', width=100, anchor='center')
        self.treeview.column('#Coordinate', width=100, anchor='center')
        self.treeview.column('#Imam Name', width=100, anchor='center')

        self.bind_treeview()

        # Initial Display
        self.display_all()

    def bind_treeview(self):
        self.treeview.bind("<<TreeviewSelect>>", self.on_tree_select)

    def clear_entries(self):
        self.entry_name.set("")
        self.entry_id.set("")
        self.entry_coordinate.set("")
        self.entry_address.set("")
        self.entry_imam_name.set("")

    def insert_entry(self):
        id = self.entry_id.get()
        name = self.entry_name.get()
        type = self.selected_type.get()
        coordinate = self.entry_coordinate.get()
        address = self.entry_address.get()
        imam_name = self.entry_imam_name.get()

        if id == "" or name == "" or type == "" or coordinate == "" or address == "" or imam_name == "":
            missing_fields = []
            if id == "":
                missing_fields.append("ID")
            if name == "":
                missing_fields.append("Name")
            if type == "":
                missing_fields.append("Type")
            if coordinate == "":
                missing_fields.append("Coordinate")
            if address == "":
                missing_fields.append("Address")
            if imam_name == "":
                missing_fields.append("Imam Name")

            missing_fields_str = ', '.join(missing_fields)
            messagebox.showinfo(title="Add Record", message=f"Please Insert Data in the following fields: {missing_fields_str}!")
        else:
            try:
                # Check if ID already exists
                cursor = self.database.execute("SELECT ID FROM Mosque WHERE ID=?", (id,))
                existing_id = cursor.fetchone()
                if existing_id:
                    messagebox.showinfo(title="Add Record", message='ID already exists. Please choose a different ID.')
                else:
                    # Insert the new record
                    self.database.execute(
                        "INSERT INTO Mosque(ID, Name, Type, Coordinate, Address, Imam_Name) VALUES (?, ?, ?, ?, ?, ?)",
                        (id, name, type, coordinate, address, imam_name))
                    self.database.commit()
                    messagebox.showinfo(title="Add Record", message='Mosque Added successfully')
                    self.display_all()
                    self.clear_entries()

            except sqlite3.IntegrityError:
                messagebox.showinfo(title="Add Record", message='ID already exists. Please choose a different ID.')

    def display_row_in_treeview(self, row):
        item_id = row['ID']
        self.treeview.insert('', 'end', item_id, text=item_id)
        self.treeview.set(item_id, 0, row['Name'])
        self.treeview.set(item_id, 1, row['Imam_Name'])
        self.treeview.set(item_id, 2, row['Type'])
        self.treeview.set(item_id, 3, row['Address'])
        self.treeview.set(item_id, 4, row['Coordinate'])

    def search_records(self):
        search_criteria = self.selected_search_criteria.get()
        if search_criteria == "Name":
            self.search_by_name()
        elif search_criteria == "Imam Name":
            self.search_by_imam_name()
        elif search_criteria == "Address":
            self.search_by_address()
        elif search_criteria == "Type":
            self.search_by_type()
        else:
            messagebox.showinfo(title="Search Criteria", message="Please select a valid search criteria!")

    def search_by_id(self):
        self.treeview.delete(*self.treeview.get_children())
        id_to_search = self.entry_id.get()
        cursor = self.database.execute("select * from Mosque where ID=?", (id_to_search,))
        for row in cursor:
            self.display_row_in_treeview(row)

    def search_by_imam_name(self):
        self.treeview.delete(*self.treeview.get_children())
        imam_name_to_search = self.entry_imam_name.get()
        suggestions = self.get_closest_matches(imam_name_to_search, self.get_imam_names_from_database())
        if suggestions:
            selected_suggestion = messagebox.askquestion("Suggestions", f"Did you mean: {', '.join(suggestions)}?")
            if selected_suggestion == 'yes':
                imam_name_to_search = suggestions[0]
            else:
                return
        cursor = self.database.execute("select * from Mosque where Imam_Name LIKE ?", ('%' + imam_name_to_search + '%',))
        for row in cursor:
            self.display_row_in_treeview(row)

    def search_by_address(self):
        self.treeview.delete(*self.treeview.get_children())
        address_to_search = self.entry_address.get()
        suggestions = self.get_closest_matches(address_to_search, self.get_addresses_from_database())
        if suggestions:
            selected_suggestion = messagebox.askquestion("Suggestions", f"Did you mean: {', '.join(suggestions)}?")
            if selected_suggestion == 'yes':
                address_to_search = suggestions[0]
            else:
                return
        cursor = self.database.execute("select * from Mosque where Address LIKE ?", ('%' + address_to_search + '%',))
        for row in cursor:
            self.display_row_in_treeview(row)

    def search_by_type(self):
        self.treeview.delete(*self.treeview.get_children())
        type_to_search = self.selected_type.get()
        cursor = self.database.execute("select * from Mosque where Type=?", (type_to_search,))
        for row in cursor:
            self.display_row_in_treeview(row)

    def search_by_name(self):
        self.treeview.delete(*self.treeview.get_children())
        name_to_search = self.entry_name.get()
        suggestions = self.get_closest_matches(name_to_search, self.get_names_from_database())
        if suggestions:
            selected_suggestion = messagebox.askquestion("Suggestions", f"Did you mean: {', '.join(suggestions)}?")
            if selected_suggestion == 'yes':
                name_to_search = suggestions[0]
            else:
                return
        cursor = self.database.execute("select * from Mosque where Name LIKE ?", ('%' + name_to_search + '%',))
        for row in cursor:
            self.display_row_in_treeview(row)

    def get_names_from_database(self):
        cursor = self.database.execute("select Name from Mosque")
        return [row['Name'] for row in cursor]

    def get_imam_names_from_database(self):
        cursor = self.database.execute("select Imam_Name from Mosque")
        return [row['Imam_Name'] for row in cursor]

    def get_addresses_from_database(self):
        cursor = self.database.execute("select Address from Mosque")
        return [row['Address'] for row in cursor]

    def get_closest_matches(self, term, options, n=3, cutoff=0.6):
        return difflib.get_close_matches(term, options, n=n, cutoff=cutoff)

    def on_tree_select(self, event):
        selected_items = self.treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            cursor = self.database.execute("select * from Mosque where ID=?", (selected_item,))
            for row in cursor:
                self.entry_id.set(str(row['ID']))
                self.entry_name.set(str(row['Name']))
                self.selected_type.set(str(row['Type']))
                self.entry_coordinate.set(str(row['Coordinate']))
                self.entry_address.set(str(row['Address']))
                self.entry_imam_name.set(str(row['Imam_Name']))

    def delete_entry(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showinfo("Delete Record", "Please select a record to delete.")
            return

        selected_item = selected_items[0]

        try:
            conn = sqlite3.connect("MosquesData.db")
            cur = conn.cursor()

            # Delete the record from the database
            cur.execute("DELETE FROM Mosque WHERE ID=?", (selected_item,))
            conn.commit()

            # Delete the item from the Treeview
            self.treeview.delete(selected_item)
            messagebox.showinfo("Delete Record", "Record is deleted successfully.")
            self.display_all()
            self.clear_entries()

        except sqlite3.Error as e:
            messagebox.showerror("Delete Error", f"An error occurred while deleting the record: {e}")

        finally:
            conn.close()

    def update_entry(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showinfo("Update Record", "Please select a record to update.")
            return

        selected_item = selected_items[0]
        if (
                self.entry_id.get() == ""
                or self.entry_name.get() == ""
                or self.selected_type.get() == ""
                or self.entry_coordinate.get() == ""
                or self.entry_address.get() == ""
                or self.entry_imam_name.get() == ""
        ):
            messagebox.showinfo(title="Update Record", message="Please insert data.")
            return

        try:
            id = self.entry_id.get()
            name = self.entry_name.get()
            type = self.selected_type.get()
            coordinate = self.entry_coordinate.get()
            address = self.entry_address.get()
            imam_name = self.entry_imam_name.get()

            # Update all fields in the database
            self.database.execute(
                "UPDATE Mosque SET Name=?, Type=?, Coordinate=?, Address=?, Imam_Name=? WHERE ID=?",
                (name, type, coordinate, address, imam_name, id),
            )
            self.database.commit()

            # Update the columns in the Treeview list
            self.treeview.set(selected_item, '#Name', name)
            self.treeview.set(selected_item, '#Type', type)
            self.treeview.set(selected_item, '#Coordinate', coordinate)
            self.treeview.set(selected_item, '#Address', address)
            self.treeview.set(selected_item, '#Imam Name', imam_name)

            messagebox.showinfo(title="Update Record", message="Data is updated successfully.")
            self.clear_entries()

        except Exception as e:
            messagebox.showerror(title="Update Error", message=f"An error occurred: {e}")

    def display_all(self):
        self.treeview.delete(*self.treeview.get_children())
        try:
            cursor = self.database.execute("SELECT * FROM Mosque")
            for row in cursor:
                self.display_row_in_treeview(row)

        except sqlite3.Error as e:
            messagebox.showinfo(title="Display All", message=f'Error fetching data: {e}')

    def display_on_map(self):
        selected_items = self.treeview.selection()

        if not selected_items:
            messagebox.showinfo("Display on Map", "Please select a record from the list.")
            return

        selected_item = selected_items[0]
        coordinates = self.treeview.item(selected_item, "values")[4]
        if coordinates:
            output_file = "map.html"
            latitude, longitude = coordinates.split(',')
            map_object = folium.Map(location=[float(latitude), float(longitude)])
            map_object.save(output_file)
            webbrowser.open(output_file, new=2)
        else:
            messagebox.showinfo("Display on Map", "Selected record does not have coordinates.")

if __name__ == '__main__':
    MosqueManagementSystem()
