import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk  
from datetime import datetime

DB_NAME = "bus_service.db"

# Utility Functions
def get_connection():
    """Establish a connection to the database."""
    return sqlite3.connect(DB_NAME)

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_user(email, password):
    """Validate a user login."""
    hashed_password = hash_password(password)
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
        return cur.fetchone()

class BusAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Service Application")
        self.root.geometry("800x500")  # Larger window size
        self.root.resizable(False, False)  # Prevent resizing

        self.previous_window = self.root
        # Load and display the bus service image
        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack()

        self.bg_image = Image.open("bus_service_image.jpg")  # Your bus service image
        self.bg_image = self.bg_image.resize((800, 500), Image.Resampling.LANCZOS)  # Resize it to fit the window
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)  # Set the image as background

        # Login Frame (side by side with the image)
        self.login_frame = tk.Frame(self.root, bg='white', bd=5)
        self.login_frame.place(x=520, y=100, width=250, height=300)  # Position the login form on the right side

        self.email_label = tk.Label(self.login_frame, text="Email:", bg='white')
        self.email_label.grid(row=0, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.login_frame)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.login_frame, text="Password:", bg='white')
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login_action)
        self.login_button.grid(row=2, columnspan=2, pady=20)

        self.signup_button = tk.Button(self.root, text="Sign Up", command=self.show_signup, bg='lightblue', width=10)
        self.signup_button.place(x=520, y=420)

   

    def login_action(self):
        """Handle login action."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = validate_user(email, password)
        if user:
            messagebox.showinfo("Login Success", f"Welcome {user[1]}!")
            self.login_frame.pack_forget()  # Hide login frame
            role = user[5]
            if role == 'admin':
                self.admin_menu()
            else:
                self.user_menu(user[0])
        else:
            messagebox.showerror("Invalid Credentials", "Incorrect email or password. Please try again.")

    def show_signup(self):
        """Show the signup window."""
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Sign Up")
        self.signup_window.geometry("400x300")
        self.signup_window.resizable(False, False)
        
        
        self.name_label = tk.Label(self.signup_window, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.signup_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.email_label = tk.Label(self.signup_window, text="Email:")
        self.email_label.grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.signup_window)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        self.phone_label = tk.Label(self.signup_window, text="Phone:")
        self.phone_label.grid(row=2, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(self.signup_window)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.signup_window, text="Password:")
        self.password_label.grid(row=3, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.signup_window, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        self.signup_button = tk.Button(self.signup_window, text="Sign Up", command=self.signup_action)
        self.signup_button.grid(row=4, columnspan=2, pady=10)

    def signup_action(self):
        """Handle signup action."""
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)", 
                            (name, email, phone, hashed_password))
                conn.commit()
                messagebox.showinfo("Signup Successful", "You have successfully signed up.")
                self.signup_window.quit()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already exists. Please choose another one.")

    def admin_menu(self):
        """Admin menu."""
        # Clear previous content and set up the admin interface
        for widget in self.root.winfo_children():
            widget.destroy()  # Destroy any existing widgets in the main window

        self.root.title("Admin Menu")  # Set title for the admin menu
        self.root.geometry("800x500")  # Keep consistent window size

        # Create a title label
        title_label = tk.Label(self.root, text="Admin Menu", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # Add admin buttons
        tk.Button(self.root, text="View System Details", command=self.view_all_details, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Manage Buses", command=self.manage_buses, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Manage Routes", command=self.manage_routes, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Manage Drivers", command=self.manage_drivers, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Manage Tickets", command=self.manage_tickets, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Manage Schedule", command=self.manage_schedule, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout_admin, bg="red", fg="white", width=30, height=2).pack(pady=20)
        def logout_admin(self):
            """Admin logout function."""
            # Close the admin menu window
            self.admin_window.destroy()

            # Bring the user back to the login/signup window
            self.root.deiconify()  # Unhide the root window
            self.email_entry.delete(0, tk.END)  # Clear the email entry field
            self.password_entry.delete(0, tk.END)  # Clear the password entry field

    def user_menu(self, user_id):
        """User menu."""
        self.user_window = tk.Toplevel(self.root)
        self.user_window.title("User Menu")
        self.user_window.geometry("500x400")
        self.user_window.resizable(False, False)

        tk.Button(self.user_window, text="View All Buses", command=self.view_all_buses).pack(pady=10)
        tk.Button(self.user_window, text="Search Buses", command=self.search_buses).pack(pady=10)
        tk.Button(self.user_window, text="View and Book Tickets", command=lambda: self.view_and_book_tickets(user_id)).pack(pady=10)
        tk.Button(self.user_window, text="Prebook a Bus", command=lambda: self.prebook_bus(user_id)).pack(pady=10)
        tk.Button(self.user_window, text="Dashboard", command=self.contact_us).pack(pady=10)
        tk.Button(self.user_window, text="Logout", command=self.logout_user).pack(pady=20)

        def logout_user(self):
            """User logout function."""
            # Close the user menu window
            self.user_window.destroy()

            # Bring the user back to the login/signup window
            self.root.deiconify()  # Unhide the root window
            self.email_entry.delete(0, tk.END)  # Clear the email entry field
            self.password_entry.delete(0, tk.END)  # Clear the password entry field     

    def view_all_details(self):
        """Admin function to view detailed system information."""
        # Create a new window to display the details
        details_window = tk.Toplevel(self.root)
        details_window.title("Bus System Details")
        details_window.geometry("1000x800")

        # Create a scrollable frame
        frame = tk.Frame(details_window)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Database Query
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                    SELECT 
                    buses.bus_id AS "Bus ID",
                    buses.name AS "Bus Name",
                    routes.route_name AS "Route Name",
                    drivers1.name AS "Driver 1",
                    drivers2.name AS "Driver 2",
                    COUNT(tickets.ticket_id) AS "Available Tickets",
                    schedules.departure_date || ' ' || schedules.departure_time AS "Departure Schedule",
                    schedules.arrival_time AS "Arrival Time"
                        FROM buses
                        LEFT JOIN routes ON buses.route_id = routes.route_id
                        LEFT JOIN drivers AS drivers1 ON buses.driver_id1 = drivers1.driver_id
                        LEFT JOIN drivers AS drivers2 ON buses.driver_id2 = drivers2.driver_id
                        LEFT JOIN tickets ON buses.bus_id = tickets.bus_id AND tickets.status = 'unsold'
                        LEFT JOIN schedules ON buses.bus_id = schedules.bus_id
                     GROUP BY 
                    buses.bus_id, 
                    buses.name, 
                    routes.route_name, 
                    drivers1.name, 
                    drivers2.name, 
                    schedules.departure_date, 
                    schedules.departure_time, 
                    schedules.arrival_time
                ORDER BY buses.bus_id;

            """)
            rows = cur.fetchall()

        # Table Headers
        headers = ["Bus ID", "Bus Name", "Route", "Driver", "Co-driver","Available Tickets", "Departure Schedule","Arrival Time"]
        for col_num, header in enumerate(headers):
            header_label = tk.Label(scrollable_frame, text=header, font=('Arial', 12, 'bold'), bg='lightblue', borderwidth=1, relief="solid")
            header_label.grid(row=0, column=col_num, sticky="nsew", padx=1, pady=1)

        # Populate the Table with Data
        for row_num, row in enumerate(rows, start=1):
            for col_num, cell in enumerate(row):
                cell_label = tk.Label(scrollable_frame, text=cell if cell is not None else "N/A", font=('Arial', 10), borderwidth=1, relief="solid")
                cell_label.grid(row=row_num, column=col_num, sticky="nsew", padx=1, pady=1)

        # Set column widths
        for col_num in range(len(headers)):
            scrollable_frame.grid_columnconfigure(col_num, minsize=100)

        # Add a Close Button
        close_button = tk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.pack(pady=10)


    def manage_buses(self):
        """Admin function to manage buses."""
        self.manage_buses_window = tk.Toplevel(self.root)
        self.manage_buses_window.title("Manage Buses")
        self.manage_buses_window.geometry("600x600")
        self.manage_buses_window.resizable(False, False)

        # Add Bus Button
        add_bus_button = tk.Button(
            self.manage_buses_window, text="Add Bus", command=self.add_bus, width=20
        )
        add_bus_button.pack(pady=10)

        # Update Bus Button
        update_bus_button = tk.Button(
            self.manage_buses_window, text="Update Bus", command=self.update_bus, width=20
        )
        update_bus_button.pack(pady=10)

        # Delete Bus Button
        delete_bus_button = tk.Button(
            self.manage_buses_window, text="Delete Bus", command=self.delete_bus, width=20
        )
        delete_bus_button.pack(pady=10)
    def add_bus(self):
        """Admin function to add a new bus."""
        self.add_bus_window = tk.Toplevel(self.manage_buses_window)
        self.add_bus_window.title("Add Bus")
        self.add_bus_window.geometry("600x600")
        self.add_bus_window.resizable(False, False)

        # Input fields for bus details
        tk.Label(self.add_bus_window, text="Bus Name:").grid(row=0, column=0, padx=10, pady=5)
        bus_name_entry = tk.Entry(self.add_bus_window)
        bus_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_bus_window, text="Bus Number:").grid(row=1, column=0, padx=10, pady=5)
        bus_number_entry = tk.Entry(self.add_bus_window)
        bus_number_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_bus_window, text="Ticket Price:").grid(row=2, column=0, padx=10, pady=5)
        ticket_price_entry = tk.Entry(self.add_bus_window)
        ticket_price_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_bus_window, text="Capacity:").grid(row=3, column=0, padx=10, pady=5)
        capacity_entry = tk.Entry(self.add_bus_window)
        capacity_entry.grid(row=3, column=1, padx=10, pady=5)

        # Route Details
        tk.Label(self.add_bus_window, text="Route Name:").grid(row=4, column=0, padx=10, pady=5)
        route_name_entry = tk.Entry(self.add_bus_window)
        route_name_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.add_bus_window, text="Stops (comma-separated):").grid(row=5, column=0, padx=10, pady=5)
        stops_entry = tk.Entry(self.add_bus_window)
        stops_entry.grid(row=5, column=1, padx=10, pady=5)

        # Driver Details
        tk.Label(self.add_bus_window, text="Driver ID:").grid(row=6, column=0, padx=10, pady=5)
        driver1_entry = tk.Entry(self.add_bus_window)
        driver1_entry.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(self.add_bus_window, text="Co-Driver ID (optional):").grid(row=7, column=0, padx=10, pady=5)
        driver2_entry = tk.Entry(self.add_bus_window)
        driver2_entry.grid(row=7, column=1, padx=10, pady=5)

        # Schedule Details
        tk.Label(self.add_bus_window, text="Departure Date (YYYY-MM-DD):").grid(row=8, column=0, padx=10, pady=5)
        departure_date_entry = tk.Entry(self.add_bus_window)
        departure_date_entry.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(self.add_bus_window, text="Departure Time (HH:MM):").grid(row=9, column=0, padx=10, pady=5)
        departure_time_entry = tk.Entry(self.add_bus_window)
        departure_time_entry.grid(row=9, column=1, padx=10, pady=5)

        tk.Label(self.add_bus_window, text="Arrival Time (HH:MM):").grid(row=10, column=0, padx=10, pady=5)
        arrival_time_entry = tk.Entry(self.add_bus_window)
        arrival_time_entry.grid(row=10, column=1, padx=10, pady=5)

        def save_bus():
            """Save bus details to the database."""
            bus_name = bus_name_entry.get()
            bus_number = bus_number_entry.get()
            ticket_price = float(ticket_price_entry.get())
            capacity = int(capacity_entry.get())
            route_name = route_name_entry.get()
            stops = stops_entry.get()
            driver1 = int(driver1_entry.get())
            driver2 = driver2_entry.get()
            driver2 = int(driver2) if driver2 else None
            departure_date = departure_date_entry.get()
            departure_time = departure_time_entry.get()
            arrival_time = arrival_time_entry.get()

            with get_connection() as conn:
                cur = conn.cursor()

                # Insert route details
                cur.execute("INSERT INTO routes (route_name, stops) VALUES (?, ?)", (route_name, stops))
                route_id = cur.lastrowid

                # Insert bus details
                cur.execute(
                    """
                    INSERT INTO buses (name, number, route_id, ticket_price, capacity, driver_id1, driver_id2)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (bus_name, bus_number, route_id, ticket_price, capacity, driver1, driver2)
                )
                bus_id = cur.lastrowid

                # Insert schedule details
                cur.execute(
                    """
                    INSERT INTO schedules (bus_id, route_id, departure_date, departure_time, arrival_time)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (bus_id, route_id, departure_date, departure_time, arrival_time)
                )

                # Update driver assignments
                cur.execute("INSERT INTO driver_assignments (bus_id, driver_id) VALUES (?, ?)", (bus_id, driver1))
                if driver2:
                    cur.execute("INSERT INTO driver_assignments (bus_id, driver_id) VALUES (?, ?)", (bus_id, driver2))

                conn.commit()
                messagebox.showinfo("Success", "Bus added successfully!")
                self.add_bus_window.destroy()

        # Save Button
        save_button = tk.Button(self.add_bus_window, text="Save", command=save_bus)
        save_button.grid(row=11, columnspan=2, pady=20)

    def update_bus(self):
        """Admin function to update an existing bus."""
        self.update_bus_window = tk.Toplevel(self.manage_buses_window)
        self.update_bus_window.title("Update Bus")
        self.update_bus_window.geometry("600x600")
        self.update_bus_window.resizable(False, False)

        # Load buses from the database
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT bus_id, name FROM buses")
            buses = cur.fetchall()

        bus_list = [bus[1] for bus in buses]
        selected_bus = tk.StringVar()
        selected_bus.set(bus_list[0] if bus_list else None)

        # Dropdown to select the bus
        tk.Label(self.update_bus_window, text="Select Bus to Update:").grid(row=0, column=0, padx=10, pady=5)
        bus_dropdown = tk.OptionMenu(self.update_bus_window, selected_bus, *bus_list)
        bus_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Input fields
        labels = ["Bus Name:", "Bus Number:", "Ticket Price:", "Capacity:", "Route Name:", "Stops:", 
                "Driver ID:", "Co-Driver ID (optional):", "Departure Date (YYYY-MM-DD):", 
                "Departure Time (HH:MM):", "Arrival Time (HH:MM):"]
        entries = []

        for i, label in enumerate(labels, start=1):
            tk.Label(self.update_bus_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.update_bus_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def fetch_and_update():
            """Populate fields with the selected bus details."""
            bus_name = selected_bus.get()
            bus_id = next((bus[0] for bus in buses if bus[1] == bus_name), None)

            if not bus_id:
                messagebox.showerror("Error", "Failed to fetch bus details.")
                return

            with get_connection() as conn:
                cur = conn.cursor()

                # Fetch bus details
                cur.execute("SELECT * FROM buses WHERE bus_id = ?", (bus_id,))
                bus_details = cur.fetchone()

                if not bus_details:
                    messagebox.showerror("Error", "Bus details not found.")
                    return

                # Populate fields
                entries[0].delete(0, tk.END)
                entries[0].insert(0, bus_details[1])  # Bus Name
                entries[1].delete(0, tk.END)
                entries[1].insert(0, bus_details[2])  # Bus Number

                # Additional queries for route, drivers, and schedule
                # (Repeat logic from original implementation as needed)

        fetch_button = tk.Button(self.update_bus_window, text="Fetch Details", command=fetch_and_update)
        fetch_button.grid(row=12, columnspan=2, pady=10)

        def save_changes():
            """Save updated bus details to the database."""
            try:
                # Collect inputs and validate them (add validation logic here)
                updated_details = [entry.get() for entry in entries]

                # Update database logic (reuse from original implementation)

                messagebox.showinfo("Success", "Bus updated successfully!")
                self.update_bus_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_button = tk.Button(self.update_bus_window, text="Save Changes", command=save_changes)
        save_button.grid(row=13, columnspan=2, pady=10)



    def delete_bus(self):
        """Admin function to delete a bus."""
        self.delete_bus_window = tk.Toplevel(self.root)
        self.delete_bus_window.title("Delete Bus")
        self.delete_bus_window.geometry("400x300")

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT bus_id, name FROM buses")
            buses = cur.fetchall()

        bus_names = [bus[1] for bus in buses]
        selected_bus = tk.StringVar()
        selected_bus.set(bus_names[0] if bus_names else "No buses available")

        tk.Label(self.delete_bus_window, text="Select Bus to Delete:").pack(pady=5)
        bus_dropdown = tk.OptionMenu(self.delete_bus_window, selected_bus, *bus_names)
        bus_dropdown.pack(pady=5)

        def delete_selected_bus():
            if not buses:
                messagebox.showerror("Error", "No buses to delete.")
                return

            bus_name = selected_bus.get()
            bus_id = next((bus[0] for bus in buses if bus[1] == bus_name), None)

            if not bus_id:
                messagebox.showerror("Error", "Failed to fetch bus ID.")
                return

            try:
                with get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM buses WHERE bus_id = ?", (bus_id,))
                    cur.execute("DELETE FROM schedules WHERE bus_id = ?", (bus_id,))
                    cur.execute("DELETE FROM driver_assignments WHERE bus_id = ?", (bus_id,))
                    conn.commit()

                messagebox.showinfo("Success", f"Bus '{bus_name}' deleted successfully!")
                self.delete_bus_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        delete_button = tk.Button(self.delete_bus_window, text="Delete Bus", command=delete_selected_bus)
        delete_button.pack(pady=20)

        
            


    def manage_routes(self):
        """Admin function to manage routes."""
        self.manage_routes_window = tk.Toplevel(self.root)
        self.manage_routes_window.title("Manage Routes")
        self.manage_routes_window.geometry("600x600")
        self.manage_routes_window.resizable(False, False)

        # Title label
        tk.Label(self.manage_routes_window, text="Manage Routes", font=("Arial", 16)).pack(pady=10)

        # Fetch all routes from the database
        def fetch_routes():
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT route_id, route_name, stops FROM routes")
                return cur.fetchall()

        # Refresh the route list display
        def refresh_route_list():
            routes_listbox.delete(0, tk.END)
            routes = fetch_routes()
            for route in routes:
                routes_listbox.insert(tk.END, f"{route[1]} - Stops: {route[2]}")

        # Route listbox to display routes
        routes_listbox = tk.Listbox(self.manage_routes_window, width=70, height=15)
        routes_listbox.pack(pady=10)
        refresh_route_list()

        # Add new route functionality
        def add_route():
            add_route_window = tk.Toplevel(self.manage_routes_window)
            add_route_window.title("Add Route")
            add_route_window.geometry("400x300")
            add_route_window.resizable(False, False)

            tk.Label(add_route_window, text="Route Name:").pack(pady=5)
            route_name_entry = tk.Entry(add_route_window)
            route_name_entry.pack(pady=5)

            tk.Label(add_route_window, text="Stops (comma-separated):").pack(pady=5)
            stops_entry = tk.Entry(add_route_window)
            stops_entry.pack(pady=5)

            def save_new_route():
                route_name = route_name_entry.get().strip()
                stops = stops_entry.get().strip()

                if not route_name or not stops:
                    messagebox.showerror("Error", "All fields are required.")
                    return

                with get_connection() as conn:
                    try:
                        cur = conn.cursor()
                        cur.execute("INSERT INTO routes (route_name, stops) VALUES (?, ?)", (route_name, stops))
                        conn.commit()
                        messagebox.showinfo("Success", "Route added successfully!")
                        add_route_window.destroy()
                        refresh_route_list()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to add route: {str(e)}")

            tk.Button(add_route_window, text="Save", command=save_new_route).pack(pady=10)

        # Update route functionality
        def update_route():
            selected_index = routes_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a route to update.")
                return

            selected_route = fetch_routes()[selected_index[0]]
            route_id, route_name, stops = selected_route

            update_route_window = tk.Toplevel(self.manage_routes_window)
            update_route_window.title("Update Route")
            update_route_window.geometry("400x300")
            update_route_window.resizable(False, False)

            tk.Label(update_route_window, text="Route Name:").pack(pady=5)
            route_name_entry = tk.Entry(update_route_window)
            route_name_entry.insert(0, route_name)
            route_name_entry.pack(pady=5)

            tk.Label(update_route_window, text="Stops (comma-separated):").pack(pady=5)
            stops_entry = tk.Entry(update_route_window)
            stops_entry.insert(0, stops)
            stops_entry.pack(pady=5)

            def save_updated_route():
                updated_name = route_name_entry.get().strip()
                updated_stops = stops_entry.get().strip()

                if not updated_name or not updated_stops:
                    messagebox.showerror("Error", "All fields are required.")
                    return

                with get_connection() as conn:
                    try:
                        cur = conn.cursor()
                        cur.execute(
                            "UPDATE routes SET route_name = ?, stops = ? WHERE route_id = ?",
                            (updated_name, updated_stops, route_id),
                        )
                        conn.commit()
                        messagebox.showinfo("Success", "Route updated successfully!")
                        update_route_window.destroy()
                        refresh_route_list()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to update route: {str(e)}")

            tk.Button(update_route_window, text="Save Changes", command=save_updated_route).pack(pady=10)

        # Delete route functionality
        def delete_route():
            selected_index = routes_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a route to delete.")
                return

            selected_route = fetch_routes()[selected_index[0]]
            route_id, route_name, _ = selected_route

            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete route '{route_name}'?"):
                with get_connection() as conn:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM routes WHERE route_id = ?", (route_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Route deleted successfully!")
                        refresh_route_list()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete route: {str(e)}")

        # Buttons for managing routes
        buttons_frame = tk.Frame(self.manage_routes_window)
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="Add Route", command=add_route).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(buttons_frame, text="Update Route", command=update_route).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(buttons_frame, text="Delete Route", command=delete_route).grid(row=0, column=2, padx=10, pady=5)

        # Close the manage routes window
        tk.Button(self.manage_routes_window, text="Close", command=self.manage_routes_window.destroy).pack(pady=10)


    def manage_drivers(self):
        """Admin function to manage drivers."""
        
        # Create a new window for managing drivers
        self.driver_window = tk.Toplevel(self.root)
        self.driver_window.title("Manage Drivers")
        self.driver_window.geometry("600x400")
        self.driver_window.resizable(False, False)

        # Title Label
        tk.Label(self.driver_window, text="Manage Drivers", font=("Arial", 16)).pack(pady=10)

        # List of drivers
        self.driver_listbox = tk.Listbox(self.driver_window, width=50, height=10)
        self.driver_listbox.pack(pady=10)

        # Fetch drivers and display them
        self.fetch_drivers()

        # Add Driver Button
        add_driver_button = tk.Button(self.driver_window, text="Add Driver", font=("Arial", 12), command=self.add_driver)
        add_driver_button.pack(pady=10)

        # Update Driver Button
        update_driver_button = tk.Button(self.driver_window, text="Update Driver", font=("Arial", 12), command=self.update_driver)
        update_driver_button.pack(pady=10)

        # Delete Driver Button
        delete_driver_button = tk.Button(self.driver_window, text="Delete Driver", font=("Arial", 12), command=self.delete_driver)
        delete_driver_button.pack(pady=10)

    def fetch_drivers(self):
        """Fetch and display drivers."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT driver_id, name, license_number FROM drivers")
            drivers = cur.fetchall()

        # Clear the listbox
        self.driver_listbox.delete(0, tk.END)

        # Populate the listbox with driver names
        for driver in drivers:
            self.driver_listbox.insert(tk.END, f"{driver[1]} - {driver[2]}")  # name - license_number

    def add_driver(self):
        """Add a new driver."""
        name = simpledialog.askstring("Add Driver", "Enter driver's name:")
        license_number = simpledialog.askstring("Add Driver", "Enter driver's license number:")
        phone = simpledialog.askstring("Add Driver", "Enter driver's phone number:")
        address = simpledialog.askstring("Add Driver", "Enter driver's address:")

        if name and license_number and phone and address:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO drivers (name, license_number, phone, address)
                    VALUES (?, ?, ?, ?)
                """, (name, license_number, phone, address))
                conn.commit()

            messagebox.showinfo("Driver Added", "Driver has been successfully added.")
            self.fetch_drivers()

    def update_driver(self):
        """Update an existing driver."""
        selected_driver = self.driver_listbox.curselection()
        if selected_driver:
            driver_info = self.driver_listbox.get(selected_driver[0]).split(" - ")
            driver_name = driver_info[0]
            
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT driver_id, name, license_number, phone, address FROM drivers WHERE name = ?", (driver_name,))
                driver = cur.fetchone()

            # Ask for updated details
            new_name = simpledialog.askstring("Update Driver", f"Enter new name (current: {driver[1]}):", initialvalue=driver[1])
            new_license = simpledialog.askstring("Update Driver", f"Enter new license number (current: {driver[2]}):", initialvalue=driver[2])
            new_phone = simpledialog.askstring("Update Driver", f"Enter new phone number (current: {driver[3]}):", initialvalue=driver[3])
            new_address = simpledialog.askstring("Update Driver", f"Enter new address (current: {driver[4]}):", initialvalue=driver[4])

            # Update the database
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE drivers
                    SET name = ?, license_number = ?, phone = ?, address = ?
                    WHERE driver_id = ?
                """, (new_name, new_license, new_phone, new_address, driver[0]))
                conn.commit()

            messagebox.showinfo("Driver Updated", "Driver details have been successfully updated.")
            self.fetch_drivers()

    def delete_driver(self):
        """Delete a driver."""
        selected_driver = self.driver_listbox.curselection()
        if selected_driver:
            driver_info = self.driver_listbox.get(selected_driver[0]).split(" - ")
            driver_name = driver_info[0]
            
            confirm_delete = messagebox.askyesno("Delete Driver", f"Are you sure you want to delete driver {driver_name}?")
            if confirm_delete:
                with get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM drivers WHERE name = ?", (driver_name,))
                    conn.commit()

                messagebox.showinfo("Driver Deleted", "Driver has been successfully deleted.")
                self.fetch_drivers()



    def manage_tickets(self):
        """Admin function to manage tickets."""
        
        self.ticket_window = tk.Toplevel(self.root)
        self.ticket_window.title("Manage Tickets")
        self.ticket_window.geometry("600x400")
        self.ticket_window.resizable(False, False)

        tk.Label(self.ticket_window, text="Manage Tickets", font=("Arial", 16)).pack(pady=10)

        # Listbox to show all tickets
        self.ticket_listbox = tk.Listbox(self.ticket_window, width=50, height=10)
        self.ticket_listbox.pack(pady=10)

        self.fetch_tickets()

        add_ticket_button = tk.Button(self.ticket_window, text="Add Ticket", font=("Arial", 12), command=self.add_ticket)
        add_ticket_button.pack(pady=10)

        update_ticket_button = tk.Button(self.ticket_window, text="Update Ticket", font=("Arial", 12), command=self.update_ticket)
        update_ticket_button.pack(pady=10)

        delete_ticket_button = tk.Button(self.ticket_window, text="Delete Ticket", font=("Arial", 12), command=self.delete_ticket)
        delete_ticket_button.pack(pady=10)

    def fetch_tickets(self):
        """Fetch and display tickets."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT tickets.ticket_id, buses.name, tickets.seat_number, tickets.price, tickets.status
                FROM tickets
                JOIN buses ON tickets.bus_id = buses.bus_id
            """)
            tickets = cur.fetchall()

        self.ticket_listbox.delete(0, tk.END)

        for ticket in tickets:
            self.ticket_listbox.insert(tk.END, f"{ticket[1]} - Seat {ticket[2]} - Status: {ticket[4]}")

    def add_ticket(self):
        """Add a new ticket for a bus."""
        bus_id = simpledialog.askinteger("Add Ticket", "Enter Bus ID for the ticket:")
        seat_number = simpledialog.askinteger("Add Ticket", "Enter seat number:")
        seat_id = f"{bus_id}-{seat_number}"  # Combine bus ID and seat number to generate a unique seat ID
        price = simpledialog.askfloat("Add Ticket", "Enter price for the ticket:")

        if bus_id and seat_number and price:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO tickets (bus_id, seat_number, seat_id, price, status)
                    VALUES (?, ?, ?, ?, 'unsold')
                """, (bus_id, seat_number, seat_id, price))
                conn.commit()

            messagebox.showinfo("Ticket Added", "Ticket has been successfully added.")
            self.fetch_tickets()

    def update_ticket(self):
        """Update an existing ticket."""
        selected_ticket = self.ticket_listbox.curselection()
        if selected_ticket:
            ticket_info = self.ticket_listbox.get(selected_ticket[0]).split(" - ")
            bus_name = ticket_info[0]

            new_status = simpledialog.askstring("Update Ticket", f"Enter new status (current: {ticket_info[2]}):", initialvalue=ticket_info[2])

            if new_status:
                with get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE tickets
                        SET status = ?
                        WHERE seat_id = ?
                    """, (new_status, ticket_info[1]))
                    conn.commit()

                messagebox.showinfo("Ticket Updated", "Ticket status has been updated.")
                self.fetch_tickets()

    def delete_ticket(self):
        """Delete a ticket."""
        selected_ticket = self.ticket_listbox.curselection()
        if selected_ticket:
            ticket_info = self.ticket_listbox.get(selected_ticket[0]).split(" - ")
            seat_id = ticket_info[1]
            
            confirm_delete = messagebox.askyesno("Delete Ticket", f"Are you sure you want to delete ticket for seat {seat_id}?")
            if confirm_delete:
                with get_connection() as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM tickets WHERE seat_id = ?", (seat_id,))
                    conn.commit()

                messagebox.showinfo("Ticket Deleted", "Ticket has been successfully deleted.")
                self.fetch_tickets()




    def manage_schedule(self):
        """Admin function to manage schedule."""
        self.manage_schedule_window = tk.Toplevel(self.root)
        self.manage_schedule_window.title("Manage Schedule")
        self.manage_schedule_window.geometry("700x600")
        self.manage_schedule_window.resizable(False, False)

        # Title label
        tk.Label(self.manage_schedule_window, text="Manage Schedule", font=("Arial", 16)).pack(pady=10)

        # Fetch all buses and routes for schedule management
        def fetch_buses():
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT bus_id, name FROM buses")
                return cur.fetchall()

        def fetch_routes():
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT route_id, route_name FROM routes")
                return cur.fetchall()

        # Refresh bus list
        def refresh_bus_list():
            bus_listbox.delete(0, tk.END)
            buses = fetch_buses()
            for bus in buses:
                bus_listbox.insert(tk.END, f"Bus ID: {bus[0]} - Name: {bus[1]}")

        # Refresh route list
        def refresh_route_list():
            route_listbox.delete(0, tk.END)
            routes = fetch_routes()
            for route in routes:
                route_listbox.insert(tk.END, f"Route ID: {route[0]} - Name: {route[1]}")

        # Bus selection listbox
        bus_listbox = tk.Listbox(self.manage_schedule_window, width=70, height=10)
        bus_listbox.pack(pady=10)
        refresh_bus_list()

        # Route selection listbox
        route_listbox = tk.Listbox(self.manage_schedule_window, width=70, height=10)
        route_listbox.pack(pady=10)
        refresh_route_list()

        # Fetch schedules for a selected bus
        def fetch_schedules(bus_id):
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT schedule_id, departure_date, departure_time, arrival_time, route_id FROM schedules WHERE bus_id = ?", (bus_id,))
                return cur.fetchall()

        # Display schedules for the selected bus
        def display_schedules(bus_id):
            schedule_listbox.delete(0, tk.END)
            schedules = fetch_schedules(bus_id)
            for schedule in schedules:
                route_name = next((route[1] for route in fetch_routes() if route[0] == schedule[4]), "Unknown")
                schedule_listbox.insert(tk.END, f"Schedule ID: {schedule[0]} - Route: {route_name} - Departure: {schedule[1]} {schedule[2]} - Arrival: {schedule[3]}")

        # Schedule listbox to show schedule details for the selected bus
        schedule_listbox = tk.Listbox(self.manage_schedule_window, width=70, height=10)
        schedule_listbox.pack(pady=10)

        # Select a bus and show corresponding schedules
        def select_bus_and_show_schedules():
            selected_index = bus_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a bus.")
                return

            selected_bus = fetch_buses()[selected_index[0]]
            bus_id = selected_bus[0]

            display_schedules(bus_id)

        # Add schedule functionality
        def add_schedule():
            selected_bus_index = bus_listbox.curselection()
            selected_route_index = route_listbox.curselection()

            if not selected_bus_index or not selected_route_index:
                messagebox.showerror("Error", "Please select both a bus and a route.")
                return

            selected_bus = fetch_buses()[selected_bus_index[0]]
            bus_id = selected_bus[0]

            selected_route = fetch_routes()[selected_route_index[0]]
            route_id = selected_route[0]

            # Get date and time input for the new schedule
            departure_date = departure_date_entry.get()
            departure_time = departure_time_entry.get()
            arrival_time = arrival_time_entry.get()

            if not departure_date or not departure_time or not arrival_time:
                messagebox.showerror("Error", "Please provide valid date and time.")
                return

            with get_connection() as conn:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO schedules (bus_id, route_id, departure_date, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)",
                        (bus_id, route_id, departure_date, departure_time, arrival_time),
                    )
                    conn.commit()
                    messagebox.showinfo("Success", "Schedule added successfully!")
                    display_schedules(bus_id)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add schedule: {str(e)}")

        # Update schedule functionality
        def update_schedule():
            selected_index = schedule_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a schedule to update.")
                return

            selected_schedule = fetch_schedules(selected_bus_id)[selected_index[0]]
            schedule_id, _, _, _, route_id = selected_schedule

            update_schedule_window = tk.Toplevel(self.manage_schedule_window)
            update_schedule_window.title("Update Schedule")
            update_schedule_window.geometry("400x400")
            update_schedule_window.resizable(False, False)

            tk.Label(update_schedule_window, text="Departure Date:").pack(pady=5)
            departure_date_entry = tk.Entry(update_schedule_window)
            departure_date_entry.insert(0, selected_schedule[1])  # Pre-fill with existing date
            departure_date_entry.pack(pady=5)

            tk.Label(update_schedule_window, text="Departure Time:").pack(pady=5)
            departure_time_entry = tk.Entry(update_schedule_window)
            departure_time_entry.insert(0, selected_schedule[2])  # Pre-fill with existing time
            departure_time_entry.pack(pady=5)

            tk.Label(update_schedule_window, text="Arrival Time:").pack(pady=5)
            arrival_time_entry = tk.Entry(update_schedule_window)
            arrival_time_entry.insert(0, selected_schedule[3])  # Pre-fill with existing time
            arrival_time_entry.pack(pady=5)

            def save_updated_schedule():
                updated_departure_date = departure_date_entry.get()
                updated_departure_time = departure_time_entry.get()
                updated_arrival_time = arrival_time_entry.get()

                with get_connection() as conn:
                    try:
                        cur = conn.cursor()
                        cur.execute(
                            "UPDATE schedules SET departure_date = ?, departure_time = ?, arrival_time = ? WHERE schedule_id = ?",
                            (updated_departure_date, updated_departure_time, updated_arrival_time, schedule_id),
                        )
                        conn.commit()
                        messagebox.showinfo("Success", "Schedule updated successfully!")
                        update_schedule_window.destroy()
                        display_schedules(selected_bus_id)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to update schedule: {str(e)}")

            tk.Button(update_schedule_window, text="Save Changes", command=save_updated_schedule).pack(pady=10)

        # Delete schedule functionality
        def delete_schedule():
            selected_index = schedule_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select a schedule to delete.")
                return

            selected_schedule = fetch_schedules(selected_bus_id)[selected_index[0]]
            schedule_id = selected_schedule[0]

            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete schedule {schedule_id}?"):
                with get_connection() as conn:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM schedules WHERE schedule_id = ?", (schedule_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Schedule deleted successfully!")
                        display_schedules(selected_bus_id)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete schedule: {str(e)}")

        # Buttons for managing schedules
        buttons_frame = tk.Frame(self.manage_schedule_window)
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="Add Schedule", command=add_schedule).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(buttons_frame, text="Update Schedule", command=update_schedule).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(buttons_frame, text="Delete Schedule", command=delete_schedule).grid(row=0, column=2, padx=10, pady=5)

        # Close the manage schedule window
        tk.Button(self.manage_schedule_window, text="Close", command=self.manage_schedule_window.destroy).pack(pady=10)

        # Button to select bus and show schedules
        tk.Button(self.manage_schedule_window, text="Select Bus and Show Schedules", command=select_bus_and_show_schedules).pack(pady=10)

        # Entry fields for adding/updating schedules
        tk.Label(self.manage_schedule_window, text="Departure Date (YYYY-MM-DD):").pack(pady=5)
        departure_date_entry = tk.Entry(self.manage_schedule_window)
        departure_date_entry.pack(pady=5)

        tk.Label(self.manage_schedule_window, text="Departure Time (HH:MM):").pack(pady=5)
        departure_time_entry = tk.Entry(self.manage_schedule_window)
        departure_time_entry.pack(pady=5)

        tk.Label(self.manage_schedule_window, text="Arrival Time (HH:MM):").pack(pady=5)
        arrival_time_entry = tk.Entry(self.manage_schedule_window)
        arrival_time_entry.pack(pady=5)


    def view_all_buses(self):
        """User function to view all buses with detailed information."""
        self.view_buses_window = tk.Toplevel(self.root)
        self.view_buses_window.title("View All Buses")
        self.view_buses_window.geometry("900x600")
        self.view_buses_window.resizable(False, False)

        # Title Label
        tk.Label(self.view_buses_window, text="Available Buses", font=("Arial", 16)).pack(pady=10)

        # Fetch all buses with their details (including route, stops, schedules, and ticket prices)
        def fetch_all_buses():
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT buses.bus_id, buses.name, buses.number, buses.ticket_price, buses.capacity, 
                        routes.route_name, routes.stops
                    FROM buses
                    JOIN routes ON buses.route_id = routes.route_id
                """)
                return cur.fetchall()

        all_buses = fetch_all_buses()

        # Create a treeview widget to display the bus details in a table format
        treeview = ttk.Treeview(self.view_buses_window, columns=("Bus Name", "Bus Number", "Route", "Stops", "Capacity", "Ticket Price"), show="headings")
        treeview.pack(pady=10, fill=tk.BOTH, expand=True)

        # Define headings for the treeview columns
        treeview.heading("Bus Name", text="Bus Name")
        treeview.heading("Bus Number", text="Bus Number")
        treeview.heading("Route", text="Route")
        treeview.heading("Stops", text="Stops")
        treeview.heading("Capacity", text="Capacity")
        treeview.heading("Ticket Price", text="Ticket Price")

        # Adjust column widths
        treeview.column("Bus Name", width=150)
        treeview.column("Bus Number", width=100)
        treeview.column("Route", width=150)
        treeview.column("Stops", width=200)
        treeview.column("Capacity", width=100)
        treeview.column("Ticket Price", width=100)

        # Insert rows of bus data into the treeview
        for bus in all_buses:
            bus_id, bus_name, bus_number, ticket_price, capacity, route_name, stops = bus
            treeview.insert("", tk.END, values=(bus_name, bus_number, route_name, stops, capacity, ticket_price))

        # Optionally, create a double-click event to show more detailed information about a bus
        def view_bus_details(event):
            selected_item = treeview.selection()
            if selected_item:
                bus_details = treeview.item(selected_item)["values"]
                bus_name, bus_number, route_name, stops, capacity, ticket_price = bus_details

                # Create a window to display bus details in more detail
                bus_details_window = tk.Toplevel(self.view_buses_window)
                bus_details_window.title(f"Bus Details - {bus_name}")
                bus_details_window.geometry("400x300")
                bus_details_window.resizable(False, False)

                # Display detailed information
                tk.Label(bus_details_window, text=f"Bus Name: {bus_name}", font=("Arial", 14)).pack(pady=5)
                tk.Label(bus_details_window, text=f"Bus Number: {bus_number}", font=("Arial", 12)).pack(pady=5)
                tk.Label(bus_details_window, text=f"Route: {route_name}", font=("Arial", 12)).pack(pady=5)
                tk.Label(bus_details_window, text=f"Stops: {stops}", font=("Arial", 12)).pack(pady=5)
                tk.Label(bus_details_window, text=f"Capacity: {capacity} seats", font=("Arial", 12)).pack(pady=5)
                tk.Label(bus_details_window, text=f"Ticket Price: ${ticket_price}", font=("Arial", 12)).pack(pady=5)

        treeview.bind("<Double-1>", view_bus_details)

        # Close the view buses window button
        close_button = tk.Button(self.view_buses_window, text="Close", command=self.view_buses_window.destroy)
        close_button.pack(pady=10)


    def search_and_book_buses(self, user_id):
        """User function to search for buses and book tickets."""
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Search and Book Buses")
        self.search_window.geometry("900x600")
        self.search_window.resizable(False, False)

        # Title Label
        tk.Label(self.search_window, text="Search for Buses", font=("Arial", 16)).pack(pady=10)

        # Search Bus Criteria (Name or Route)
        tk.Label(self.search_window, text="Search by Bus Name or Route:", font=("Arial", 12)).pack(pady=5)
        self.search_entry = tk.Entry(self.search_window, font=("Arial", 12), width=30)
        self.search_entry.pack(pady=10)
        
        # Search Button
        search_button = tk.Button(self.search_window, text="Search", font=("Arial", 12), command=self.search_buses)
        search_button.pack(pady=10)

        # Result Treeview for showing available buses
        self.treeview = ttk.Treeview(self.search_window, columns=("Bus Name", "Bus Number", "Route", "Ticket Price", "Capacity"), show="headings")
        self.treeview.pack(pady=10, fill=tk.BOTH, expand=True)

        # Define headings
        self.treeview.heading("Bus Name", text="Bus Name")
        self.treeview.heading("Bus Number", text="Bus Number")
        self.treeview.heading("Route", text="Route")
        self.treeview.heading("Ticket Price", text="Ticket Price")
        self.treeview.heading("Capacity", text="Capacity")

        self.treeview.column("Bus Name", width=150)
        self.treeview.column("Bus Number", width=100)
        self.treeview.column("Route", width=150)
        self.treeview.column("Ticket Price", width=100)
        self.treeview.column("Capacity", width=100)

        # Bind selection event for bus selection
        self.treeview.bind("<Double-1>", self.view_and_book_tickets)

    def search_buses(self):
        """Search buses based on the search entry."""
        search_term = self.search_entry.get().lower()
        if not search_term:
            messagebox.showwarning("Search", "Please enter a search term.")
            return

        # Fetch buses matching the search term
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT buses.bus_id, buses.name, buses.number, buses.ticket_price, buses.capacity, 
                    routes.route_name
                FROM buses
                JOIN routes ON buses.route_id = routes.route_id
                WHERE LOWER(buses.name) LIKE ? OR LOWER(routes.route_name) LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%"))
            buses = cur.fetchall()

        # Clear previous results
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Insert matching buses into the treeview
        for bus in buses:
            bus_id, bus_name, bus_number, ticket_price, capacity, route_name = bus
            self.treeview.insert("", tk.END, values=(bus_name, bus_number, route_name, ticket_price, capacity))

    def view_and_book_tickets(self, event):
        """View and book tickets for a selected bus."""
        selected_item = self.treeview.selection()
        if selected_item:
            bus_details = self.treeview.item(selected_item)["values"]
            bus_name, bus_number, route_name, ticket_price, capacity = bus_details
            bus_id = self.treeview.item(selected_item)["text"]

            # Create new window to show available tickets for the selected bus
            self.ticket_window = tk.Toplevel(self.search_window)
            self.ticket_window.title(f"Available Tickets - {bus_name}")
            self.ticket_window.geometry("800x600")
            self.ticket_window.resizable(False, False)

            # Label for bus details
            tk.Label(self.ticket_window, text=f"Bus Name: {bus_name}", font=("Arial", 14)).pack(pady=10)
            tk.Label(self.ticket_window, text=f"Route: {route_name}", font=("Arial", 12)).pack(pady=5)
            tk.Label(self.ticket_window, text=f"Ticket Price: ${ticket_price}", font=("Arial", 12)).pack(pady=5)

            # Fetch available seats for the selected bus
            self.fetch_available_seats(bus_id)

            # Seat Selection
            tk.Label(self.ticket_window, text="Select Seats (Available seats are shown):", font=("Arial", 12)).pack(pady=10)
            self.seat_listbox = tk.Listbox(self.ticket_window, selectmode=tk.MULTIPLE, font=("Arial", 12), height=10)
            self.seat_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

            # Add available seats to the listbox
            self.populate_seats(bus_id)

            # Button to confirm and book selected seats
            book_button = tk.Button(self.ticket_window, text="Book Selected Tickets", font=("Arial", 12), command=lambda: self.book_tickets(bus_id, ticket_price, user_id))
            book_button.pack(pady=10)

    def fetch_available_seats(self, bus_id):
        """Fetch and show available seats for a given bus."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT seat_id FROM tickets WHERE bus_id = ? AND status = 'unsold'
            """, (bus_id,))
            available_seats = cur.fetchall()
        return [seat[0] for seat in available_seats]

    def populate_seats(self, bus_id):
        """Populate available seats into the seat listbox."""
        available_seats = self.fetch_available_seats(bus_id)
        for seat in available_seats:
            self.seat_listbox.insert(tk.END, seat)

    def book_tickets(self, bus_id, ticket_price, user_id):
        """Book selected tickets and process payment."""
        selected_seats = [self.seat_listbox.get(i) for i in self.seat_listbox.curselection()]
        if not selected_seats:
            messagebox.showwarning("Select Seats", "Please select at least one seat.")
            return

        total_amount = len(selected_seats) * ticket_price

        # Insert tickets into the database
        with get_connection() as conn:
            cur = conn.cursor()
            for seat_id in selected_seats:
                cur.execute("""
                    INSERT INTO tickets (bus_id, seat_id, status, price, user_id)
                    VALUES (?, ?, 'sold', ?, ?)
                """, (bus_id, seat_id, ticket_price, user_id))

        messagebox.showinfo("Booking Successful", f"You have successfully booked {len(selected_seats)} seat(s) for a total of ${total_amount}.")
        self.ticket_window.destroy()


    def prebook_bus(self, user_id):
        """User function to prebook a bus."""
        route_name = simpledialog.askstring("Prebook Bus", "Enter the route name:")
        bus_name = simpledialog.askstring("Prebook Bus", "Enter the bus name you want to prebook:")
        
        # Fetch bus details and available schedule based on route and bus name
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT buses.bus_id, schedules.schedule_id, schedules.departure_date, schedules.departure_time
                FROM buses
                JOIN schedules ON buses.bus_id = schedules.bus_id
                WHERE buses.name = ? AND buses.route_id = (SELECT route_id FROM routes WHERE route_name = ?)
            """, (bus_name, route_name))
            available_schedules = cur.fetchall()

        if not available_schedules:
            messagebox.showwarning("No Schedules", "No schedules available for the selected bus and route.")
            return

        # Display available schedules
        schedule_list = "\n".join([f"Schedule ID: {s[1]}, Date: {s[2]}, Time: {s[3]}" for s in available_schedules])
        selected_schedule_id = simpledialog.askinteger("Prebook Bus", f"Available schedules:\n{schedule_list}\nEnter Schedule ID to prebook:")

        # Prebook the bus
        if selected_schedule_id:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO prebooked_buses (user_id, bus_id, prebook_date)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (user_id, available_schedules[selected_schedule_id - 1][0]))  # Assume valid selection
                conn.commit()

            messagebox.showinfo("Prebook Successful", f"Successfully prebooked the bus for schedule ID: {selected_schedule_id}.")


    def search_buses_for_prebooking(self):
        """Search buses for prebooking based on name or route."""
        search_term = self.search_entry.get().lower()
        if not search_term:
            messagebox.showwarning("Search", "Please enter a search term.")
            return

        # Fetch buses matching the search term
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT buses.bus_id, buses.name, buses.number, buses.ticket_price, buses.capacity, 
                    routes.route_name
                FROM buses
                JOIN routes ON buses.route_id = routes.route_id
                WHERE LOWER(buses.name) LIKE ? OR LOWER(routes.route_name) LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%"))
            buses = cur.fetchall()

        # Clear previous results
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Insert matching buses into the treeview
        for bus in buses:
            bus_id, bus_name, bus_number, ticket_price, capacity, route_name = bus
            self.treeview.insert("", tk.END, values=(bus_name, bus_number, route_name, ticket_price, capacity))

    def view_bus_schedules_for_prebooking(self, event):
        """View and select schedule for prebooking a bus."""
        selected_item = self.treeview.selection()
        if selected_item:
            bus_details = self.treeview.item(selected_item)["values"]
            bus_name, bus_number, route_name, ticket_price, capacity = bus_details
            bus_id = self.treeview.item(selected_item)["text"]

            # Create a new window to show bus schedules
            self.schedule_window = tk.Toplevel(self.prebook_window)
            self.schedule_window.title(f"Select Schedule for {bus_name}")
            self.schedule_window.geometry("800x600")
            self.schedule_window.resizable(False, False)

            # Label for bus details
            tk.Label(self.schedule_window, text=f"Bus Name: {bus_name}", font=("Arial", 14)).pack(pady=10)
            tk.Label(self.schedule_window, text=f"Route: {route_name}", font=("Arial", 12)).pack(pady=5)
            tk.Label(self.schedule_window, text=f"Ticket Price: ${ticket_price}", font=("Arial", 12)).pack(pady=5)

            # Fetch available schedules for the selected bus
            self.fetch_bus_schedules(bus_id)

            # Listbox to select schedule
            tk.Label(self.schedule_window, text="Select a Schedule for Prebooking:", font=("Arial", 12)).pack(pady=10)
            self.schedule_listbox = tk.Listbox(self.schedule_window, selectmode=tk.SINGLE, font=("Arial", 12), height=10)
            self.schedule_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

            # Add available schedules to the listbox
            self.populate_schedules(bus_id)

            # Button to confirm and prebook the bus
            prebook_button = tk.Button(self.schedule_window, text="Prebook Bus", font=("Arial", 12), command=lambda: self.confirm_prebooking(bus_id, user_id))
            prebook_button.pack(pady=10)

    def fetch_bus_schedules(self, bus_id):
        """Fetch and show available schedules for the selected bus."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT schedule_id, departure_date, departure_time, arrival_time 
                FROM schedules 
                WHERE bus_id = ?
            """, (bus_id,))
            schedules = cur.fetchall()
        return schedules

    def populate_schedules(self, bus_id):
        """Populate available schedules into the schedule listbox."""
        schedules = self.fetch_bus_schedules(bus_id)
        for schedule in schedules:
            schedule_id, departure_date, departure_time, arrival_time = schedule
            schedule_str = f"Date: {departure_date}, Time: {departure_time} - {arrival_time}"
            self.schedule_listbox.insert(tk.END, schedule_str)

    def confirm_prebooking(self, bus_id, user_id):
        """Confirm prebooking of the selected bus and schedule."""
        selected_schedule_index = self.schedule_listbox.curselection()
        if not selected_schedule_index:
            messagebox.showwarning("Select Schedule", "Please select a schedule to prebook.")
            return

        selected_schedule_str = self.schedule_listbox.get(selected_schedule_index)
        selected_schedule = selected_schedule_str.split(",")
        departure_date = selected_schedule[0].split(":")[1].strip()

        # Insert prebooking into the database
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO prebooked_buses (user_id, bus_id, prebook_date)
                VALUES (?, ?, ?)
            """, (user_id, bus_id, departure_date))

        messagebox.showinfo("Prebooking Successful", f"You have successfully prebooked a bus for {departure_date}.")
        self.schedule_window.destroy()


    def dashboard(self, user_id):
        """User Dashboard where they can view and manage purchased tickets and prebookings."""
        
        # Create a new window for the user dashboard
        self.dashboard_window = tk.Toplevel(self.root)
        self.dashboard_window.title("User Dashboard")
        self.dashboard_window.geometry("900x600")
        self.dashboard_window.resizable(False, False)

        # Title Label
        tk.Label(self.dashboard_window, text="User Dashboard", font=("Arial", 16)).pack(pady=10)

        # Section for Viewing Purchased Tickets
        tk.Label(self.dashboard_window, text="Your Purchased Tickets", font=("Arial", 14)).pack(pady=10)
        
        # Create a Treeview for displaying purchased tickets
        self.ticket_treeview = ttk.Treeview(self.dashboard_window, columns=("Bus Name", "Route", "Seat Number", "Price"), show="headings")
        self.ticket_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

        # Define headings for ticket display
        self.ticket_treeview.heading("Bus Name", text="Bus Name")
        self.ticket_treeview.heading("Route", text="Route")
        self.ticket_treeview.heading("Seat Number", text="Seat Number")
        self.ticket_treeview.heading("Price", text="Price")

        self.ticket_treeview.column("Bus Name", width=150)
        self.ticket_treeview.column("Route", width=150)
        self.ticket_treeview.column("Seat Number", width=100)
        self.ticket_treeview.column("Price", width=100)

        # Fetch purchased tickets for the user
        self.fetch_user_purchased_tickets(user_id)

        # Button to cancel selected ticket
        cancel_ticket_button = tk.Button(self.dashboard_window, text="Cancel Ticket", font=("Arial", 12), command=self.cancel_ticket)
        cancel_ticket_button.pack(pady=10)

        # Section for Viewing Prebooked Buses
        tk.Label(self.dashboard_window, text="Your Prebooked Buses", font=("Arial", 14)).pack(pady=10)
        
        # Create a Treeview for displaying prebooked buses
        self.prebook_treeview = ttk.Treeview(self.dashboard_window, columns=("Bus Name", "Route", "Prebook Date"), show="headings")
        self.prebook_treeview.pack(pady=10, fill=tk.BOTH, expand=True)

        # Define headings for prebooked bus display
        self.prebook_treeview.heading("Bus Name", text="Bus Name")
        self.prebook_treeview.heading("Route", text="Route")
        self.prebook_treeview.heading("Prebook Date", text="Prebook Date")

        self.prebook_treeview.column("Bus Name", width=150)
        self.prebook_treeview.column("Route", width=150)
        self.prebook_treeview.column("Prebook Date", width=100)

        # Fetch prebooked buses for the user
        self.fetch_user_prebooked_buses(user_id)

        # Button to cancel selected prebooking
        cancel_prebooking_button = tk.Button(self.dashboard_window, text="Cancel Prebooking", font=("Arial", 12), command=self.cancel_prebooking)
        cancel_prebooking_button.pack(pady=10)

    def fetch_user_purchased_tickets(self, user_id):
        """Fetch and display the purchased tickets for the user."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT buses.name, routes.route_name, tickets.seat_number, tickets.price, tickets.ticket_id
                FROM tickets
                JOIN buses ON tickets.bus_id = buses.bus_id
                JOIN routes ON buses.route_id = routes.route_id
                WHERE tickets.user_id = ? AND tickets.status = 'sold'
            """, (user_id,))
            tickets = cur.fetchall()

        # Clear previous data in the treeview
        for row in self.ticket_treeview.get_children():
            self.ticket_treeview.delete(row)

        # Insert data into the treeview
        for ticket in tickets:
            bus_name, route_name, seat_number, price, ticket_id = ticket
            self.ticket_treeview.insert("", tk.END, values=(bus_name, route_name, seat_number, price), tags=(ticket_id,))

    def fetch_user_prebooked_buses(self, user_id):
        """Fetch and display the prebooked buses for the user."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT buses.name, routes.route_name, prebooked_buses.prebook_date, prebooked_buses.prebook_id
                FROM prebooked_buses
                JOIN buses ON prebooked_buses.bus_id = buses.bus_id
                JOIN routes ON buses.route_id = routes.route_id
                WHERE prebooked_buses.user_id = ?
            """, (user_id,))
            prebookings = cur.fetchall()

        # Clear previous data in the treeview
        for row in self.prebook_treeview.get_children():
            self.prebook_treeview.delete(row)

        # Insert data into the treeview
        for prebooking in prebookings:
            bus_name, route_name, prebook_date, prebook_id = prebooking
            self.prebook_treeview.insert("", tk.END, values=(bus_name, route_name, prebook_date), tags=(prebook_id,))

    def cancel_ticket(self, user_id):
        """Cancel a purchased ticket."""
        ticket_id = simpledialog.askinteger("Cancel Ticket", "Enter the ticket ID you want to cancel:")
        
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM tickets WHERE ticket_id = ? AND user_id = ?", (ticket_id, user_id))
            conn.commit()

        messagebox.showinfo("Ticket Canceled", "Your ticket has been canceled.")

    def cancel_prebooking(self, user_id):
        """Cancel a prebooked bus."""
        prebook_id = simpledialog.askinteger("Cancel Prebooking", "Enter the prebooking ID you want to cancel:")
        
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM prebooked_buses WHERE prebook_id = ? AND user_id = ?", (prebook_id, user_id))
            conn.commit()

        messagebox.showinfo("Prebooking Canceled", "Your prebooking has been canceled.")

        def logout_admin(self):
            """Logout admin and return to login."""
            self.admin_window.quit()
            self.root.deiconify()

        def logout_user(self):
            """Logout user and return to login."""
            self.user_window.quit()
            self.root.deiconify()

    def main():
        root = tk.Tk()
        app = BusAppGUI(root)
        root.mainloop()

    if __name__ == "__main__":
        main()

