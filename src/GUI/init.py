import oracledb
from sshtunnel import SSHTunnelForwarder
import ttkbootstrap as ttk
import tkinter as tk
import tkinter.messagebox
import pyodbc
import datetime
import sys
import os.path

# database backend stuff
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from db import DatabaseConnection
from repositories.AddressRepo       import AddressRepository
from repositories.CartItemsRepo     import CartItemsRepository
from repositories.CategoriesRepo    import CategoriesRepository
from repositories.OrderItemsRepo    import OrderItemsRepository
from repositories.OrdersRepo        import OrdersRepository
from repositories.ProductSKUsRepo   import ProductSKUsRepository
from repositories.ProductsRepo      import ProductsRepository
from repositories.UserRepo          import UserRepository

from services.AddressService        import AddressService
from services.AuthService           import AuthService
from services.UserService           import UserService




## Local DB Connection
# def connect_test_db():
#     conn = pyodbc.connect(
#         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;UID=sa;PWD=Test1234;TrustServerCertificate=yes')
#     crsr = conn.cursor()
#     #crsr.close()
#     #conn.close()
#     return crsr, conn

# Production Remote DB Connection
# Oracle DB Connection
'''
DSN = '"{UID}"/cqpncltc@localhost:%d/dbms' % 1521

try:
    with SSHTunnelForwarder(
        ("csdoor.comp.polyu.edu.hk", 22),
        ssh_username="{}",
        ssh_password="{}",
        remote_bind_address=("studora.comp.polyu.edu.hk", 1521),
        local_bind_address=("127.0.0.1", 1521)
    ) as tunnel:
        print("in tunnel")
        dsn = f'"{}"/cqpncltc@localhost:1521/dbms'
        connection = oracledb.connect(dsn)
        cursor = connection.cursor()
        cursor.execute("select * from user")
        cursor.close()
        connection.close()

        print("Connected.")

except Exception as e:
    print(e)
    print("Not connected.")
'''
on_page = ""
uname = ""
def main(root):
    global on_page
    DBConnect = DatabaseConnection()
    DBConnect.connect_to_DB()

    # Object creation
    AddressRepo     = AddressRepository(DBConnect.connection, DBConnect.cursor)
    CartItemsRepo   = CartItemsRepository(DBConnect.connection, DBConnect.cursor)
    CategoriesRepo  = CategoriesRepository(DBConnect.connection, DBConnect.cursor)
    OrderItemsRepo  = OrderItemsRepository(DBConnect.connection, DBConnect.cursor)
    OrdersRepo      = OrdersRepository(DBConnect.connection, DBConnect.cursor)
    ProductSKUsRepo = ProductSKUsRepository(DBConnect.connection, DBConnect.cursor)
    ProductsRepo    = ProductsRepository(DBConnect.connection, DBConnect.cursor)
    UserRepo        = UserRepository(DBConnect.connection, DBConnect.cursor)

    AuthServices        = AuthService(DBConnect.connection, DBConnect.cursor)
    AddressServices     = AddressService(DBConnect.connection, DBConnect.cursor)
    UserServices        = UserService(DBConnect.connection, DBConnect.cursor)

    def on_closing():
        # Exit Database
        DBConnect.force_close_all_connections()
        # Exit GUI
        portal.destroy()
        root.deiconify()
        root.destroy()

    def mainpage(menu_frame):
        global on_page
        if on_page == "mainpage":
            return
        else:
            on_page = "mainpage"
        # left and right frame
        left_frame = tk.Frame(portal, bg="white")
        left_frame.pack(side="left", fill="y", padx=1, pady=0)
        left_frame.config(width=200, height=500)
        left_frame.config(highlightbackground="white", highlightthickness=1)
        left_frame.config(highlightcolor="white")

        # shopping cart label
        shopping_cart_label = ttk.Label(left_frame, text="Shopping Cart")
        shopping_cart_label.pack(padx=90, pady=10)
        sep = ttk.Separator(left_frame, orient="horizontal")
        sep.pack(fill="x", pady=0)

        # shopping cart table
        shopping_cart_table = ttk.Treeview(left_frame)
        shopping_cart_table["columns"] = ("1", "2", "3", "4")
        shopping_cart_table.column("#0", width=0, stretch="no")
        shopping_cart_table.column("1", anchor="w", width=12)
        shopping_cart_table.column("2", anchor="w", width=100)
        shopping_cart_table.column("3", anchor="w", width=12)
        shopping_cart_table.column("4", anchor="w", width=30)

        shopping_cart_table.heading("#0", text="", anchor="w")
        shopping_cart_table.heading("1", text="ID", anchor="w")
        shopping_cart_table.heading("2", text="Name", anchor="w")
        shopping_cart_table.heading("3", text="Qty", anchor="w")
        shopping_cart_table.heading("4", text="Price", anchor="w")

        shopping_cart_table.pack(fill="both", expand=True, padx=0, pady=0)

        # cart options frame
        cart_options_frame = tk.Frame(left_frame, bg="white")
        cart_options_frame.pack(side="bottom", fill="x", padx=0, pady=0)
        cart_options_frame.config(width=200, height=50)

        def remove_selected():
            item = shopping_cart_table.selection()[0]
            total_price.config(text=f"$ {float(total_price['text'][2:]) - float(shopping_cart_table.item(item, 'values')[3])}")
            shopping_cart_table.delete(item)

        # remove button
        remove_button = ttk.Button(cart_options_frame, text="Remove Selected", bootstyle="danger", command=remove_selected)
        remove_button.pack(padx=10, pady=5, anchor="w")

        def empty_cart():
            shopping_cart_table.delete(*shopping_cart_table.get_children())
            total_price.config(text="$ 0.00")
    
        # empty cart button
        empty_cart_button = ttk.Button(cart_options_frame, text="Empty Cart", bootstyle="danger", command=empty_cart)
        empty_cart_button.place(x=262, y=20, anchor="e")

        
        # total price label
        total_price_label = ttk.Label(left_frame, text="Total Price")
        total_price_label.pack(padx=10, pady=3, anchor="e")

        # total price
        total_price = ttk.Label(left_frame, text="$ 0.00", font=("TKDefaultFont", 26))
        total_price.pack(padx=10, pady=3, anchor="e")

        def checkout():
            # get all items in shopping cart into list

            items = get_item()

            print(items)

            # check if cart is empty
            if len(items) == 0:
                tk.messagebox.showerror("Error", "Cart is empty")
                return
            
            # Checkout window
            checkout_window = tk.Toplevel(portal)
            checkout_window.title("Checkout")
            checkout_window.geometry("700x350")

            # Checkout frame
            checkout_frame = tk.Frame(checkout_window, bg="white")
            checkout_frame.pack(side="left", fill="both", padx=1, pady=0)
            checkout_frame.config(highlightbackground="white", highlightthickness=1)
            checkout_frame.config(highlightcolor="white")

            # Checkout label
            checkout_label = ttk.Label(checkout_frame, text="Checkout")
            checkout_label.pack(pady=10, padx=260, anchor="center", fill="x")
            
            sep = ttk.Separator(checkout_frame, orient="horizontal")
            sep.pack(fill="x", pady=0)

            # left right frame
            ileft_frame = tk.Frame(checkout_frame, bg="white")
            ileft_frame.pack(side="left", fill="both", padx=1, pady=0)
            ileft_frame.config(width=200, height=500)
            ileft_frame.config(highlightbackground="white", highlightthickness=1)
            ileft_frame.config(highlightcolor="white")

            # shopping cart label
            shopping_cart_label = ttk.Label(ileft_frame, text="Shopping Cart")
            shopping_cart_label.pack(padx=90, pady=10)
            sep = ttk.Separator(left_frame, orient="horizontal")
            sep.pack(fill="x", pady=0)

            # shopping cart table
            shopping_cart_table = ttk.Treeview(ileft_frame)
            shopping_cart_table["columns"] = ("1", "2", "3", "4")
            shopping_cart_table.column("#0", width=0, stretch="no")
            shopping_cart_table.column("1", anchor="w", width=12)
            shopping_cart_table.column("2", anchor="w", width=100)
            shopping_cart_table.column("3", anchor="w", width=12)
            shopping_cart_table.column("4", anchor="w", width=30)

            shopping_cart_table.heading("#0", text="", anchor="w")
            shopping_cart_table.heading("1", text="ID", anchor="w")
            shopping_cart_table.heading("2", text="Name", anchor="w")
            shopping_cart_table.heading("3", text="Qty", anchor="w")
            shopping_cart_table.heading("4", text="Price", anchor="w")

            shopping_cart_table.pack(fill="both", expand=True, padx=0, pady=0)

            # populate shopping cart table
            for item in items:
                shopping_cart_table.insert("", "end", text="", values=(item[0], item[1], item[2], item[3]))
            
            # check if items are in stock
            for item in items:
                row = ProductSKUsRepo.GetRecord("*", f"WHERE ID = {item[0]}")
            

                # crsr = DBConnect.cursor
                # conn = DBConnect.connection
                # crsr.execute("SELECT * FROM test.dbo.products WHERE id=?", item[0])
                # rows = crsr.fetchall()
                # crsr.close()
                # conn.close()

                if (int(row[0].get("STOCK")) <= 0): # idk it's list 
                    tk.messagebox.showerror("Error", "Not enough stock")
                    checkout_window.destroy()
                    return

            # iright frame
            iright_frame = tk.Frame(checkout_frame, bg="white")
            iright_frame.pack(side="right", fill="both", padx=1, pady=0)
            iright_frame.config(width=200, height=500)
            iright_frame.config(highlightbackground="white", highlightthickness=1)
            iright_frame.config(highlightcolor="white")

            # total price label
            total_price_label = ttk.Label(iright_frame, text="Total Price", width=200)
            total_price_label.pack(padx=10, pady=3, anchor="center")

            # total price
            total_price = ttk.Label(iright_frame, text="$ 0.00", font=("TKDefaultFont", 26))
            total_price.pack(padx=10, pady=3, anchor="center")

            # calculate total price
            for item in items:
                total_price.config(text=f"$ {float(total_price['text'][2:]) + float(item[3])}")

            sep = ttk.Separator(iright_frame, orient="horizontal")
            sep.pack(fill="x", pady=0)

            # payment method label
            payment_method_label = ttk.Label(iright_frame, text="Pay By:")
            payment_method_label.place(x=9, y=90, anchor="w")

            # payment method combobox
            payment_method_combobox = ttk.Combobox(iright_frame, values=["Visa", "MasterCard"], width=7, textvariable="Payment Method")
            payment_method_combobox.place(x=70, y=90, anchor="w")

            # payment method combobox default value
            payment_method_combobox.current(0)

            sep = ttk.Separator(iright_frame, orient="horizontal")
            sep.pack(fill="x", pady=0)

            # payment entry
            payment_entry = ttk.Entry(iright_frame, width=25)
            payment_entry.place(x=165, y=90, anchor="w")

            # ship to label
            ship_to_label = ttk.Label(iright_frame, text="Ship To")
            ship_to_label.place(x=9, y=130, anchor="w")

            # ship to entry
            ship_to_entry = ttk.Entry(iright_frame)
            ship_to_entry.place(x=70, y=130, anchor="w")

            # contact number label
            contact_number_label = ttk.Label(iright_frame, text="Tel.")
            contact_number_label.place(x=9, y=170, anchor="w")

            # contact number entry
            contact_number_entry = ttk.Entry(iright_frame)
            contact_number_entry.place(x=70, y=170, anchor="w")

            # address label
            address_label = ttk.Label(iright_frame, text="Address")
            address_label.place(x=9, y=210, anchor="w")

            # address entry
            address_entry = ttk.Entry(iright_frame, width=35)
            address_entry.place(x=70, y=210, anchor="w")

            sep = ttk.Separator(iright_frame, orient="horizontal")
            sep.place(x=0, y=240, relwidth=1)


            def place_order():
                # check payment validity
                if payment_method_combobox.get() == "Visa":
                    if len(payment_entry.get()) != 16:
                        tk.messagebox.showerror("Error", "Invalid Visa Card Number")
                        return
                elif payment_method_combobox.get() == "MasterCard":
                    if len(payment_entry.get()) != 16:
                        tk.messagebox.showerror("Error", "Invalid MasterCard Number")
                        return
                
                # check all fields are filled
                if ship_to_entry.get() == "" or contact_number_entry.get() == "" or address_entry.get() == "":
                    tk.messagebox.showerror("Error", "Please fill in all fields")
                    return
                
                try:
                    # get user_id from username and store in variable

                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("SELECT * FROM test.dbo.users WHERE username=?", uname)
                    # rows = crsr.fetchall()
                    # crsr.close()
                    # conn.close()

                    user_id = UserRepo.find_by_username(uname)
                    user_id = user_id[0]

                    addressID = AddressRepo.get_by_user_id(user_id)
                    addressID = addressID[0]

                    # commit order meta to database: user_id, total_amount, paid_at, payment_method, payment_no, shipment_data 
                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection

                    # crsr.execute("INSERT INTO test.dbo.orders (user_id, total_amount, paid_at, payment_method, payment_no, shipment_data) VALUES (?, ?, ?, ?, ?, ?)", user_id, total_price['text'][2:], datetime.datetime.now(), payment_method_combobox.get(), payment_entry.get(), address_entry.get())
                    # conn.commit()
                    # crsr.close()
                    # conn.close()
                    record_number = int(OrdersRepo.ReturnNumberOfEntries()) + 1
                    OrdersRepo.AddRecord(record_number, user_id, addressID[0], total_price['text'][2:], "null", datetime.datetime.now(), payment_method_combobox.get(), payment_entry.get(), "Not Shipped yet", address_entry.get(), "null", "null", "N")
                    OrdersRepo.Commit()

                    # get order_id by top 1 and user_id

                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("SELECT TOP 1 * FROM test.dbo.orders WHERE user_id=? ORDER BY id DESC", user_id)
                    # rows = crsr.fetchall()
                    # crsr.close()
                    # conn.close()
                    # order_id = rows[0][0]
                    rows = OrdersRepo.GetRecord("*", f"WHERE USER_ID = {user_id} ORDER BY ID DESC")
                    order_id = rows[0].get("ID")


                    

                    # commit order items to database: order_id, product_id, price, amount
                    for item in items:
                        # crsr = DBConnect.cursor
                        # conn = DBConnect.connection
                        # crsr.execute("INSERT INTO test.dbo.order_items (order_id, product_id, price, amount) VALUES (?, ?, ?, ?)", order_id, item[0], item[3], item[2])
                        # conn.commit()
                        # crsr.close()
                        # conn.close()
                        rows = ProductSKUsRepo.GetRecord("*", f"WHERE PRODUCT_ID = {item[0]}")
                        Product_ID = rows[0].get("PRODUCT_ID")

                        record_number = int(OrderItemsRepo.ReturnNumberOfEntries() + 1)
                        OrderItemsRepo.AddRecord(record_number, order_id, item[0], Product_ID, item[2], item[3])
                        OrdersRepo.Commit()


                    
                    # deduct stock from products table
                    for item in items:
                        # crsr = DBConnect.cursor
                        # conn = DBConnect.connection
                        # crsr.execute("UPDATE test.dbo.products SET stock=stock-? WHERE id=?", item[2], item[0])
                        # conn.commit()
                        # crsr.close()
                        # conn.close()

                        Stock = ProductSKUsRepo.GetRecord("*", f" WHERE ID = {item[0]}")
                        Stock = int(Stock[0].get("STOCK"))
                        Stock = Stock - int(item[2])
                        row = int(item[0])

                        ProductSKUsRepo.UpdateRecord("STOCK", Stock, "ID", row)
                        ProductSKUsRepo.Commit()



                    # empty cart
                    empty_cart()

                    # close checkout window
                    checkout_window.destroy()

                    # show success message
                    tk.messagebox.showinfo("Success", "Order placed successfully")
                except Exception as e:
                    print(e)
                    tk.messagebox.showerror("Error", "Error placing order")
                    return







            # Place Order button
            place_order_button = ttk.Button(iright_frame, text="Place Order", bootstyle="success", command=place_order)
            place_order_button.place(x=400, y=270, anchor="e")

            # populate entries

            # crsr = DBConnect.cursor
            # conn = DBConnect.connection
            # crsr.execute("SELECT * FROM test.dbo.users WHERE username=?", uname)
            # rows = crsr.fetchall()
            # crsr.close()
            # conn.close()


            userData = UserRepo.find_by_username(uname)
            addressData = AddressRepo.get_by_user_id(userData[0])

            ship_to_entry.insert(0, userData[1])
            # contact_number_entry.insert(0, rows[0][6])
            address_entry.insert(0, addressData[0][2].read())

            payment_method_combobox.config(state="readonly")
            ship_to_entry.config(state="readonly")
            # contact_number_entry.config(state="readonly")
            address_entry.config(state="readonly")






   

            


        def get_item():
            items = []
            for child in shopping_cart_table.get_children():
                items.append(shopping_cart_table.item(child, "values"))
            return items


        # checkout button
        checkout_button = ttk.Button(left_frame, text="Checkout", bootstyle="success", command=lambda: checkout())
        checkout_button.pack(padx=10, pady=5, anchor="e")

        sep1 = ttk.Separator(left_frame, orient="horizontal")
        sep1.pack(fill="x", pady=0)


        right_frame = tk.Frame(portal, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        right_frame.config(width=600, height=500)
        right_frame.config(highlightbackground="white", highlightthickness=1)
        right_frame.config(highlightcolor="white")

        # product label
        product_label = ttk.Label(right_frame, text="Products")
        product_label.pack(padx=10, pady=10)
        sep = ttk.Separator(right_frame, orient="horizontal")
        sep.pack(fill="x", pady=0)

        # search bar
        search_bar = ttk.Entry(right_frame, width=30)

        # sort by label
        sort_by_label = ttk.Label(right_frame, text="")
        sort_by_label.pack(padx=10, pady=10)

        sort_by_menu = ttk.Combobox(right_frame, values=["Price", "Name", "Product ID"], width=15, textvariable="Sort By")
        sort_by_menu.place(x=170, y=60, anchor="e")
        search_bar.place(x=185, y=60, anchor="w")

        def sort_by():
            sort_option = sort_by_menu.get()
            if sort_option == "Price":
                product_table.delete(*product_table.get_children())
                rows = ProductsRepo.GetRecord("*", "ORDER BY PRICE")
                
                for row in rows:
                    product_table.insert("", "end", text="", values=(row.get("ID"), row.get("CATEGORY_ID"), row.get("PRICE"), row.get("TITLE"), row.get("DESCRIPTION")))
            


            elif sort_option == "Name":
                product_table.delete(*product_table.get_children())
                rows = ProductsRepo.GetRecord("*", "ORDER BY TITLE")
                for row in rows:
                    product_table.insert("", "end", text="", values=(row.get("ID"), row.get("CATEGORY_ID"), row.get("PRICE"), row.get("TITLE"), row.get("DESCRIPTION")))


            elif sort_option == "Product ID":
                product_table.delete(*product_table.get_children())
                rows = ProductsRepo.GetRecord("*", "ORDER BY ID")
                for row in rows:
                    product_table.insert("", "end", text="", values=(row.get("ID"), row.get("CATEGORY_ID"), row.get("PRICE"), row.get("TITLE"), row.get("DESCRIPTION")))


        sort_by_menu.bind("<<ComboboxSelected>>", lambda event: sort_by())

        def search():
            # crsr = DBConnect.cursor
            # conn = DBConnect.connection
            # crsr.execute("SELECT * FROM test.dbo.products WHERE title LIKE ?", f"%{search_bar.get()}%")
            # results = []
            # rows = crsr.fetchall()

            rows = ProductsRepo.GetRecord("*", f"WHERE TITLE LIKE {search_bar.get()}")

            # for row in rows:
            #     result = {}
            #     for i, column in enumerate(crsr.description):
            #         result[column[0]] = row[i]
            #     results.append(result)
            # crsr.close()
            # conn.close()

            # clear table
            product_table.delete(*product_table.get_children())
            
            # insert data into table
            for row in rows:
                product_table.insert("", "end", text="", values=(row.get("ID"), row.get("CATEGORY_ID"), row.get("PRICE"), row.get("TITLE"), row.get("DESCRIPTION")))

        
        search_button = ttk.Button(right_frame, text="Search", bootstyle="secondary", command=search)
        search_button.place(x=475, y=60, anchor="w")
        search_bar.insert(0, "")
        sort_by_menu.current(0)


        sep1 = ttk.Separator(right_frame, orient="vertical")
        sep1.pack(side="right", fill="y", pady=0)

        # product table
        product_table = ttk.Treeview(right_frame)
        product_table["columns"] = ("1", "2", "3", "4", "5")
        product_table.column("#0", width=0, stretch="no")
        product_table.column("1", anchor="w", width=12)
        product_table.column("2", anchor="w", width=12)
        product_table.column("3", anchor="w", width=30)
        product_table.column("4", anchor="w", width=100)
        product_table.column("5", anchor="w", width=400)

        product_table.heading("#0", text="", anchor="w")
        product_table.heading("1", text="ID", anchor="w")
        product_table.heading("2", text="CatID", anchor="w")
        product_table.heading("3", text="Price", anchor="w")
        product_table.heading("4", text="Name", anchor="w")
        product_table.heading("5", text="Description", anchor="w")

        product_table.pack(fill="both", expand=True, padx=0, pady=0)

        # product information panel
        product_info_panel = tk.Frame(right_frame, bg="white")
        product_info_panel.pack(side="bottom", fill="x", padx=0, pady=0)
        product_info_panel.config(width=600, height=150)
        product_info_panel.config(highlightbackground="white", highlightthickness=1)
        product_info_panel.config(highlightcolor="white")

        # Name of product
        product_name = ttk.Label(product_info_panel, text="Name of Product", font=("TKDefaultFont", 16))
        product_name.place(x=100, y=24, anchor="w")

        # Price of product
        product_price = ttk.Label(product_info_panel, text="Unit Price")
        product_price.place(x=100, y=46, anchor="w")

        # product description
        product_description = ttk.Label(product_info_panel, text="Description", wraplength=500)
        def add_to_cart():
            item = product_table.selection()[0]

            # check if item is already in cart
            # if so, increase quantity and calculate price
            for child in shopping_cart_table.get_children():
                if shopping_cart_table.item(child, "values")[0] == product_table.item(item, "values")[0]:
                    quantity = int(shopping_cart_table.item(child, "values")[2]) + 1
                    price = float(product_table.item(item, "values")[2]) * quantity
                    shopping_cart_table.item(child, text="", values=(product_table.item(item, "values")[0], product_table.item(item, "values")[3], quantity, price))
                    total_price.config(text=f"$ {float(total_price['text'][2:]) + float(product_table.item(item, 'values')[2])}")
                    return
            else:
                shopping_cart_table.insert("", "end", text="", values=(product_table.item(item, "values")[0], product_table.item(item, "values")[3], 1, product_table.item(item, "values")[2]))
                total_price.config(text=f"$ {float(total_price['text'][2:]) + float(product_table.item(item, 'values')[2])}")

        # add to cart button
        add_to_cart_button = ttk.Button(product_info_panel, text="Add to Cart", bootstyle="warning", command=add_to_cart)
        add_to_cart_button.place(x=100, y=130, anchor="e")

        rows = ProductsRepo.GetRecord("*", "")

        results = []
        # for row in rows:
        #     result = {}
        #     # for i, column in enumerate(crsr.description):
        #     #     result[column[0]] = row[i]
        #     results.append(result)

        # insert data into table
        for row in rows:
            product_table.insert("", "end", text="", values=(row.get("ID"), row.get("CATEGORY_ID"), row.get("PRICE"), row.get("TITLE"), row.get("DESCRIPTION")))

        # update product information panel when clicked
        def update_product_info(event):
            item = product_table.selection()[0]
            product_name.config(text=product_table.item(item, "values")[3])
            product_price.config(text=f"$ {product_table.item(item, 'values')[2]}")
            product_description.config(text=product_table.item(item, 'values')[4])
        
        product_table.bind("<ButtonRelease-1>", update_product_info)

       # check if clicked on menu_frame
        def check_click(event):
            # check if event.widget has "!frame2" in it
            if "!frame2" in str(event.widget):
                # check if cart is empty
                    if len(shopping_cart_table.get_children()) != 0:
                    # check if user wants to leave
                        if tk.messagebox.askokcancel("Warning", "You had items in your cart. But it's okay, we've emptied it for you."):
                            empty_cart()
                        
            return

        portal.bind("<ButtonRelease-1>", check_click)

    def inventory(menu_frame):
        global on_page
        if on_page == "inventory":
            return
        else:
            on_page = "inventory"


        def open_inventory_window():
            # Create a new window for the inventory
            inventory_window = tk.Toplevel(portal)
            inventory_window.title("Inventory")
            inventory_window.geometry("900x600")

            # Inventory frame
            inventory_frame = tk.Frame(inventory_window, bg="white")
            inventory_frame.pack(side="left", fill="both", padx=1, pady=0)
            inventory_frame.config(highlightbackground="white", highlightthickness=1)
            inventory_frame.config(highlightcolor="white")

            # Shopping cart label
            inventory_label = ttk.Label(inventory_frame, text="Current Inventory")
            inventory_label.pack(pady=10, anchor="center", fill="x")

            sep = ttk.Separator(inventory_frame, orient="horizontal")
            sep.pack(fill="x", pady=0)

            # Inventory table
            inventory_table = ttk.Treeview(inventory_frame)
            inventory_table["columns"] = ("1", "2", "3", "4", "5", "6")
            inventory_table.column("#0", width=0, stretch="no")
            inventory_table.column("1", anchor="w", width=4)
            inventory_table.column("2", anchor="w", width=4)
            inventory_table.column("3", anchor="w", width=10)
            inventory_table.column("4", anchor="w", width=12)
            inventory_table.column("5", anchor="w", width=100)
            inventory_table.column("6", anchor="w", width=400)

            inventory_table.heading("#0", text="", anchor="w")
            inventory_table.heading("1", text="ID", anchor="w")
            inventory_table.heading("2", text="CatID", anchor="w")
            inventory_table.heading("3", text="Price", anchor="w")
            inventory_table.heading("4", text="Stock", anchor="w")
            inventory_table.heading("5", text="Name", anchor="w")
            inventory_table.heading("6", text="Description", anchor="w")

            inventory_table.pack(fill="both", expand=True, padx=0, pady=0)

            # Product information panel
            product_info_panel = tk.Frame(inventory_frame, bg="white")
            product_info_panel.pack(side="bottom", fill="x", padx=0, pady=0)
            product_info_panel.config(width=900, height=150)
            product_info_panel.config(highlightbackground="white", highlightthickness=1)
            product_info_panel.config(highlightcolor="white")

            # Name of product
            product_name_entry = ttk.Entry(product_info_panel, font=("TKDefaultFont", 16))
            product_name_entry.place(x=110, y=24, anchor="w")
            product_name_label = ttk.Label(product_info_panel, text="Name")
            product_name_label.place(x=105, y=24, anchor="e")

            # Price of product
            product_price_entry = ttk.Entry(product_info_panel)
            product_price_entry.place(x=110, y=59, anchor="w")
            product_price_label = ttk.Label(product_info_panel, text="Price")
            product_price_label.place(x=105, y=59, anchor="e")

            # Product description
            product_description_entry = ttk.Entry(product_info_panel, width=60)
            product_description_entry.place(x=110, y=93, anchor="w")
            product_description_label = ttk.Label(product_info_panel, text="Description")
            product_description_label.place(x=100, y=93, anchor="e")

            # Separator
            sep2 = ttk.Separator(product_info_panel, orient="horizontal")
            sep2.place(x=0, y=110, relwidth=1)

            # Stock label
            stock_label = ttk.Label(product_info_panel, text="Stock")
            stock_label.place(x=100, y=130, anchor="e")

            # Stock entry spinbox
            stock_spinbox = tk.Spinbox(product_info_panel, from_=0, to=100000, width=10)
            stock_spinbox.place(x=110, y=130, anchor="w")

            def update_product():
                # update product information
                item = inventory_table.selection()[0]
                try:
                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("UPDATE test.dbo.products SET title=?, lowest_price=?, description=?, stock=? WHERE id=?", product_name_entry.get(), product_price_entry.get(), product_description_entry.get(), stock_spinbox.get(), inventory_table.item(item, "values")[0])
                    # conn.commit()
                    # crsr.close()
                    # conn.close()

                    ProductsRepo.UpdateRecord("TITLE", product_name_entry.get(), "ID", inventory_table.item(item, "values")[0])
                    ProductsRepo.UpdateRecord("PRICE", product_price_entry.get(), "ID", inventory_table.item(item, "values")[0])
                    ProductsRepo.UpdateRecord("DESCRIPTION", product_description_entry.get(), "ID", inventory_table.item(item, "values")[0])
                    ProductSKUsRepo.UpdateRecord("STOCK", stock_spinbox.get(), "PRODUCT_ID", inventory_table.item(item, "values")[0])
                    ProductsRepo.Commit()

                except:
                    print("Error updating product")
                empty_fields()
                populate_inventory_table()
        
            # Update Details button
            update_details_button = ttk.Button(product_info_panel, text="Update Details", bootstyle="warning", command=update_product)
            update_details_button.place(x=890, y=130, anchor="e")

            def delete_product():
                # delete product from database
                item = inventory_table.selection()[0]
                try:
                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("DELETE FROM test.dbo.products WHERE id=?", inventory_table.item(item, "values")[0])
                    # conn.commit()
                    # crsr.close()
                    # conn.close()

                    ProductsRepo.DeleteRecord("ID", inventory_table.item(item, "values")[0])
                    ProductSKUsRepo.DeleteRecord("PRODUCT_ID", inventory_table.item(item, "values")[0])

                    ProductsRepo.Commit()
                    ProductSKUsRepo.Commit()

                except:
                    print("Error deleting product")
                
                empty_fields()
                populate_inventory_table()

            # Delete Product button
            delete_product_button = ttk.Button(product_info_panel, text="Delete Product", bootstyle="danger", command=delete_product)
            delete_product_button.place(x=770, y=130, anchor="e")

            def add_product():
                # add product to database
                try:
                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("INSERT INTO test.dbo.products (title, lowest_price, description, stock, category_id) VALUES (?, ?, ?, ?, ?)", product_name_entry.get(), product_price_entry.get(), product_description_entry.get(), stock_spinbox.get(), "1")
                    # conn.commit()
                    # crsr.close()
                    # conn.close()

                    ProductsEntriesNumber = ProductsRepo.ReturnNumberOfEntries() + 1
                    ProductSKUsEntriesNumber = ProductSKUsRepo.ReturnNumberOfEntries() + 1
                    ProductsRepo.AddRecord(ProductsEntriesNumber, 0, product_name_entry.get(), product_description_entry.get(), "null", product_price_entry.get())
                    
                    ProductsEntriesNumber = ProductsRepo.ReturnNumberOfEntries()
                    ProductSKUsRepo.AddRecord(ProductSKUsEntriesNumber, ProductsEntriesNumber, product_name_entry.get(), product_description_entry.get(), product_price_entry.get(), stock_spinbox.get())
                    ProductsRepo.Commit()
                    ProductSKUsRepo.Commit()


                except Exception as e:
                    print(e)
                empty_fields()
                populate_inventory_table()

            # Add Product button
            add_product_button = ttk.Button(product_info_panel, text="Add Product", bootstyle="success", command=add_product)
            add_product_button.place(x=648, y=130, anchor="e")

            def empty_fields():
                product_name_entry.delete(0, "end")
                product_price_entry.delete(0, "end")
                product_description_entry.delete(0, "end")
                stock_spinbox.delete(0, "end")

            # Empty Fields button
            empty_fields_button = ttk.Button(product_info_panel, text="Empty Fields", bootstyle="primary", command=empty_fields)
            empty_fields_button.place(x=540, y=130, anchor="e")

            def populate_inventory_table():
                
                inventory_table.delete(*inventory_table.get_children())
                # crsr = DBConnect.cursor
                # conn = DBConnect.connection
                # crsr.execute("SELECT * FROM test.dbo.products")
                # results = []
                # rows = crsr.fetchall()
                # for row in rows:
                #     result = {}
                #     for i, column in enumerate(crsr.description):
                #         result[column[0]] = row[i]
                #     results.append(result)
                # crsr.close()
                # conn.close()

                rows = ProductSKUsRepo.GetRecord("*", "")



                # Insert data into table
                for row in rows:
                    inventory_table.insert("", "end", text="", values=(row[0], row[1], row[5], row[6], row[2], row[3]))

            populate_inventory_table()

            # Update product information panel when clicked
            def update_product_info(event):
                item = inventory_table.selection()[0]
                product_name_entry.delete(0, "end")
                product_name_entry.insert(0, inventory_table.item(item, "values")[4])
                product_price_entry.delete(0, "end")
                product_price_entry.insert(0, inventory_table.item(item, "values")[2])
                product_description_entry.delete(0, "end")
                product_description_entry.insert(0, inventory_table.item(item, 'values')[5])
                stock_spinbox.delete(0, "end")
                stock_spinbox.insert(0, inventory_table.item(item, "values")[3])
        

            inventory_table.bind("<ButtonRelease-1>", update_product_info)
            inventory_window.mainloop()
            inventory_window.destroy()
        
        open_inventory_window()

    def myac(menu_frame):
        global on_page, uname
        if on_page == "myac":
            return
        else:
            on_page = "myac"

        def open_myac_window():
            # Create a new window for the inventory
            myac_window = tk.Toplevel(portal)
            myac_window.title("My Account")
            myac_window.geometry("600x280")

            # My Account frame
            myac_frame = tk.Frame(myac_window, bg="white")
            myac_frame.pack(side="left", fill="both", padx=1, pady=0)
            myac_frame.config(highlightbackground="white", highlightthickness=1)
            myac_frame.config(highlightcolor="white")

            # My Account label
            myac_label = ttk.Label(myac_frame, text="My A/C")
            myac_label.pack(pady=10, padx=270, anchor="center", fill="x")

            sep = ttk.Separator(myac_frame, orient="horizontal")
            sep.pack(fill="x", pady=0)

            # Account Details frame
            account_details_frame = tk.Frame(myac_frame, bg="white")
            account_details_frame.pack(side="top", fill="x", padx=0, pady=0)
            account_details_frame.config(width=600, height=600)
            account_details_frame.config(highlightbackground="white", highlightthickness=1)
            account_details_frame.config(highlightcolor="white")

            # username display
            username_label = ttk.Label(account_details_frame, text="Username")
            username_label.place(x=100, y=24, anchor="e")

            username_entry = ttk.Entry(account_details_frame)
            username_entry.place(x=110, y=24, anchor="w")
            username_entry.insert(0, "")

            # password display
            password_label = ttk.Label(account_details_frame, text="Password")
            password_label.place(x=100, y=59, anchor="e")

            password_entry = ttk.Entry(account_details_frame)
            password_entry.place(x=110, y=59, anchor="w")

            # password confirmation display
            password_confirm_label = ttk.Label(account_details_frame, text="Retype")
            password_confirm_label.place(x=100, y=93, anchor="e")

            password_confirm_entry = ttk.Entry(account_details_frame, show="*")
            password_confirm_entry.place(x=110, y=93, anchor="w")

            # Separator
            sep2 = ttk.Separator(account_details_frame, orient="horizontal")
            sep2.place(x=0, y=110, relwidth=1)

            # Contact Details label
            contact_details_label = ttk.Label(account_details_frame, text="Contact Details")
            contact_details_label.place(x=100, y=130, anchor="e")
            
  
            # Contact Name Entry
            contact_name_entry = ttk.Entry(account_details_frame)
            contact_name_entry.place(x=110, y=130, anchor="w")

            # Contact Number Label
            contact_number_label = ttk.Label(account_details_frame, text="Tel.")
            contact_number_label.place(x=277, y=130, anchor="w")

            # Contact Number Entry
            contact_number_entry = ttk.Entry(account_details_frame)
            contact_number_entry.place(x=310, y=130, anchor="w")

            # Address Label
            address_label = ttk.Label(account_details_frame, text="Address")
            address_label.place(x=100, y=160, anchor="e")

            # Address Entry
            address_entry = ttk.Entry(account_details_frame, width=42)
            address_entry.place(x=110, y=165, anchor="w")

            # Separator
            sep3 = ttk.Separator(account_details_frame, orient="horizontal")
            sep3.place(x=0, y=190, relwidth=1)

            def update_details():
                if password_entry.get() != password_confirm_entry.get():
                    if password_entry.get() == "":
                        tk.messagebox.showerror("Error", "Password cannot be empty")
                        return
                    tk.messagebox.showerror("Error", "Passwords do not match")
                    return
                else:
                    try:
                        # crsr = DBConnect.cursor
                        # conn = DBConnect.connection
                        # crsr.execute("UPDATE test.dbo.users SET username=?, password=?, contact_name=?, contact_number=?, details=? WHERE username=?", username_entry.get(), password_entry.get(), contact_name_entry.get(), contact_number_entry.get(), address_entry.get(), uname)
                        # conn.commit()
                        # crsr.close()
                        # conn.close()
                        UserID = UserRepo.find_by_username(username_entry.get())
                        UserRepo.update(UserID[0], username_entry.get(), "null", password_entry.get(), UserID[4])


                        tk.messagebox.showinfo("Success", "Details updated")
                        populate_account_details()
                    except Exception as e:
                        print(e)
            # Update Details button
            update_details_button = ttk.Button(account_details_frame, text="Update Details", bootstyle="warning", command=update_details)
            update_details_button.place(x=5, y=210, anchor="w")


            # populate account details
            def populate_account_details():
                # crsr = DBConnect.cursor
                # conn = DBConnect.connection
                # crsr.execute("SELECT * FROM test.dbo.users WHERE username=?", uname)
                # rows = crsr.fetchall()
                # crsr.close()
                # conn.close()

                rows = UserRepo.find_by_username(uname)


                # Insert data into table
                for row in rows:
                    print(row)
                    username_entry.insert(0, row[1])                    
                    contact_name_entry.insert(0, row[5])
                    contact_number_entry.insert(0, row[6])
                    address_entry.insert(0, row[7])



            populate_account_details()

        open_myac_window()


    def admin_user(menu_frame):
        global on_page
        if on_page == "admin_user":
            return
        else:
            on_page = "admin_user"

        def open_admin_user_window():
          # Create a new window for the inventory
            admin_user_window= tk.Toplevel(portal)
            admin_user_window.title("Inventory")
            admin_user_window.geometry("900x600")

            # Inventory frame
            admin_user_frame = tk.Frame(admin_user_window, bg="white")
            admin_user_frame.pack(side="left", fill="both", padx=1, pady=0)
            admin_user_frame.config(highlightbackground="white", highlightthickness=1)
            admin_user_frame.config(highlightcolor="white")

            # Shopping cart label
            admin_user_label = ttk.Label(admin_user_frame, text="Registered Users")
            admin_user_label.pack(pady=10, anchor="center", fill="x")

            sep = ttk.Separator(admin_user_frame, orient="horizontal")
            sep.pack(fill="x", pady=0) 

            # User table
            user_table = ttk.Treeview(admin_user_frame)
            user_table["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
            user_table.column("#0", width=0, stretch="no")
            user_table.column("1", anchor="w", width=6)
            user_table.column("2", anchor="w", width=150)
            user_table.column("3", anchor="w", width=20)
            user_table.column("4", anchor="w", width=100)
            user_table.column("5", anchor="w", width=40)
            user_table.column("6", anchor="w", width=150)
            user_table.column("7", anchor="w", width=100)
            user_table.column("8", anchor="w", width=400)


            user_table.heading("#0", text="", anchor="w")
            user_table.heading("1", text="ID", anchor="w")
            user_table.heading("2", text="Username", anchor="w")
            user_table.heading("3", text="Avatar URL", anchor="w")
            user_table.heading("4", text="Password", anchor="w")
            user_table.heading("5", text="Is Admin", anchor="w")
            user_table.heading("6", text="Contact Name", anchor="w")
            user_table.heading("7", text="Contact Number", anchor="w")
            user_table.heading("8", text="Address", anchor="w")

            user_table.pack(fill="both", expand=True, padx=0, pady=0)

            # populate user table
            def populate_user_table():
                user_table.delete(*user_table.get_children())
                # crsr = DBConnect.cursor
                # conn = DBConnect.connection
                # crsr.execute("SELECT * FROM test.dbo.users")
                # rows = crsr.fetchall()
                # crsr.close()
                # conn.close()

                DBConnect.cursor.execute("SELECT * FROM User")
                rows = DBConnect.cursor.fetchall()

                DBConnect.cursor.execute("SELECT * FROM Address")
                AddressData = DBConnect.cursor.fetchall()

                # Insert data into table
                for row in rows:
                    user_table.insert("", "end", text="", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                
            populate_user_table()

            # Action frame
            action_frame = tk.Frame(admin_user_frame, bg="white")
            action_frame.pack(side="bottom", fill="x", padx=0, pady=0)
            action_frame.config(width=900, height=50)
            action_frame.config(highlightbackground="white", highlightthickness=1)
            action_frame.config(highlightcolor="white")

            # delete user
            def delete_user():
                item = user_table.selection()[0]
                try:
                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("DELETE FROM test.dbo.users WHERE id=?", user_table.item(item, "values")[0])
                    # conn.commit()
                    # crsr.close()
                    # conn.close()

                    UserRepo.delete(user_table.item(item, "values")[0])


                except:
                    print("Error deleting user")
                populate_user_table()
            
            # Delete User button
            delete_user_button = ttk.Button(action_frame, text="Delete User", bootstyle="danger", command=delete_user)
            delete_user_button.place(x=5, y=25, anchor="w")

            def edit_user():

                item = user_table.selection()[0]
                luname = user_table.item(item, "values")[1]

                # edit user window
                edit_user_window = tk.Toplevel(admin_user_window)
                edit_user_window.title("Edit User")
                edit_user_window.geometry("600x280")

                # Edit User frame
                edit_user_frame = tk.Frame(edit_user_window, bg="white")
                edit_user_frame.pack(side="left", fill="both", padx=1, pady=0)
                edit_user_frame.config(highlightbackground="white", highlightthickness=1)
                edit_user_frame.config(highlightcolor="white")

                # Edit User label
                edit_user_label = ttk.Label(edit_user_frame, text="Edit User")
                edit_user_label.pack(pady=10, padx=270, anchor="center", fill="x")

                sep = ttk.Separator(edit_user_frame, orient="horizontal")
                sep.pack(fill="x", pady=0)

                # Account Details frame
                account_details_frame = tk.Frame(edit_user_frame, bg="white")
                account_details_frame.pack(side="top", fill="x", padx=0, pady=0)
                account_details_frame.config(width=600, height=600)
                account_details_frame.config(highlightbackground="white", highlightthickness=1)
                account_details_frame.config(highlightcolor="white")

                # username display
                username_label = ttk.Label(account_details_frame, text="Username")
                username_label.place(x=100, y=24, anchor="e")

                username_entry = ttk.Entry(account_details_frame)
                username_entry.place(x=110, y=24, anchor="w")
                username_entry.insert(0, "")

                # password display
                password_label = ttk.Label(account_details_frame, text="Password")
                password_label.place(x=100, y=59, anchor="e")

                password_entry = ttk.Entry(account_details_frame)
                password_entry.place(x=110, y=59, anchor="w")

                # password confirmation display
                password_confirm_label = ttk.Label(account_details_frame, text="Retype")
                password_confirm_label.place(x=100, y=93, anchor="e")

                password_confirm_entry = ttk.Entry(account_details_frame, show="*")
                password_confirm_entry.place(x=110, y=93, anchor="w")

                # Separator
                sep2 = ttk.Separator(account_details_frame, orient="horizontal")
                sep2.place(x=0, y=110, relwidth=1)

                # Contact Details label
                contact_details_label = ttk.Label(account_details_frame, text="Contact Details")
                contact_details_label.place(x=100, y=130, anchor="e")

                # Contact Name Entry
                contact_name_entry = ttk.Entry(account_details_frame)
                contact_name_entry.place(x=110, y=130, anchor="w")

                # Contact Number Label
                contact_number_label = ttk.Label(account_details_frame, text="Tel.")
                contact_number_label.place(x=277, y=130, anchor="w")

                # Contact Number Entry
                contact_number_entry = ttk.Entry(account_details_frame)
                contact_number_entry.place(x=310, y=130, anchor="w")

                # Address Label
                address_label = ttk.Label(account_details_frame, text="Address")
                address_label.place(x=100, y=160, anchor="e")

                # Address Entry
                address_entry = ttk.Entry(account_details_frame, width=42)
                address_entry.place(x=110, y=165, anchor="w")

                # Separator
                sep3 = ttk.Separator(account_details_frame, orient="horizontal")
                sep3.place(x=0, y=190, relwidth=1)

                def update_details():
                    if password_entry.get() != password_confirm_entry.get():
                        if password_entry.get() == "":
                            tk.messagebox.showerror("Error", "Password cannot be empty")
                            return
                        tk.messagebox.showerror("Error", "Passwords do not match")
                        return
                    else:
                        try:
                            # crsr = DBConnect.cursor
                            # conn = DBConnect.connection
                            # crsr.execute("UPDATE test.dbo.users SET username=?, password=?, contact_name=?, contact_number=?, details=? WHERE username=?", username_entry.get(), password_entry.get(), contact_name_entry.get(), contact_number_entry.get(), address_entry.get(), uname)
                            # conn.commit()
                            # crsr.close()
                            # conn.close()
                            UserID = UserRepo.find_by_username(username_entry.get())
                            UserRepo.update(UserID[0], username_entry.get(), "null", password_entry.get(), UserID[4])

                            tk.messagebox.showinfo("Success", "Details updated")
                            edit_user_window.destroy()
                        except Exception as e:
                            print(e)
                            edit_user_window.destroy()
                
                # Update Details button
                update_details_button = ttk.Button(account_details_frame, text="Update Details", bootstyle="warning", command=update_details)
                update_details_button.place(x=5, y=210, anchor="w")
                
                # populate account details
                def populate_account_details():
                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("SELECT * FROM test.dbo.users WHERE username=?", luname)
                    # rows = crsr.fetchall()
                    # crsr.close()
                    # conn.close()

                    rows = UserRepo.find_by_username(luname)

                    # Insert data into table
                    for row in rows:
                        print(row)
                        username_entry.insert(0, row[1])                    
                        contact_name_entry.insert(0, row[5])
                        contact_number_entry.insert(0, row[6])
                        address_entry.insert(0, row[7])

                populate_account_details()
                


            # Edit User button
            edit_user_button = ttk.Button(action_frame, text="Edit User", bootstyle="warning", command=lambda: edit_user())
            edit_user_button.place(x=110, y=25, anchor="w")

            def make_user_admin():
                item = user_table.selection()[0]
                try:
                    # crsr = DBConnect.cursor
                    # conn = DBConnect.connection
                    # crsr.execute("UPDATE test.dbo.users SET is_admin=? WHERE id=?", "1", user_table.item(item, "values")[0])
                    # conn.commit()
                    # crsr.close()
                    # conn.close()
                    UserID = UserRepo.find_by_username(username_entry.get())
                    UserRepo.update(UserID[0], UserID[1], UserID[2], UserID[3], user_table.item(item, "values")[0])
                except:
                    print("Error making user admin")
                populate_user_table()

            # Make User Admin button
            make_user_admin_button = ttk.Button(action_frame, text="Make User Admin", bootstyle="success", command=make_user_admin)
            make_user_admin_button.place(x=198, y=25, anchor="w")

        open_admin_user_window()
        
    def reporting(menu_frame):

        # Create a new window for reporting
        reporting_window = tk.Toplevel(portal)
        reporting_window.title("Reporting")
        reporting_window.geometry("900x900")

        # Reporting frame
        reporting_frame = tk.Frame(reporting_window, bg="white")
        reporting_frame.pack(side="left", fill="both", padx=1, pady=0)
        reporting_frame.config(highlightbackground="white", highlightthickness=1)
        reporting_frame.config(highlightcolor="white")

        # sales report label
        sales_report_label = ttk.Label(reporting_frame, text="Sales Report")
        sales_report_label.pack(pady=10, anchor="center", fill="x")

        sep = ttk.Separator(reporting_frame, orient="horizontal")
        sep.pack(fill="x", pady=0)

        # options frame
        options_frame = tk.Frame(reporting_frame, bg="white")
        options_frame.pack(side="top", fill="x", padx=0, pady=0)
        options_frame.config(width=900, height=50)
        options_frame.config(highlightbackground="white", highlightthickness=1)
        options_frame.config(highlightcolor="white")


        # Sales report table
        sales_report_table = ttk.Treeview(reporting_frame)
        sales_report_table["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        sales_report_table.column("#0", width=0, stretch="no")
        sales_report_table.column("1", anchor="w", width=12)
        sales_report_table.column("2", anchor="w", width=12)
        sales_report_table.column("3", anchor="w", width=40)
        sales_report_table.column("4", anchor="w", width=200)
        sales_report_table.column("5", anchor="w", width=300)
        sales_report_table.column("6", anchor="w", width=50)
        sales_report_table.column("7", anchor="w", width=30)

        sales_report_table.heading("#0", text="", anchor="w")
        sales_report_table.heading("1", text="ID", anchor="w")
        sales_report_table.heading("2", text="OrderID", anchor="w")
        sales_report_table.heading("3", text="Unit Price", anchor="w")
        sales_report_table.heading("4", text="Name", anchor="w")
        sales_report_table.heading("5", text="Description", anchor="w")
        sales_report_table.heading("6", text="Sales", anchor="w")
        sales_report_table.heading("7", text="Quantity", anchor="w")

        sales_report_table.pack(fill="both", expand=True, padx=0, pady=0)



        # populate sales report table
        def populate_sales_report_table():
            # get all order items
            # crsr = DBConnect.cursor
            # conn = DBConnect.connection
            # crsr.execute("SELECT * FROM test.dbo.order_items")
            # rows = crsr.fetchall()
            # crsr.close()
            # conn.close()

            rows = OrderItemsRepo.GetRecord("*", "")

            # get name and description of each item
            for row in rows:
                # crsr = DBConnect.cursor
                # conn = DBConnect.connection
                # crsr.execute("SELECT * FROM test.dbo.products WHERE id=?", row[2])
                # product = crsr.fetchone()
                # crsr.close()
                # conn.close()
                product = ProductSKUsRepo.GetRecord("*", f"WHERE PRODUCT_ID = {row[2]}")

                sales_report_table.insert("", "end", text="", values=(row.get("ID"), row.get("ORDER_ID"), product.get("STOCK"), product.get("TITLE"), product.get("DESCRIPTION"), row.get("PRODUCT_ID"), row.get("AMOUNT")))
            
        populate_sales_report_table()



    def login():
        global is_admin, uname
        is_admin = False
        flag = False
        try:
            username = username_entry.get()
            password = password_entry.get()

            user = AuthServices.authenticate(username, password)

            # crsr = DBConnect.cursor
            # conn = DBConnect.connection
            # crsr.execute("SELECT * FROM test.dbo.users")
            # rows = crsr.fetchall()
            # crsr.close()
            # conn.close()
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Error", "Error connecting to database")
            return False


        if user is not None:
                if user[4] == "Y":
                    is_admin = True
                print("Login success!")
                flag = True

        # for row in user:
        #     # check if username is found and password matches
        #     if row[1] == username and row[3] == password:
        #         uname = username
        #         if row[4] == "1":
        #             is_admin = True
        #         print("Login success!")
        #         flag = True
        #         break

        else:   # If no break
            login_label.config(text="Login failed. Please try again.")      

 

        if flag:
            login_frame.destroy()
            title.destroy()
            sep = ttk.Separator(portal, orient="horizontal")
            sep.pack(fill="x", pady=0)
            menu_frame = tk.Frame(portal, bg="white")
            menu_frame.pack(fill="x", pady=0)
            menu_frame.config(width=900, height=25)
            menu_frame.config(highlightbackground="white", highlightthickness=1)
            menu_frame.config(highlightcolor="white")

            # product button
            product_button = ttk.Button(menu_frame, text="Products", command=lambda: mainpage(menu_frame), bootstyle="Success")
            product_button.pack(side="left")
            
            # Account button
            account_button = ttk.Button(menu_frame, text="My Account", command=lambda: myac(menu_frame), bootstyle="info")
            account_button.pack(side="left")

            print (f"Admin: {is_admin}")
            if is_admin:
                
                # Inventory button
                inventory_button = ttk.Button(menu_frame, text="(Admin) Inventory", command=lambda: inventory(menu_frame), bootstyle="warning")
                inventory_button.pack(side="left")

                # Users A/C button
                users_button = ttk.Button(menu_frame, text="(Admin) Users", command=lambda: admin_user(menu_frame), bootstyle="warning")
                users_button.pack(side="left")

                # Reporting button
                reporting_button = ttk.Button(menu_frame, text="(Admin) Reporting", command=lambda: reporting(menu_frame), bootstyle="warning")
                reporting_button.pack(side="left")

            # user name on the right top
            uname = username
            username_label = ttk.Label(menu_frame, text=username)
            username_label.pack(side="right", padx=10, pady=10)

        return flag
  
    portal = tk.Toplevel(root)
    root.withdraw()
    portal.title("COMP2411 DBMS Project Demo")
    portal.geometry("900x900")
    portal.minsize(500, 600)
    portal.resizable(True, True)
    portal.protocol("WM_DELETE_WINDOW", on_closing)

    # Title Label
    title = ttk.Label(portal, text="COMP2411 DBMS Project Demo", font=("TKDefaultFont", 24))
    caption = ttk.Label(portal, text="Online Shopping System (OSS)", font=("TKDefaultFont", 16))
    
    # Login Frame
    login_frame = tk.Frame(portal, bg="white")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")
    login_frame.config(width=500, height=300)
    login_frame.config(highlightbackground="white", highlightthickness=1)
    login_frame.config(highlightcolor="white")

    # Login Form
    username_label = ttk.Label(login_frame, text="Username:")
    username_entry = ttk.Entry(login_frame)

    password_label = ttk.Label(login_frame, text="Password:")
    password_entry = ttk.Entry(login_frame, show="*")

    login_button = ttk.Button(login_frame, text="Login", command=login, bootstyle="light", width=12)
    login_label = ttk.Label(login_frame, text="Please login to continue")

    def register():
       
       def open_register_window():
            # Create a new window for the inventory
            register_win = tk.Toplevel(portal)
            register_win.title("Register A/C")
            register_win.geometry("600x280")

            # My Account frame
            register_frame = tk.Frame(register_win, bg="white")
            register_frame.pack(side="left", fill="both", padx=1, pady=0)
            register_frame.config(highlightbackground="white", highlightthickness=1)
            register_frame.config(highlightcolor="white")

            # My Account label
            myac_label = ttk.Label(register_frame, text="My A/C")
            myac_label.pack(pady=10, padx=270, anchor="center", fill="x")

            sep = ttk.Separator(register_frame, orient="horizontal")
            sep.pack(fill="x", pady=0)

            # Account Details frame
            account_details_frame = tk.Frame(register_frame, bg="white")
            account_details_frame.pack(side="top", fill="x", padx=0, pady=0)
            account_details_frame.config(width=600, height=600)
            account_details_frame.config(highlightbackground="white", highlightthickness=1)
            account_details_frame.config(highlightcolor="white")

            # username display
            username_label = ttk.Label(account_details_frame, text="Username")
            username_label.place(x=100, y=24, anchor="e")

            username_entry = ttk.Entry(account_details_frame)
            username_entry.place(x=110, y=24, anchor="w")
            username_entry.insert(0, "")

            # password display
            password_label = ttk.Label(account_details_frame, text="Password")
            password_label.place(x=100, y=59, anchor="e")

            password_entry = ttk.Entry(account_details_frame)
            password_entry.place(x=110, y=59, anchor="w")

            # password confirmation display
            password_confirm_label = ttk.Label(account_details_frame, text="Retype")
            password_confirm_label.place(x=100, y=93, anchor="e")

            password_confirm_entry = ttk.Entry(account_details_frame, show="*")
            password_confirm_entry.place(x=110, y=93, anchor="w")

            # Separator
            sep2 = ttk.Separator(account_details_frame, orient="horizontal")
            sep2.place(x=0, y=110, relwidth=1)

            # Contact Details label
            contact_details_label = ttk.Label(account_details_frame, text="Contact Details")
            contact_details_label.place(x=100, y=130, anchor="e")
            
  
            # Contact Name Entry
            contact_name_entry = ttk.Entry(account_details_frame)
            contact_name_entry.place(x=110, y=130, anchor="w")

            # Contact Number Label
            contact_number_label = ttk.Label(account_details_frame, text="Tel.")
            contact_number_label.place(x=277, y=130, anchor="w")

            # Contact Number Entry
            contact_number_entry = ttk.Entry(account_details_frame)
            contact_number_entry.place(x=310, y=130, anchor="w")

            # Address Label
            address_label = ttk.Label(account_details_frame, text="Address")
            address_label.place(x=100, y=160, anchor="e")

            # Address Entry
            address_entry = ttk.Entry(account_details_frame, width=42)
            address_entry.place(x=110, y=165, anchor="w")

            # Separator
            sep3 = ttk.Separator(account_details_frame, orient="horizontal")
            sep3.place(x=0, y=190, relwidth=1)

            def post_details():
                if password_entry.get() == "":
                        tk.messagebox.showerror("Error", "Password cannot be empty")
                        return
                if password_entry.get() != password_confirm_entry.get():
                   
                    tk.messagebox.showerror("Error", "Passwords do not match")
                    return
                else:
                    try:
                        # add user to database with username, "", password, "0", contact_name, contact_number, details
                        # crsr = DBConnect.cursor
                        # conn = DBConnect.connection
                        # crsr.execute("INSERT INTO test.dbo.users (username, password, is_admin, contact_name, contact_number, details) VALUES (?, ?, ?, ?, ?, ?)", username_entry.get(), password_entry.get(), "0", contact_name_entry.get(), contact_number_entry.get(), address_entry.get())
                        # conn.commit()
                        # crsr.close()
                        # conn.close()
                        UserRepo.create(username_entry.get(), "null", password_entry.get(), "N")

                        tk.messagebox.showinfo("Success", "Account created")
                        register_win.destroy()

                    except Exception as e:
                        print(e)
                        register_win.destroy()
            # Update Details button
            update_details_button = ttk.Button(account_details_frame, text="Register Details", bootstyle="warning", command=post_details)
            update_details_button.place(x=5, y=210, anchor="w")
       open_register_window()

    # register button
    register_button = ttk.Button(login_frame, text="Register", bootstyle="light", width=12, command=register)
    
    # Grid layout
    username_label.grid(row=0, column=0, padx=10, pady=10)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_label.grid(row=1, column=0, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    login_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=3)
    register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=3)
    
    # pack
    title.pack(pady=10)
    caption.pack(pady=10)
    login_frame.pack(pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(theme="darkly")
    root = style.master
    main(root)
    
    root.withdraw()
    root.mainloop()