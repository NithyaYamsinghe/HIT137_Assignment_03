# Group Number: Group 56
# STUDENT NAME: Nithya Romeshika Yamasinghe 
# STUDENT NUMBER: S370170
# STUDENT NAME: Ruhani Kakkar 
# STUDENT NUMBER: S371452
# STUDENT NAME: Laba Limbu 
# STUDENT NUMBER: S370270
# STUDENT NAME: Purni Maya Rana 
# STUDENT NUMBER: S371011

import re
import csv
import random
import pymysql
import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageOps
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox, Canvas, filedialog, PhotoImage, Label, Frame, NO, W

# Create a tkinter window instance
window = tk.Tk()

# Set the window title
window.title("STARLIGHT CLOTHING BOUTIQUE")

# Set the window dimensions
window.geometry("1500x800")

# Set the window icon (replace "starlight-logo.ico" with the actual path to your icon file)
window.iconbitmap("starlight-logo.ico")

# Set the default font for the entire app
default_font = ("Helvetica", 12)

# Create style and set the default font for ttk widgets
style = ttk.Style()
style.configure(".", font=default_font)

# Create a style for ttk labels
style.configure("TLabel", font=default_font)

# Create a style for ttk entry widgets
style.configure("TEntry", font=default_font)

# Create a style for ttk combobox
style.configure("TCombobox", font=default_font)

# Create a style for ttk buttons
style = ttk.Style()
style.configure("TButton",
                font=default_font,
                padding=5,
                relief="flat",
                background="#196E78",
                width=15)

# Load an image using PhotoImage
img = PhotoImage(file="window-background.png")

# Create a label to display the background image
label = Label(window, image=img)
label.place(x=0, y=0)

# Create a label at the top of the page with an image
header_label = Label(window, text="STARLIGHT CLOTHING BOUTIQUE", font=("Helvetica", 24), background="#FDEDEC", foreground="#F08080")
header_label.pack(padx=20, pady=20)  # Adjust pady as needed for spacing

# Define a list of placeholders with five empty strings
placeholderArray = ['', '', '', '', '']

# Define a string containing numeric digits
numeric = '1234567890'

# Define a string containing uppercase English alphabet letters
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Initialize a list of tkinter StringVar objects
# This is typically used to create variables that can hold string values in a tkinter application
for i in range(0, 5):
    # Create a StringVar and assign it to the i-th element of the placeholderArray
    placeholderArray[i] = tk.StringVar()

# Define a function to establish a database connection
def connection():
    # Create a connection object with the database server details
    conn = pymysql.connect(
        host='localhost',           # Database server hostname
        user='root',                # Database username
        password='Root@123',        # Database password
        db='starlightstockmanagementdb'  # Database name
    )
    return conn

# Establish a database connection and store it in the 'conn' variable
conn = connection()

# Create a cursor object for executing SQL queries
cursor = conn.cursor()

# Define a function to generate a barcode given an item_id and an optional quiet_zone_size
def generate_barcode(item_id, quiet_zone_size=10):
    
    # Define a function to calculate the checksum for Code128 barcode
    def calculate_checksum(data):
       
        # Filter out non-digit characters from the data
        numeric_data = ''.join(filter(str.isdigit, data))

        # Weights used in Code128 checksum calculation
        weights = [1, 2, 3, 4, 5, 6, 7]
        checksum = 104  # Initial value for Code128 checksum calculation

        # Iterate through the numeric data and calculate the checksum
        for i, digit in enumerate(numeric_data):
            weight = weights[i % len(weights)]
            checksum += int(digit) * weight

        return str(checksum % 103)

    # Calculate the checksum and append it to the item_id
    item_id_with_checksum = item_id + calculate_checksum(item_id)

    # Create a writer and generate the Code128 barcode
    writer = ImageWriter()
    barcode = Code128(item_id_with_checksum, writer=writer)

    # Define the filename for the barcode
    barcode_filename = f"barcodes/{item_id}"

    # Define the full path for the barcode image
    barcode_path = f"{barcode_filename}"

    # Save the barcode image
    barcode.save(barcode_path)

    # Open the barcode image
    img = Image.open(f"{barcode_path}.png")

    # Add a quiet zone around the barcode and save it
    img_with_quiet_zone = ImageOps.expand(img, border=quiet_zone_size, fill='white')
    img_with_quiet_zone.save(f"{barcode_path}.png")

    # Return the path to the generated barcode image
    return barcode_path

# Define a function to display a barcode for a given item_id
def display_barcode(item_id):
    # Generate the path for the barcode image
    barcode_path = generate_barcode(item_id)

    # Load the barcode image as a PhotoImage
    barcode_image = PhotoImage(file=f"{barcode_path}.png")

    # Find and destroy any existing label in the barcode_frame
    existing_label = barcode_frame.grid_slaves(row=0, column=0)
    if existing_label:
        existing_label[0].destroy()

    # Create a new label to display the barcode image
    barcode_label = Label(barcode_frame, image=barcode_image, width=200, height=200)
    barcode_label.photo = barcode_image  # Store a reference to the PhotoImage to prevent it from being garbage collected
    barcode_label.grid(row=0, column=0, padx=10, pady=10)

# The function "generate_barcode(item_id)" is assumed to be defined elsewhere in the code.
# It generates the barcode image for the given item_id and returns the path to the image.

# Define a function to handle the process of displaying a barcode
def show_barcode():
    # Get the values entered by the user from the GUI elements
    item_id = itemIdEntry.get()
    name = nameEntry.get()
    price = priceEntry.get()
    qnt = qntEntry.get()
    category = categoryCombo.get()

    # Check if any of the required fields are empty
    if not item_id or not name or not price or not qnt or not category:
        # Display a warning message if any field is empty
        messagebox.showwarning("Barcode Generation", "Please fill in all fields.")
        return

    # Call the display_barcode function to generate and display the barcode
    display_barcode(item_id)

# Define a function to upload and process an image containing a barcode
def upload_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    
    # Check if a file was selected
    if file_path:
        # Attempt to decode any barcodes found in the selected image
        decoded_objects = decode(Image.open(file_path))

        # Check if any barcodes were successfully decoded
        if decoded_objects:
            # Extract the decoded data (assuming it contains an item ID in the format "123-ABC")
            val = decoded_objects[0].data.decode('utf-8')
            match = re.search(r'\d+-[A-Z]', val)
            item_id = match.group()
            
            # Call a function to update stock quantity based on the decoded item ID
            update_stock_quantity(item_id)
        else:
            # Display a warning if no barcode was found in the selected image
            messagebox.showwarning("Barcode Decoding", "No barcode found in the selected image.")
    else:
        # Display a warning if no image file was selected
        messagebox.showwarning("Barcode Decoding", "Please select an image file.")

# Define a function to update the stock quantity based on the item ID
def update_stock_quantity(item_id):
    try:
        # Ping the database connection to ensure it's active
        cursor.connection.ping()
    
        # Query to fetch the current quantity of the item from the database
        sql_fetch_quantity = f"SELECT `quantity` FROM stocks WHERE `item_id` = '{item_id}'"
        cursor.execute(sql_fetch_quantity)
        current_quantity = cursor.fetchone()

        # Check if a valid current quantity is retrieved and it's greater than 0
        if current_quantity and int(current_quantity[0]) > 0:
            # Convert the current quantity to an integer
            current_quantity_int = int(current_quantity[0])

            # Calculate the new quantity (subtract 1)
            new_quantity = current_quantity_int - 1

            # Update the database with the new quantity
            sql_update_quantity = f"UPDATE stocks SET `quantity` = {new_quantity} WHERE `item_id` = '{item_id}'"
            cursor.execute(sql_update_quantity)
            conn.commit()
            conn.close()

            # Refresh the table (assuming this function exists)
            refreshTable()

            # Show a success message
            messagebox.showinfo("Stock Update", f"Item ID: {item_id} - Stock quantity updated successfully.")
        else:
            # Show a warning if the item is out of stock
            messagebox.showwarning("Stock Update", f"Item ID: {item_id} - Out of stock.")
    except Exception as err:
        # Show a warning if there's an error while updating stock quantity
        messagebox.showwarning("Stock Update", f"Error updating stock quantity: {str(err)}")

# Define a function to open a statistics window
def open_statistics_window():
    # Create a new Toplevel window for statistics
    statistics_window = tk.Toplevel(window)
    statistics_window.title("STOCK STATISTICS")
    statistics_window.geometry("1500x800")  
    statistics_window.iconbitmap("starlight-logo.ico")
    statistics_window.configure(bg="#FFEBEE") 

    # Read data from your source (assuming the `read` function exists)
    data = read()
    
    # Extract quantities and categories from the data
    quantities = [int(item[3]) for item in data]
    categories = [item[4] for item in data]

    # Calculate category-wise quantities
    category_quantity = {}
    for i, cat in enumerate(categories):
        if cat in category_quantity:
            category_quantity[cat] += quantities[i]
        else:
            category_quantity[cat] = quantities[i]

    # Create a pie chart for category-wise quantities
    labels = category_quantity.keys()
    sizes = category_quantity.values()
    fig1, ax1 = plt.subplots(figsize=(6, 6)) 
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal') 

    # Extract item IDs, names, and quantities from the data
    item_ids = [item[0] for item in data]
    item_names = [item[1] for item in data]
    quantities = [int(item[3]) for item in data]

    # Create a bar chart for item-wise quantities
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    x = range(len(item_ids))
    bars = ax2.bar(x, quantities, color='#F08080')

    # Customize x-axis labels
    ax2.set_xticks(x)
    ax2.set_xticklabels(item_names, rotation=45, fontsize=8, ha='right')

    # Customize bar colors
    for bar in bars:
        bar.set_color('#F08080')

    # Create canvas widgets for embedding Matplotlib figures
    canvas1 = Canvas(statistics_window, width=600, height=400, bg="#FFEBEE")
    canvas1.pack(side=tk.LEFT, padx=20, pady=20)
    fig_canvas1 = FigureCanvasTkAgg(fig1, master=canvas1)
    fig_canvas1.draw()
    fig_canvas1.get_tk_widget().pack()

    canvas2 = Canvas(statistics_window, width=600, height=400, bg="#FFEBEE")
    canvas2.pack(side=tk.RIGHT, padx=20, pady=20)
    fig_canvas2 = FigureCanvasTkAgg(fig2, master=canvas2)
    fig_canvas2.draw()
    fig_canvas2.get_tk_widget().pack()

    # Add a label for the chart title
    chart_title_label = tk.Label(statistics_window, text="STOCK STATISTICS", font=("Helvetica", 14), background="#F08080", foreground="#FFEBEE")
    chart_title_label.pack(padx=[10, 10], pady=[10, 10])

# Define a function to check the quantity of items in stock
def check_quantity():
    try:
        # Ping the database connection to ensure it's active
        cursor.connection.ping()

        # SQL query to fetch item information from the 'stocks' table
        sql = "SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks"

        # Execute the SQL query
        cursor.execute(sql)

        # Fetch all results
        results = cursor.fetchall()

        # Commit the changes (if any) to the database
        conn.commit()

        # Close the database connection
        conn.close()

        # Iterate through the fetched results
        for item in results:
            item_id, name, price, quantity, category, date = item

            # Convert the quantity to an integer
            quantity = int(quantity)

            # Check if the quantity is less than 2
            if quantity < 2:
                # Show a warning message for items with low stock
                messagebox.showwarning("Low Stock", f"Item '{name}' (ID: {item_id}) has low stock! Quantity: {quantity}")
    except Exception as err:
        # Show a warning message if there's an error
        messagebox.showwarning("Stock Check Error", f"Error checking stock quantity: {str(err)}")

# Define a function to read data from the 'stocks' table
def read():
    try:
        # Ping the database connection to ensure it's active
        cursor.connection.ping()

        # SQL query to fetch item information from the 'stocks' table, ordered by 'id' in descending order
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks ORDER BY `id` DESC"

        # Execute the SQL query
        cursor.execute(sql)

        # Fetch all results
        results = cursor.fetchall()

        # Commit the changes (if any) to the database
        conn.commit()

        # Close the database connection
        conn.close()

        # Return the fetched results
        return results
    except Exception as err:
        # Show a warning message if there's an error
        messagebox.showwarning("Data Read Error", f"Error reading data from the database: {str(err)}")
        return []  # Return an empty list in case of an error

# Define a function to refresh the table in your GUI
def refreshTable():
    # Clear all existing data from the treeview widget (my_tree)
    for data in my_tree.get_children():
        my_tree.delete(data)

    # Fetch the updated data by calling the 'read' function
    data_array = read()

    # Insert the updated data into the treeview widget (my_tree)
    for array in data_array:
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    # Configure the tag 'orow' to set the background color for alternating rows
    my_tree.tag_configure('orow', background="#EEEEEE")

    # Pack the treeview widget to update its display
    my_tree.pack()

    # Check item quantities after refreshing the table
    check_quantity()

# Define a function to set the value of a tkinter StringVar in placeholderArray
def setph(word, num):
    # Iterate through the placeholderArray
    for ph in range(0, 5):
        # Check if the current index (ph) matches the specified 'num'
        if ph == num:
            # Set the value of the StringVar at the specified index (num) to the given 'word'
            placeholderArray[ph].set(word)

# Define a function to generate a random item ID
def generateRand():
    itemId = ''

    # Generate the first part of the item ID (3 random digits)
    for i in range(0, 3):
        randno = random.randrange(0, len(numeric))
        itemId = itemId + str(numeric[randno])

    # Generate the second part of the item ID (a hyphen and a random uppercase letter)
    randno = random.randrange(0, len(alpha))
    itemId = itemId + '-' + str(alpha[randno])

    # Set the generated item ID in the first placeholder
    setph(itemId, 0)

# Define a function to save a new record in the database
def save():
    # Retrieve and convert data from input fields
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())
    valid = True

    # Check if any of the required fields are empty
    if not(itemId and itemId.strip()) or not(name and name.strip()) or not(price and price.strip()) or not(qnt and qnt.strip()) or not(cat and cat.strip()):
        messagebox.showwarning("", "Please fill up all entries")
        return

    # Check if the item ID length is less than 5 characters
    if len(itemId) < 5:
        messagebox.showwarning("", "Invalid Item Id")
        return

    # Check the format of the item ID
    if(not(itemId[3] == '-')):
        valid = False

    # Check the first three characters of the item ID are numeric
    for i in range(0, 3):
        if(not(itemId[i] in numeric)):
            valid = False
            break

    # Check the fourth character of the item ID is an uppercase letter
    if(not(itemId[4] in alpha)):
        valid = False

    # If the item ID format is not valid, show a warning
    if not(valid):
        messagebox.showwarning("", "Invalid Item Id")
        return
    
    # Check if the price and quantity are valid numeric values
    if not price.isdigit():
        messagebox.showwarning("", "Please enter a valid price")
        return

    if not qnt.isdigit():
        messagebox.showwarning("", "Please enter a valid quantity")
        return

    # Check if the quantity and price are greater than zero
    if int(qnt) <= 0:
        messagebox.showwarning("", "Please enter a valid quantity")
        return

    if int(price) <= 0:
        messagebox.showwarning("", "Please enter a valid price")
        return

    try:
        # Ping the database connection to ensure it's active
        cursor.connection.ping()

        # Check if the item ID is already in the database
        sql = f"SELECT * FROM stocks WHERE `item_id` = '{itemId}'"
        cursor.execute(sql)
        checkItemNo = cursor.fetchall()

        # If the item ID is already used, show a warning
        if len(checkItemNo) > 0:
            messagebox.showwarning("", "Item Id already used")
            return
        else:
            # Insert the new record into the 'stocks' table
            cursor.connection.ping()
            sql = f"INSERT INTO stocks (`item_id`, `name`, `price`, `quantity`, `category`) VALUES ('{itemId}','{name}','{price}','{qnt}','{cat}')"
            cursor.execute(sql)

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

        # Clear the input fields by setting placeholders to empty strings
        for num in range(0, 5):
            setph('', num)

        # Show a success message
        messagebox.showinfo("", "Record saved successfully.")
    except:
        # Show a warning if an error occurs while saving the record
        messagebox.showwarning("", "Error occurred while saving the record")
        return

    # Refresh the table
    refreshTable()

    # Clear any existing barcode displayed on the GUI
    existing_label = barcode_frame.grid_slaves(row=0, column=0)
    if existing_label:
        existing_label[0].destroy()

# Define a function to update an existing record in the database
def update():
    selectedItemId = ''
    try:
        # Get the selected item ID from the treeview
        selectedItem = my_tree.selection()[0]
        selectedItemId = str(my_tree.item(selectedItem)['values'][0])
    except:
        messagebox.showwarning("", "Please select a data row")
    
    # Retrieve and convert data from input fields
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())

    # Check if any of the required fields are empty
    if not(itemId and itemId.strip()) or not(name and name.strip()) or not(price and price.strip()) or not(qnt and qnt.strip()) or not(cat and cat.strip()):
        messagebox.showwarning("", "Please fill up all the fields")
        return

    # Check if the selected item ID matches the new item ID
    if selectedItemId != itemId:
        messagebox.showwarning("", "You can't change the Item Id")
        return

    # Check if the price and quantity are valid numeric values
    if not price.isdigit():
        messagebox.showwarning("", "Please enter a valid price")
        return

    if not qnt.isdigit():
        messagebox.showwarning("", "Please enter a valid quantity")
        return

    # Check if the quantity and price are greater than zero
    if int(qnt) <= 0:
        messagebox.showwarning("", "Please enter a valid quantity")
        return

    if int(price) <= 0:
        messagebox.showwarning("", "Please enter a valid price")
        return

    try:
        # Ping the database connection to ensure it's active
        cursor.connection.ping()

        # Update the record in the 'stocks' table with the new data
        sql = f"UPDATE stocks SET `name` = '{name}', `price` = '{price}', `quantity` = '{qnt}', `category` = '{cat}' WHERE `item_id` = '{itemId}'"
        cursor.execute(sql)

        # Commit the changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

        # Clear the input fields by setting placeholders to empty strings
        for num in range(0, 5):
            setph('', num)

        # Show a success message
        messagebox.showinfo("", "Record updated successfully.")
    except Exception as err:
        # Show a warning if an error occurs while updating the record
        messagebox.showwarning("", "Error occurred: " + str(err))
        return

    # Refresh the table
    refreshTable()

    # Clear any existing barcode displayed on the GUI
    existing_label = barcode_frame.grid_slaves(row=0, column=0)
    if existing_label:
        existing_label[0].destroy()

# Define a function to delete a selected record from the database
def delete():
    try:
        # Check if a row is selected in the treeview
        if my_tree.selection():
            # Ask for confirmation before deleting the selected data
            decision = messagebox.askquestion("", "Do you want to delete the selected data?")
            
            # If the user confirms the deletion, proceed with the deletion
            if decision != 'yes':
                return
            else:
                # Get the selected item ID from the treeview
                selectedItem = my_tree.selection()[0]
                itemId = str(my_tree.item(selectedItem)['values'][0])

                try:
                    # Ping the database connection to ensure it's active
                    cursor.connection.ping()

                    # Delete the record from the 'stocks' table based on the selected item ID
                    sql = f"DELETE FROM stocks WHERE `item_id` = '{itemId}'"
                    cursor.execute(sql)

                    # Commit the changes to the database
                    conn.commit()

                    # Close the database connection
                    conn.close()

                    # Show a success message
                    messagebox.showinfo("", "Record has been successfully deleted")
                except:
                    # Show a message if an error occurs during deletion
                    messagebox.showinfo("", "Sorry, an error occurred")

                # Refresh the table to reflect the updated data
                refreshTable()
    except:
        # Show a warning if no data row is selected
        messagebox.showwarning("", "Please select a data row")

# Define a function to select and populate input fields with data from the selected row in the table
def select():
    try:
        # Get the selected item's data from the treeview
        selectedItem = my_tree.selection()[0]
        itemId = str(my_tree.item(selectedItem)['values'][0])
        name = str(my_tree.item(selectedItem)['values'][1])
        price = str(my_tree.item(selectedItem)['values'][2])
        qnt = str(my_tree.item(selectedItem)['values'][3])
        cat = str(my_tree.item(selectedItem)['values'][4])

        # Set the values in input fields using the setph function
        setph(itemId, 0)
        setph(name, 1)
        setph(price, 2)
        setph(qnt, 3)
        setph(cat, 4)
    except:
        # Show a warning if no data row is selected
        messagebox.showwarning("", "Please select a data row")

# Define a function to search for records in the database based on user input
def find():
    # Retrieve and convert data from input fields
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())

    try:
        # Ping the database connection to ensure it's active
        cursor.connection.ping()

        # Build an SQL query based on the user's input
        if(itemId and itemId.strip()):
            sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `item_id` LIKE '%{itemId}%' "
        elif(name and name.strip()):
            sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `name` LIKE '%{name}%' "
        elif(price and price.strip()):
            sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `price` LIKE '%{price}%' "
        elif(qnt and qnt.strip()):
            sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `quantity` LIKE '%{qnt}%' "
        elif(cat and cat.strip()):
            sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `category` LIKE '%{cat}%' "
        else:
            # Show a warning if none of the entries are filled
            messagebox.showwarning("", "Please fill up one of the entries")
            return

        # Execute the SQL query
        cursor.execute(sql)

        try:
            # Fetch the result of the query
            result = cursor.fetchall()

            # Set the fetched data in input fields using the setph function
            for num in range(0, 5):
                setph(result[0][num], num)

            # Commit any changes to the database
            conn.commit()

            # Close the database connection
            conn.close()
        except:
            # Show a warning if no data is found
            messagebox.showwarning("", "No data found")
    except:
        # Show a warning if an error occurs during the search
        messagebox.showwarning("", "An error occurred during the search")

# Define a function to clear input fields and remove any existing barcode
def clear():
    # Clear input fields by setting placeholders to empty strings
    for num in range(0, 5):
        setph('', num)

    # Clear any existing barcode displayed on the GUI
    existing_label = barcode_frame.grid_slaves(row=0, column=0)
    if existing_label:
        existing_label[0].destroy()

# Define a function to export data to an Excel (CSV) file
def exportExcel():
    try:
        # Ping the database connection to ensure it's active
        cursor.connection.ping()

        # SQL query to fetch data from the 'stocks' table
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks ORDER BY `id` DESC"
        cursor.execute(sql)

        # Fetch the data from the database
        dataraw = cursor.fetchall()

        # Get the current date and time for creating a unique filename
        date = str(datetime.now())
        date = date.replace(' ', '_')
        date = date.replace(':', '-')
        dateFinal = date[0:16]

        # Create or append to a CSV file with a unique filename
        with open("stocks_" + dateFinal + ".csv", 'a', newline='') as f:
            w = csv.writer(f, dialect='excel')
            for record in dataraw:
                w.writerow(record)

        # Close the database connection
        conn.commit()
        conn.close()

        # Show a success message
        messagebox.showinfo("", "Excel file downloaded successfully")
    except:
        # Show a warning if an error occurs during the export
        messagebox.showwarning("", "An error occurred during the export")

# Create a frame within the main window
frame = tk.Frame(window, bg="#F08080", width=500, height=500)
frame.pack(padx=20, pady=20)

# Define button colors
btnColor = "#FFA07A"

# Create a label frame for managing actions (buttons)
manageFrame = tk.LabelFrame(
    frame,
    borderwidth=1,
    bg="#FFEBEE",
    highlightbackground="#EF9A9A",
    highlightthickness=1,
    relief="solid"
)
manageFrame.grid(row=0, column=0, padx=10, pady=20)

# Create buttons with modern styling using grid
saveBtn = ttk.Button(manageFrame, text="SAVE", command=save, style="TButton")
saveBtn.grid(row=0, column=0, padx=5, pady=5)

updateBtn = ttk.Button(manageFrame, text="UPDATE", command=update, style="TButton")
updateBtn.grid(row=0, column=1, padx=5, pady=5)

deleteBtn = ttk.Button(manageFrame, text="DELETE", command=delete, style="TButton")
deleteBtn.grid(row=0, column=2, padx=5, pady=5)

selectBtn = ttk.Button(manageFrame, text="SELECT", command=select, style="TButton")
selectBtn.grid(row=0, column=3, padx=5, pady=5)

findBtn = ttk.Button(manageFrame, text="FIND", command=find, style="TButton")
findBtn.grid(row=0, column=4, padx=5, pady=5)

clearBtn = ttk.Button(manageFrame, text="CLEAR", command=clear, style="TButton")
clearBtn.grid(row=0, column=5, padx=5, pady=5)

exportBtn = ttk.Button(manageFrame, text="EXPORT EXCEL", command=exportExcel, style="TButton")
exportBtn.grid(row=0, column=6, padx=5, pady=5)

ViewStockInfoBtn = ttk.Button(manageFrame, text="VIEW STATISTICS", style="TButton", command=open_statistics_window)
ViewStockInfoBtn.grid(row=0, column=7, padx=5, pady=5)

# Create a label frame for input entries
entriesFrame = tk.LabelFrame(
    frame,
    borderwidth=1,
    bg="#FFEBEE",
    highlightbackground="#EF9A9A",
    highlightthickness=1,
    relief="solid",
    width=300,
    height=300
)
entriesFrame.grid(row=1, column=0, sticky="w", padx=[20, 20], pady=[20, 20], ipadx=6)

# Create a barcode frame within the input entries frame
barcode_frame = Frame(entriesFrame, bg="#FFEBEE")
barcode_frame.grid(row=2, column=3, padx=10, pady=10, columnspan=3, rowspan=7)

# Create labels for input fields
itemIdLabel = ttk.Label(entriesFrame, text="ITEM ID", anchor="e", width=10, background="#FFEBEE")
nameLabel = ttk.Label(entriesFrame, text="NAME", anchor="e", width=10, background="#FFEBEE")
priceLabel = ttk.Label(entriesFrame, text="PRICE", anchor="e", width=10, background="#FFEBEE")
qntLabel = ttk.Label(entriesFrame, text="QUANTITY", anchor="e", width=10, background="#FFEBEE")
categoryLabel = ttk.Label(entriesFrame, text="CATEGORY", anchor="e", width=10, background="#FFEBEE")

# Grid layout for labels
itemIdLabel.grid(row=0, column=0, padx=10, pady=5, sticky="e")
nameLabel.grid(row=1, column=0, padx=10, pady=5, sticky="e")
priceLabel.grid(row=2, column=0, padx=10, pady=5, sticky="e")
qntLabel.grid(row=3, column=0, padx=10, pady=5, sticky="e")
categoryLabel.grid(row=4, column=0, padx=10, pady=5, sticky="e")

categoryArray=['Dresses','Tops','Pants','Shorts', "Work Wear", "Mens"]

# Create entry fields and a combo box for category selection
itemIdEntry = ttk.Entry(entriesFrame, width=50, textvariable=placeholderArray[0], font=("Helvetica", 12))
nameEntry = ttk.Entry(entriesFrame, width=50, textvariable=placeholderArray[1], font=("Helvetica", 12))
priceEntry = ttk.Entry(entriesFrame, width=50, textvariable=placeholderArray[2], font=("Helvetica", 12))
qntEntry = ttk.Entry(entriesFrame, width=50, textvariable=placeholderArray[3], font=("Helvetica", 12))
categoryCombo = ttk.Combobox(entriesFrame, width=47, textvariable=placeholderArray[4], values=categoryArray, font=("Helvetica", 12))

# Grid layout for entry fields and combo box
itemIdEntry.grid(row=0, column=2, padx=5, pady=5)
nameEntry.grid(row=1, column=2, padx=5, pady=5)
priceEntry.grid(row=2, column=2, padx=5, pady=5)
qntEntry.grid(row=3, column=2, padx=5, pady=5)
categoryCombo.grid(row=4, column=2, padx=5, pady=5)

# Create a button to generate a random item ID
generateIdBtn = ttk.Button(entriesFrame, text="GENERATE ID", style="TButton", command=generateRand)
generateIdBtn.grid(row=0, column=3, padx=5, pady=5)

# Create a button to show the barcode image
show_barcode_button = ttk.Button(entriesFrame, text="ADD BARCODE", command=show_barcode, style="TButton")
show_barcode_button.grid(row=0, column=4, padx=5, pady=5)

# Create a button to scan a barcode image
upload_image_button = ttk.Button(entriesFrame, text="SCAN BARCODE", style="TButton", command=upload_image)
upload_image_button.grid(row=0, column=5, padx=5, pady=5)

# Create a frame for displaying the table (Treeview)
table_frame = tk.Frame(frame, bg="#FFEBEE")
table_frame.grid(row=2, column=0, padx=[20, 20], pady=[10, 10], sticky="w", columnspan=2)

# Create a Treeview widget for displaying the table data
my_tree = ttk.Treeview(table_frame, style="mystyle.Treeview")
my_tree['columns'] = ("Item Id", "Name", "Price", "Quantity", "Category", "Date")

# Define columns and their properties
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Item Id", anchor=W, width=70)
my_tree.column("Name", anchor=W, width=220)
my_tree.column("Price", anchor=W, width=125)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Category", anchor=W, width=150)
my_tree.column("Date", anchor=W, width=160)

# Define column headings and styles
style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 12))

my_tree.heading("Item Id", text="ITEM ID", anchor=W)
my_tree.heading("Name", text="NAME", anchor=W)
my_tree.heading("Price", text="PRICE", anchor=W)
my_tree.heading("Quantity", text="QUANTITY", anchor=W)
my_tree.heading("Category", text="CATEGORY", anchor=W)
my_tree.heading("Date", text="ADDED DATE", anchor=W)

# Configure tag for odd rows (alternate row background color)
my_tree.tag_configure('orow', background="#FFA07A")
my_tree.pack()

# Refresh the table data
refreshTable()

# Disable window resizing
window.resizable(False, False)

# Start the main event loop
window.mainloop()
