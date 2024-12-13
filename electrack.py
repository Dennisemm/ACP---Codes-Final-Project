from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from db_connect import Database


class ElecTrack:
    def __init__(self, root):
        self.root = root
        self.root.title("Electrack: Electric Tracker System")
        self.root.geometry("750x600")
        self.root.configure(bg='beige')
        self.root.resizable(0,0)

        self.database = Database()
        self.conn = self.database.get_db_connection()
        self.c = self.conn.cursor()
        
        self.create_users_table()
        self.entries = {}
        self.show_main_menu()
        
    def create_users_table(self):
        try:
            self.c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                middle_initial VARCHAR(10),
                last_name VARCHAR(255) NOT NULL,
                age INT,
                address VARCHAR(255),
                zipcode VARCHAR(20),
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                total_bill DECIMAL(10, 2) DEFAULT 0
            )
            ''')
            self.conn.commit()
        except Error as e:
            print(f"Error creating table: {e}")
            
            command=self.show_main_menu(self)
            
    def create_admin_table(self):
        try:
            self.c.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                middle_initial VARCHAR(10),
                last_name VARCHAR(255) NOT NULL,
                age INT,
                address VARCHAR(255),
                zipcode VARCHAR(20),
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                total_bill DECIMAL(10, 2) DEFAULT 0
            )
            ''')
            self.conn.commit()
        except Error as e:
            print(f"Error creating table: {e}")
            
            command=self.show_admin_dashboard(self)
    def show_main_menu(self):
        self.clear_window()
        # Add buttons for login and registration
        login_button = tk.Button(self.root, text="Login", command=self.show_user_login)
        login_button.pack(pady=10)
        
        admin_login_button = tk.Button(self.root, text="Admin Login", command=self.show_admin_login)
        admin_login_button.pack(pady=10)
        
        register_button = tk.Button(self.root, text="Register", command=self.show_registration_window)
        register_button.pack(pady=10)
        
    def show_registration_window(self):
        self.clear_window()
        
        title_label = Label(self.root, text="Register", bg='beige', font=("Arial", 18))
        title_label.grid(row=0, columnspan=4, pady=10)

        labels = ["First Name", "Middle Initial", "Last Name", "Age", "Address", "Zipcode", "Username", "Password", "Confirm Password"]
        self.entries = {}

        for i, label in enumerate(labels):
            lbl = Label(self.root, text=label, bg='beige')
            lbl.grid(row=(i // 2) + 1, column=(i % 2) * 2, padx=5, pady=5)
            entry = Entry(self.root)
            entry.grid(row=(i // 2) + 1, column=(i % 2) * 2 + 1, padx=5, pady=5)
            self.entries[label] = entry

        register_button = Button(self.root, text="Register", command=self.register_user)
        register_button.grid(row=len(labels) // 2 + 2, column=0, columnspan=2, pady=10)

        back_button = Button(self.root, text="Back to User Login", command=self.show_user_login)
        back_button.grid(row=len(labels) // 2 + 2, column=2, columnspan=2, pady=5)

    def register_user(self):
        first_name = self.entries["First Name"].get()
        middle_initial = self.entries["Middle Initial"].get()
        last_name = self.entries["Last Name"].get()
        age = self.entries["Age"].get()
        address = self.entries["Address"].get()
        zipcode = self.entries["Zipcode"].get()
        username = self.entries["Username"].get()
        password = self.entries["Password"].get()
        confirm_password = self.entries["Confirm Password"].get()

        if not (first_name and last_name and age and address and zipcode and username and password):
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        if password != confirm_password:
            messagebox.showwarning("Input Error", "Passwords do not match.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be a number.")
            return

        try:
            self.c.execute("INSERT INTO users (first_name, middle_initial, last_name, age, address, zipcode, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                           (middle_initial, last_name, age, address, zipcode, username, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.show_main_menu()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Database Error", "Username already exists. Please choose a different username.")
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def show_user_login(self):
        self.clear_window()
    
    # Create labels and entry fields for login
        tk.Label(self.root, text="Username", bg='beige').pack(pady=10)
        self.entries["Username"] = tk.Entry(self.root)
        self.entries["Username"].pack(pady=10)

        tk.Label(self.root, text="Password", bg='beige').pack(pady=10)
        self.entries["Password"] = tk.Entry(self.root, show='*')
        self.entries["Password"].pack(pady=10)

        login_button = tk.Button(self.root, text="Login", command=self.user_login)
        login_button.pack(pady=10)
    
        # Change this line to call show_admin_login instead of admin_login
        admin_login_button = tk.Button(self.root, text="Admin Login", command=self.show_admin_login)
        admin_login_button.pack(pady=5)

        back_button = tk.Button(self.root, text="Back", command=self.show_main_menu)
        back_button.pack(pady=10)


    def user_login(self):
        username = self.entries["Username"].get()
        password = self.entries["Password"].get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        try:
            # Use %s as placeholders for MySQL
            self.c.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = self.c.fetchone()  # Fetch one result

            if user:
                messagebox.showinfo("Login Success", "Welcome back!")
                # Here you can proceed to the next step, such as opening a user dashboard
                self.show_user_dashboard(user)  # Example function to show user dashboard
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def show_user_dashboard(self, user):
        self.clear_window()

        Label(self.root, text="Duration From (YYYY-MM-DD)", bg='beige').pack(pady=5)
        self.duration_from_entry = Entry(self.root)
        self.duration_from_entry.pack(pady=5)

        Label(self.root, text="Duration To (YYYY-MM-DD)", bg='beige').pack(pady=5)
        self.duration_to_entry = Entry(self.root)
        self.duration_to_entry.pack(pady=5)

        Label(self.root, text="Electricity Usage", bg='beige').pack(pady=5)
        self.electricity_usage_entry = Entry(self.root)
        self.electricity_usage_entry.pack(pady=5)

        submit_button = Button(self.root, text="Submit", command=self.submit_usage)
        submit_button.pack(pady=5)

        # Pass the user ID to show_user_data
        show_data_button = Button(self.root, text="Show Data", command=lambda: self.show_user_data(user[0]))  # Assuming user[0] is the ID
        show_data_button.pack(pady=5)

        logout_button = Button(self.root, text="Logout", command=self.show_main_menu)
        logout_button.pack(pady=5)

    def submit_usage(self):
        try:
            electricity_usage = float(self.electricity_usage_entry.get())
            bill = electricity_usage * 20
            messagebox.showinfo("Success", f"Your bill is: ${bill:.2f}")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for electricity usage.")
        
    def show_user_data(self, user_id):
        self.clear_window()
    
        # Fetch only the logged-in user's data
        self.c.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        records = self.c.fetchall()

        frame = Frame(self.root)
        frame.pack(pady=20)

        # Define the columns correctly
        columns = ("ID", "First Name", "Middle Initial", "Last Name", "Age", "Address", "Zipcode")
        tree = ttk.Treeview(frame, columns=columns, show='headings')

        # Set up the headings
        for col in columns:
            tree.heading(col, text=col)

        for record in records:
            # Ensure that the record has the same number of elements as the columns
            tree.insert("", "end", values=record)

        scrollbar_y = Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")

        tree.pack()

        back_button = Button(self.root, text="Back to Dashboard", command=lambda: self.show_user_dashboard(record))
        back_button.pack(pady=5)

    def show_admin_login(self):
        self.clear_window()
    
        tk.Label(self.root, text="Admin Username", bg='beige').pack(pady=10)
        self.admin_username_entry = tk.Entry(self.root)  # Define the entry for admin username
        self.admin_username_entry.pack(pady=10)

        tk.Label(self.root, text="Admin Password", bg='beige').pack(pady=10)
        self.admin_password_entry = tk.Entry(self.root, show='*')  # Define the entry for admin password
        self.admin_password_entry.pack(pady=10)

        admin_login_button = tk.Button(self.root, text="Login", command=self.admin_login)
        admin_login_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.show_main_menu)
        back_button.pack(pady=10)

    def admin_login(self):
        username = self.admin_username_entry.get()  # Access the admin username entry
        password = self.admin_password_entry.get()  # Access the admin password entry

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        # Implement your admin login logic here
        admin_username = "admin"
        admin_password = "admin123"

        # For example, check against the database
        try:
            self.c.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin = self.c.fetchone()  # Fetch one result

            if username == admin_username and password == admin_password:
                messagebox.showinfo("Login Success", "Welcome Admin!")
                self.show_admin_dashboard()
                
        # Proceed to the admin dashboard or functionality
            else:
                messagebox.showerror("Login Failed", "Invalid admin username or password.")
        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            
    def show_admin_dashboard(self):
        self.clear_window()

        title_label = Label(self.root, text="Admin Dashboard", bg='beige', font=("Arial", 18))
        title_label.pack(pady=10)

    # Adjust the SQL query to select the ID and other required fields
        self.c.execute("SELECT id, last_name, first_name, address, total_bill FROM users")
        records = self.c.fetchall()

        frame = Frame(self.root)
        frame.pack(pady=20)

    # Update the Treeview to show the ID along with other specified columns
        self.my_tree = ttk.Treeview(frame, columns=("ID", "Last Name", "First Name", "Address", "Total Bill"), show='headings')
        self.my_tree.heading("ID", text="ID")
        self.my_tree.heading("Last Name", text="Last Name")
        self.my_tree.heading("First Name", text="First Name")
        self.my_tree.heading("Address", text="Address")
        self.my_tree.heading("Total Bill", text="Total Bill")

    # Insert records into the Treeview
        for record in records:
            self.my_tree.insert("", "end", values=record)

    # Add vertical scrollbar
        scrollbar_y = Scrollbar(frame, orient="vertical", command=self.my_tree.yview)
        self.my_tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

    # Add horizontal scrollbar
        scrollbar_x = Scrollbar(frame, orient="horizontal", command=self.my_tree.xview)
        self.my_tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")

        self.my_tree.pack()

    # Buttons for additional functionality
        delete_button = Button(self.root, text="Delete User", command=self.delete_user)
        delete_button.pack(pady=5)

        logout_button = Button(self.root, text="Logout", command=self.show_main_menu)
        logout_button.pack(pady=5)
    
    
    
    def delete_user(self):
        selected_item = self.my_tree.selection()
        if selected_item:
            user_id = self.my_tree.item(selected_item, 'values')[0]  # Get the ID of the selected user
            self.c.execute("DELETE FROM users WHERE id=?", (user_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "User  deleted successfully.")
            self.show_admin_dashboard()
        else:
            messagebox.showwarning("Selection Error", "Please select a user to delete.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.show_main_menu
        self.root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = ElecTrack(root)
    app.run()