## IMPORTS
from customtkinter import * ##NEW TKINTER
import customtkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk ##IMAGES
import datetime as dt ##CLOCK
from datetime import date 
from time import strftime 
import os ##SAVING FILE (RECEIPT)
import pywinstyles ##HEADER
import random ##REFERENCE NUMBER
import math
from fpdf import FPDF


## WINDOW
title_menu = CTk()
title_menu.title("Welcome Page")
title_menu.geometry("1280x720")
title_menu.resizable(False, False)
title_menu._set_appearance_mode("dark")
pywinstyles.change_header_color(title_menu, color="#A72413") 
pywinstyles.change_title_color(title_menu, color="#FFCE21") 
title_menu.wm_attributes('-transparentcolor')

## FOR PAGE TURNING (SEAMLESS PAGE TURNING)
page1 = CTkFrame(title_menu) ##MAIN PAGE
page2 = CTkFrame(title_menu) ##DINE & TAKE OUT PAGE
page3 = CTkFrame(title_menu) ##LOGIN PAGE
page3_1 = CTkFrame(title_menu, width=1280, height=720) ##LOGIN PAGE
page4 = CTkFrame(title_menu, fg_color="#A72413") ##CREW PAGE
page5 = CTkFrame(title_menu, fg_color="#D34A24") ##CUSTOMER PAGE
page1.grid(row=0, column=0, sticky="nsew") 
page2.grid(row=0, column=0, sticky="nsew") 
page3.grid(row=0, column=0, sticky="nsew") 
page3_1.grid(row=0, column=0, sticky="nsew") 
page4.grid(row=0, column=0, sticky="nsew") 
page5.grid(row=0, column=0, sticky="nsew") 


## FRAMES (CREW PAGE)
header_frame = CTkFrame(page4, fg_color="#D34A24", width=1260, height=80, corner_radius=20,  bg_color="transparent")
header_frame.place(x=10, y=10)

item_frame = CTkFrame(page4, width=800, height=510, corner_radius=20, fg_color="#D34A24")
item_frame.place(x=10, y=105)

receipt_frame = CTkFrame(page4, width=430, height=605, corner_radius=20, fg_color="#D34A24")
receipt_frame.place(x=830, y=105)

receipt_fr = CTkScrollableFrame(receipt_frame, width=375, height=450, fg_color="#A72413", corner_radius=20, scrollbar_button_color="#D34A24")
receipt_fr.place(x=10, y=65)

## LOGIN PAGE
leftframe = CTkFrame(page3)
leftframe.grid(row=0, column=0, sticky="nsew")

rightframe = CTkFrame(page3, corner_radius=0, fg_color="#A72413")
rightframe.grid(row=0, column=1, sticky="nsew")

## FUNCTIONS
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path. join(base_path, relative_path)

## GLOBAL VARIABLES
order_number = random.randint(100, 999)
transaction_history_frame = None
orders = {}
total_price = 0
discount_applied = False
radio_var = StringVar(value="None") ##DINE IN AND TAKE OUT
customer_type_var = StringVar(value="PWD/Senior") 
item_images = {
    "Hakodate": ImageTk.PhotoImage(Image.open(resource_path("images/HAKODATE.png")).resize((100, 70))),
    "Kitakata": ImageTk.PhotoImage(Image.open(resource_path("images/KITAKITA.png")).resize((100, 70))),
    "Spicy Ramen": ImageTk.PhotoImage(Image.open(resource_path("images/SPICYRAMEN.png")).resize((100, 70))),
    "Shoyu Ramen": ImageTk.PhotoImage(Image.open(resource_path("images/SHOYURAMEN.png")).resize((100, 70))),
    "Tokushima": ImageTk.PhotoImage(Image.open(resource_path("images/TOKUSHIMA.png")).resize((100, 70))),
    "Yamagata": ImageTk.PhotoImage(Image.open(resource_path("images/YAMAGATA.png")).resize((100, 70))),
    "Takayama": ImageTk.PhotoImage(Image.open(resource_path("images/TAKAYAMARAMEN.png")).resize((100, 70))),
    "Shio Ramen": ImageTk.PhotoImage(Image.open(resource_path("images/SHIORAMEN.png")).resize((100, 70))),
    "Miso Ramen": ImageTk.PhotoImage(Image.open(resource_path("images/MISORAMEN.png")).resize((100, 70))),
    "Egg": ImageTk.PhotoImage(Image.open(resource_path("images/EGG.png")).resize((100, 70))),
    "Rice Cake": ImageTk.PhotoImage(Image.open(resource_path("images/TUBOL.png")).resize((100, 70))),
    "Noodle": ImageTk.PhotoImage(Image.open(resource_path("images/NOODLE.png")).resize((100, 70))),
    "Seaweed": ImageTk.PhotoImage(Image.open(resource_path("images/WEED.png")).resize((100, 70))),
    "Coke": ImageTk.PhotoImage(Image.open(resource_path("images/COKE.png")).resize((60, 70))),
    "Matcha": ImageTk.PhotoImage(Image.open(resource_path("images/MATCHA.png")).resize((60, 70))),
    "Iced Tea": ImageTk.PhotoImage(Image.open(resource_path("images/ICEDTEA.png")).resize((60, 70))),
}
def add_to_receipt(item_name, price):
    global total_price

    if item_name in orders:
        orders[item_name]['quantity'] += 1
        orders[item_name]['total_price'] += price
        orders[item_name]['widgets'][1].configure(text=f"{item_name} ({orders[item_name]['quantity']})")
    else:
        orders[item_name] = {'quantity': 1, 'total_price': price}

        scrollable_item_img_tk = item_images[item_name]
        scrollable_item_lbl = CTkLabel(scrollable_items, text="", image=scrollable_item_img_tk)
        scrollable_item_title = CTkLabel(scrollable_items, text=f"{item_name} (1)", font=("Montserrat", 15, "bold"))

        item_count = len(orders)
        row = (item_count - 1) // 100
        column = (item_count - 1) % 100

        scrollable_item_lbl.grid(row=row * 2, column=column, padx=10)
        scrollable_item_title.grid(row=row * 2 + 1, column=column)

        remove_button = CTkButton(scrollable_items, text="-", width=10, fg_color="#b02414", hover_color="#D34A24",
                                  font=("Roboto", 10, "bold"), text_color="#FFCE21",
                                  command=lambda item=item_name: remove_item(item, scrollable_item_lbl,
                                                                             scrollable_item_title, remove_button))
        remove_button.place(in_=scrollable_item_lbl, anchor="nw", bordermode="outside", relx=0.8, rely=0.1)

        orders[item_name]['widgets'] = (scrollable_item_lbl, scrollable_item_title, remove_button)

    total_price += price

    if discount_applied:
        apply_discount()  
    else:
        update_receipt()


## UPDATING RECEIPT
def update_receipt():
    global total_price, discount_applied
    for widget in receipt_fr.winfo_children():
        widget.destroy()
    CTkLabel(receipt_fr, text="Order", font=("Roboto", 20, "bold")).grid(row=0, column=0, padx=5, pady=5)
    CTkLabel(receipt_fr, text="Quantity", font=("Roboto", 20, "bold")).grid(row=0, column=2, padx=5, pady=5)
    CTkLabel(receipt_fr, text="Price", font=("Roboto", 20, "bold")).grid(row=0, column=3, padx=20, pady=5)

    subtotal = 0
    row_index = 1  

    for item_name, data in orders.items():
        quantity = data['quantity']
        total_price_item = data['total_price']
        subtotal += total_price_item

        CTkLabel(receipt_fr, text=item_name, font=("Montserrat", 15)).grid(row=row_index, column=0, padx=0, pady=5)
        CTkLabel(receipt_fr, text=quantity, font=("Montserrat", 15)).grid(row=row_index, column=2, padx=0, pady=5)
        CTkLabel(receipt_fr, text=f"P {total_price_item:.2f}", font=("Montserrat", 15)).grid(row=row_index, column=3, padx=0, pady=5)

        # Remove button
        remove_button = CTkButton(receipt_fr, text="X", width=3, fg_color="#A72413", hover_color="#D34A24",
                                  font=("Roboto", 10, "bold"), text_color="#FFCE21",
                                  command=lambda item=item_name: remove_item(item))
        remove_button.grid(row=row_index, column=1, padx=20, pady=0)

        # Void button
        void_button = CTkButton(receipt_fr, text="Clear", width=3, fg_color="#A72413", hover_color="#D34A24",
                                font=("Roboto", 10, "bold"), text_color="#FFCE21",
                                command=lambda item=item_name: void_item(item))
        void_button.grid(row=row_index, column=4, padx=0, pady=0)

        row_index += 1

    subtotal_label.configure(text=f"Subtotal:   P {subtotal:.2f}")

    vat_rate = 0.12
    total_price_with_vat = subtotal * (1 + vat_rate)

    if discount_applied:
        total_price_with_vat *= 0.80

    CTkLabel(receipt_fr, text=f"Total: \t\tP {total_price_with_vat:.2f}", font=("Roboto", 20, "bold"),
             text_color="#FFCE21").grid(row=row_index, column=0, columnspan=4, padx=10, pady=10)

    total_value.configure(text=f"P {total_price_with_vat:.2f}")



## SAVING RECEIPT
def save_receipt(total_price_with_vat, discount_applied, customer_money, change):
    global orders, total_price, radio_var, customer_type_var, order_number
    
    if not os.path.exists("receipts"):
        os.makedirs("receipts")
    if not os.path.exists("pdf_receipts"):
        os.makedirs("pdf_receipts")
    
    reference_number = random.randint(10000, 99999) 
    receipt_filename = f"receipts/receipt_{reference_number}.txt"
    receipt_filename_pdf = f"pdf_receipts/receipt_{reference_number}.pdf"

    if discount_applied:
        customer_type = customer_type_var.get()
        if customer_type == "PWD":
            discount_text = "PWD -20%"
        elif customer_type == "Senior Citizen":
            discount_text = "Senior Citizen -20%"
        else:
            discount_text = "None"
    else:
        discount_text = "None"

    dine_option = radio_var.get()  

    current_datetime = dt.datetime.now().strftime("%m-%d %I:%M %p")

    with open(receipt_filename, "w") as file:
        file.write(f"                 {order_number}\n")
        file.write(f"\n")
        file.write("---------------RECEIPT----------------\n")
        file.write("Order\t\tQuantity\tPrice\n")
        for item_name, data in orders.items():
            quantity = data['quantity']
            total_price_item = data['total_price']
            file.write(f"{item_name}\t{quantity}\t\t{total_price_item:.2f}\n")
        file.write("--------------------------------------\n")
        file.write(f"Subtotal:\t\tP {total_price:.2f}\n")
        file.write(f"Discount:\t\t{discount_text}\n")
        file.write(f"Amount Paid:\t\tP {customer_money:.2f}\n")
        file.write(f"VAT: 12%\n")
        file.write(f"Total Price\t\tP {total_price_with_vat:.2f}\n")
        file.write(f"Change Amount:\t\tP {change:.2f}\n")
        file.write("--------------------------------------\n")
        file.write(f"Option: {dine_option}\n")
        file.write(f"Reference #:\t\t{reference_number}\n")
        file.write(f"Date and Time:\t\t{current_datetime}\n")
        file.write("--------------------------------------\n\n")
        file.write("******NOW ACCEPTING APPLICATIONS******\n")
        file.write("        Text to 09218196410\n\n")
        file.write("---THANK YOU FOR CHOOSING RAMENILA!---\n")
        file.write("            COME AGAIN\n")
    
    messagebox.showinfo("Receipt Saved", f"Receipt saved as {receipt_filename}")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(receipt_filename, "r") as file:
        for line in file:
            pdf.cell(200, 10, txt=line, ln=True, align='L')

    pdf.output(receipt_filename_pdf)
    
    print(f"Receipt saved as {receipt_filename_pdf}")
    order_number = random.randint(100, 999)


## APPLYING 20% DISCOUNT
def apply_discount():
    global total_price, discount_applied
    discount_applied = True
    update_receipt()

def inquire_discount():
    messagebox.showinfo(title="Inquiry for Discount", message="Approach the front desk for the discount.")

def void_item(item_name):
    global total_price

    if item_name in orders:
        total_price -= orders[item_name]['total_price']
        del orders[item_name]

    update_receipt()

## VOIDING ITEMS
def remove_item(item_name, scrollable_item_lbl=None, scrollable_item_title=None, remove_button=None):
    global total_price
    if item_name in orders:
        price_per_unit = orders[item_name]['total_price'] / orders[item_name]['quantity']
        orders[item_name]['quantity'] -= 1
        orders[item_name]['total_price'] -= price_per_unit
        total_price -= price_per_unit

        if orders[item_name]['quantity'] <= 0:
            if scrollable_item_lbl:
                scrollable_item_lbl.destroy()
            if scrollable_item_title:
                scrollable_item_title.destroy()
            if remove_button:
                remove_button.destroy()
            del orders[item_name]
        else:
            orders[item_name]['widgets'][1].configure(text=f"{item_name} ({orders[item_name]['quantity']})")

    update_receipt()

## VOID ALL
def reset_item():
    global total_price, discount_applied
    total_price = 0
    orders.clear()
    discount_applied = False 
    update_receipt()

## 12% TAX
def apply_tax():
    global total_price
    total_price *= 1.12
    update_receipt()

## TITLE SWITCHING
def show_page(page, title):
    page.tkraise()
    title_menu.title(title)

def show_password():
    if pass_ent.cget('show') == "*":
        pass_ent.configure(show="")
    else:
        pass_ent.configure(show="*")

check_pass = Checkbutton(rightframe, text="Show password", command=show_password, bg="#A72413", font=("Roboto", 10), fg="#FFCE21", activebackground="#D34A24", activeforeground="#D34A24")
check_pass.place(x=70, y=460)

## FUNCTION FOR LOGIN
def login():
    username = usn_ent.get()
    password = pass_ent.get()
    if username == "user_admin" and password == "user_admin":
        messagebox.showinfo(title="Login Success", message="Login was Successful!")
        show_page(page4, "Crew Page")
    elif username == "echo" and password == "echo":
        messagebox.showinfo(title="Login Success", message="Login was Successful!")
        show_page(page4, "Crew Page")
    elif username == "i love my girlfriend" and password == "echo gf":
        messagebox.showinfo(title="Login Success", message="Login was Successful!")
        show_page(page4, "Crew Page")
    else:
        messagebox.showerror(title="Login Failed", message="Invalid username or password.")
    usn_ent.delete(0, END)
    pass_ent.delete(0, END)

def login1():
    def login2():
        username1 = usn1_ent.get()
        password1 = pass1_ent.get()
        if username1 == "user_admin" and password1 == "user_admin":
            messagebox.showinfo(title="Login Success", message="Login was Successful!")
            load_transaction_history()
        elif username1 == "echo" and password1 == "echo":
            messagebox.showinfo(title="Login Success", message="Login was Successful!")
            load_transaction_history()
        elif username1 == "i love my girlfriend" and password1 == "echo gf":
            messagebox.showinfo(title="Login Success", message="Login was Successful!")
            load_transaction_history()
        else:
            messagebox.showerror(title="Login Failed", message="Invalid username or password.")
        usn1_ent.delete(0, END)
        pass1_ent.delete(0, END)
    
    def show_password1():
        if pass1_ent.cget('show') == "*":
            pass1_ent.configure(show="")
        else:
            pass1_ent.configure(show="*")


    leftframe1 = CTkFrame(page3_1)
    leftframe1.grid(row=0, column=0, sticky="nsew")

    rightframe1 = CTkFrame(page3_1, height=100, width=800, corner_radius=0, fg_color="#A72413")
    rightframe1.grid(row=0, column=1, sticky="nsew")
    login1_image_left = Image.open(resource_path("images/INTRO_PIC.png")).resize((650, 720))
    login1_image_left_tk = ImageTk.PhotoImage(login1_image_left)
    login1_image_show = CTkLabel(leftframe1, text="", image=login1_image_left_tk)
    login1_image_show.pack(side=LEFT)

    go_back1 = CTkButton(rightframe1, text="< Previous Page", font=("Roboto", 15, "bold"), text_color="#FFCE21", command=lambda:show_page(page4, "Crew Page"), fg_color="#D34A24", hover_color="#D34A24")
    go_back1.place(x=70, y=34)

    welcome_lbl1 = CTkLabel(rightframe1, text="WELCOME BACK!", font=("Roboto", 50, "bold"), text_color="#FFCE21")
    welcome_lbl1.place(x=70, y=160)

    welc_sign1 = CTkLabel(rightframe1, text="Sign in to your account, Admin!", font=("Roboto", 20))
    welc_sign1.place(x=70, y=230)

    usn1_lbl = CTkLabel(rightframe1, text="Username:", font=("Roboto", 20), text_color="#FFCE21")
    usn1_lbl.place(x=70, y=280)

    usn1_ent = CTkEntry(rightframe1, placeholder_text="", height=40, width=400, border_color="#FFCE21", fg_color="#D34A24", font=("Roboto", 15))
    usn1_ent.place(x=70, y=310)

    pass1_lbl = CTkLabel(rightframe1, text="Password:", font=("Roboto", 20), text_color="#FFCE21")
    pass1_lbl.place(x=70, y=380)

    pass1_ent = CTkEntry(rightframe1, show="*", placeholder_text="", height=40, width=400, border_color="#FFCE21", fg_color="#D34A24", font=("Roboto", 15))
    pass1_ent.place(x=70, y=410)

    check_pass1 = Checkbutton(rightframe1, text="Show password", command=show_password1, bg="#A72413", font=("Roboto", 10), fg="#FFCE21", activebackground="#D34A24", activeforeground="#D34A24")
    check_pass1.place(x=70, y=460)


    login1_button = CTkButton(rightframe1, text="Login", width=400, fg_color="#FFCE21", hover_color="#D34A24", font=("Roboto", 15, "bold"), command=login2)
    login1_button.place(x=70, y=510)
    show_page(page3_1, "LOGIN PAGE ADMIN")


def load_transaction_history():
    global transaction_history_frame
    if transaction_history_frame:
        transaction_history_frame.destroy()
    
    transaction_history_frame = CTkFrame(title_menu, width=1280, height=720, fg_color="#D34A24")
    transaction_history_frame.grid(row=0, column=0, sticky="nsew")
    
    transaction_scrollable_frame = CTkScrollableFrame(transaction_history_frame, width=1200, height=600, orientation="horizontal", fg_color="#A72413", scrollbar_button_color="#D34A24")
    transaction_scrollable_frame.pack(pady=20)
    
    receipts_folder = "receipts"
    if not os.path.exists(receipts_folder):
        messagebox.showerror("Error", "Receipts folder not found.")
        return
    
    receipt_files = sorted(os.listdir(receipts_folder))
    
    for index, receipt_file in enumerate(receipt_files):
        receipt_path = os.path.join(receipts_folder, receipt_file)
        with open(receipt_path, "r") as file:
            receipt_content = file.read()
        
        reference_number = "Unknown"
        for line in receipt_content.split("\n"):
            if line.startswith("Reference #:"):
                reference_number = line.split(":")[1].strip()
                break
        
        receipt_frame = CTkFrame(transaction_scrollable_frame, width=1000, height=550, corner_radius=20, fg_color="#D34A24")
        receipt_frame.pack(side="left", padx=10, pady=10)
        
        CTkLabel(receipt_frame, text=f"RECEIPT #{reference_number}", font=("Roboto", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        CTkLabel(receipt_frame, text=receipt_content, justify="left", font=("Roboto", 12), wraplength=980).pack(anchor="w", padx=10, pady=5)
    
    previous_button = CTkButton(transaction_history_frame, text="Previous", width=100, height=150, fg_color="#A72413",
                                hover_color="#D34A24", font=("Roboto", 12, "bold"), text_color="#FFCE21",
                                command=lambda: show_page(page4, "Crew Page"))
    previous_button.pack(side="bottom", pady=10)
    show_page(transaction_history_frame, "Transaction History")

def checkout():
    global orders, total_price, discount_applied, scrollable_items

    if not orders:
        messagebox.showerror("No Orders", "No orders placed. Please add items to your order.")
        return

    vat_rate = 0.12
    total_price_with_vat = total_price * (1 + vat_rate)

    if discount_applied:
        total_price_with_vat *= 0.80

    def prompt_for_money(total_price_with_vat, discount_applied):
        money_window = CTkToplevel(fg_color="#A72413")
        money_window.title("Enter Amount")
        money_window.geometry("400x200")

        CTkLabel(money_window, text="Enter the amount of money you have:", font=("Roboto", 15, "bold"),
                 text_color="#FFCE21").pack(pady=20)

        money_var = StringVar()
        money_entry = CTkEntry(money_window, textvariable=money_var, font=("Roboto", 15), corner_radius=10)
        money_entry.pack(pady=10)

        def confirm_money(total_price_with_vat, discount_applied):
            global total_price
            try:
                customer_money = float(money_var.get())
                if math.isclose(customer_money, total_price_with_vat, rel_tol=1e-9) or customer_money > total_price_with_vat:
                    change = customer_money - total_price_with_vat
                    messagebox.showinfo("Transaction Successful",
                                        f"Thank you for your payment!\nYour change is: P{change:.2f}")
                    save_receipt(total_price_with_vat, discount_applied, customer_money, change)
                    orders.clear()
                    total_price = 0
                    discount_applied = False
                    update_receipt()
                    for widget in scrollable_items.winfo_children():
                        widget.destroy()
                    money_window.destroy()
                else:
                    messagebox.showerror("Insufficient Funds",
                                         f"You do not have enough money.\nYou are short by: P{total_price_with_vat - customer_money:.2f}")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")

        confirm_button = CTkButton(money_window, text="Confirm",
                                   command=lambda: confirm_money(total_price_with_vat, discount_applied),
                                   fg_color="#FFCE21", bg_color="#A72413", text_color="#A72413", hover_color="#FFCE21", font=("Roboto", 16, "bold"))
        confirm_button.pack(pady=10)

    prompt_for_money(total_price_with_vat, discount_applied)


## LOGO
title_menu_iconpath = ImageTk.PhotoImage(Image.open(resource_path("images/LOGO.png")))
title_menu.wm_iconbitmap()
title_menu.iconphoto(False, title_menu_iconpath)

## GRID CONFIGS
title_menu.grid_rowconfigure(0, weight=1)
title_menu.grid_columnconfigure(0, weight=1)
page1.grid_rowconfigure(0, weight=1)
page1.grid_rowconfigure(1, weight=0)
page1.grid_columnconfigure(0, weight=1)
page3.grid_rowconfigure(0, weight=1)
page3.grid_columnconfigure(0, weight=0)
page3.grid_columnconfigure(1, weight=5)


############## PAGE 1 TITLE PAGE
## RAMENILA PICTURE
image_title = Image.open(resource_path('images/RAMENILA.png')).resize((1280, 700))
image_tk = ImageTk.PhotoImage(image_title)
title_picture = CTkButton(page1, text="", image=image_tk, corner_radius=0, border_width=0, hover_color="#D34A24",fg_color="#D34A24", command= lambda:show_page(page2, "Dine In or Take Out Page"))
title_picture.grid(row=0, column=0, sticky="n")

## TITLE BUTTON
nxt_page2 = CTkButton(page1, text="CONTINUE AS CUSTOMER", command=lambda: show_page(page2, "Customer Page"), height=70, width=1280, corner_radius=0, fg_color="#A72413", hover_color="#A72413", text_color="white", font=("Roboto", 35, "bold"))
nxt_page2.grid(row=1, column=0, sticky="s")

## LOGIN PICTURE AND BUTTON
login_image = Image.open(resource_path("images/LOGIN_ICN.png")).resize((70, 50))
login_image_tk = ImageTk.PhotoImage(login_image)
nxt_page3 = CTkButton(page1, text="", command=lambda: show_page(page3, "Login Page"), image=login_image_tk, corner_radius=0, fg_color="#A72413", hover_color="#A72413", height=70)
nxt_page3.grid(row=1, column=0, sticky="e")


############## PAGE 2 DINE IN AND TAKE OUT PAGE
page2_img = Image.open(resource_path("images/DI_TO.png")).resize((1280, 720))
page2_img_tk = ImageTk.PhotoImage(page2_img)
page2_img_lbl = CTkLabel(page2, text="", image=page2_img_tk)
page2_img_lbl.place(x=0, y=0)

## DINE IN AND TAKE OUT BUTTONS
dine_in_btn_pg2 = CTkButton(page2, fg_color='#A82717',bg_color="#A82717", hover_color="#A82717", height=200, width=240, text="Dine In", font=("Roboto", 60, "bold"), command= lambda: [radio_var.set("Dine In"), show_page(page5, "Customer Page")], text_color="#FFCE21")
dine_in_btn_pg2.place(x=315, y=440)
take_out_btn_pg2 = CTkButton(page2, fg_color='#A82717',bg_color="#A82717", hover_color="#A82717", height=180, width=230, text="Take Out", font=("Roboto", 60, "bold"), command= lambda:[radio_var.set("Take Out"), show_page(page5, "Customer Page")], text_color="#FFCE21")
take_out_btn_pg2.place(x=730, y=450)

go_back_pg2 = CTkButton(page2, text="< Previous Page", font=("Roboto", 15), text_color="WHITE", command=lambda:show_page(page1, "Welcome Page"), fg_color="#A72413", hover_color="#A72413", border_width=5, border_color="#dcc3b4", bg_color="#D34A24")
go_back_pg2.place(x=575, y=670)


############## PAGE 5 (CUSTOMER PAGE)
## RAMENILA LOGO TO GO BACK TO PAGE 1
ramenila_logo_img = Image.open(resource_path("images/RAMENILALOGO.png")).resize((150, 100))
ramenila_logo_img_tk = ImageTk.PhotoImage(ramenila_logo_img)
ramenila_logo = customtkinter.CTkButton(page5, text="", command=lambda: show_page(page1, "Welcome Page"), bg_color='#D34A24', fg_color="#D34A24", hover_color="#D34A24", image=ramenila_logo_img_tk)
ramenila_logo.place(x=20, y=0)

orders_page5 = CTkScrollableFrame(page5, height=480, width=980, fg_color="#A72413", corner_radius=20, scrollbar_button_color="#D34A24")
orders_page5.place(x=250, y=10)

add_ons_page5 = CTkFrame(page5, height=400, width=200, fg_color="#A72413", corner_radius=20)
add_ons_page5.place(x=0, y=135)


## LOWER RIGHT 
frame_details = CTkFrame(page5, height=300, width=1200, fg_color="white",corner_radius=50)
frame_details.place(x=160, y=550)

scrollable_items = CTkScrollableFrame(frame_details, height=100, width=700, fg_color="#D34A24", orientation="horizontal", corner_radius=20,scrollbar_button_color="#A72413")
scrollable_items.place(x=20, y=20)

subtotal_label = CTkLabel(orders_page5, text="Subtotal:", font=("Montserrat", 40), text_color="#FFCE21", bg_color="#A72413")
subtotal_label.place(x=580, y=18)

total_label = CTkLabel(orders_page5, text="Total + VAT:", font=("Montserrat", 15), text_color="#FFCE21", bg_color="#A72413")
total_label.place(x=625, y=65)
total_value = CTkLabel(orders_page5, text="", font=("Montserrat", 15, "bold"), text_color="#FFCE21", bg_color="#A72413")
total_value.place(x=800, y=65)

checkout_btn_customer = CTkButton(frame_details, text="CHECK OUT", width=180, height=120, fg_color="#D34A24", hover_color="#A72413", font=("Montserrat", 30, "bold"), text_color="#FFCE21", command=checkout, corner_radius=20, bg_color="white")
checkout_btn_customer.place(x=835, y=25)

## ADD ONS LEFT
add_ons_lbl_page5 = CTkLabel(add_ons_page5, text="ADD-ONS:", font=("Segoe Script", 21, "bold"), text_color="#FFCE21")
add_ons_lbl_page5.place(x=35, y=20)

egg_img = Image.open(resource_path("images/EGG.png")).resize((70, 70))
egg_img_tk = ImageTk.PhotoImage(egg_img)
egg_add = CTkButton(add_ons_page5, text="", image=egg_img_tk, fg_color="transparent", hover_color="#D34A24", command=lambda: add_to_receipt("Egg", 15))
egg_add.place(x=35, y=60)

rice_cake_img = Image.open(resource_path("images/TUBOL.png")).resize((70, 70))
rice_cake_img_tk = ImageTk.PhotoImage(rice_cake_img)
rice_cake_add = CTkButton(add_ons_page5, text="", image=rice_cake_img_tk, fg_color="transparent", hover_color="#D34A24", command=lambda: add_to_receipt("Rice Cake", 20))
rice_cake_add.place(x=35, y=140)

noodle_img = Image.open(resource_path("images/NOODLE.png")).resize((70, 70))
noodle_img_tk = ImageTk.PhotoImage(noodle_img)
noodle_add = CTkButton(add_ons_page5, text="", image=noodle_img_tk, fg_color="transparent", hover_color="#D34A24", command=lambda: add_to_receipt("Noodle", 25))
noodle_add.place(x=35, y=230)

weed_img = Image.open(resource_path("images/WEED.png")).resize((70, 70))
weed_img_tk = ImageTk.PhotoImage(weed_img)
weed_add = CTkButton(add_ons_page5, text="", image=weed_img_tk, fg_color="transparent", hover_color="#D34A24", command=lambda: add_to_receipt("Seaweed", 10))
weed_add.place(x=35, y=310)

## ORDERS

orders_label = CTkLabel(orders_page5, text="Ramen",font=("Segoe Script", 50, "bold"), text_color="#FFCE21")
orders_label.grid(row=0, column=0)

hako_img = Image.open(resource_path("images/HAKODATE.png")).resize((150, 150))
hako_img_tk = ImageTk.PhotoImage(hako_img)
hako_order = CTkButton(orders_page5, text="Hakodate", compound= "top",image=hako_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Hakodate", 150), border_width=10, border_color="#D34A24")
hako_order.grid(row=1, column=0, padx=40, pady=35)
hako_lbl = CTkLabel(orders_page5, text="P 150", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
hako_lbl.place(x=120, y=340) 

ktkt_img = Image.open(resource_path("images/KITAKITA.png")).resize((150, 150))
ktkt_img_tk = ImageTk.PhotoImage(ktkt_img)
ktkt_order = CTkButton(orders_page5, text="Kitakata", compound= "top",image=ktkt_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Kitakata", 270), border_width=10, border_color="#D34A24")
ktkt_order.grid(row=1, column=1, padx=40, pady=35)
ktkt_lbl = CTkLabel(orders_page5, text="P 270", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
ktkt_lbl.place(x=460, y=340) 

sr_img = Image.open(resource_path("images/SPICYRAMEN.png")).resize((150, 150))
sr_img_tk = ImageTk.PhotoImage(sr_img)
sr_order = CTkButton(orders_page5, text="Spicy Ramen", compound= "top",image=sr_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Spicy Ramen", 150), border_width=10, border_color="#D34A24")
sr_order.grid(row=1, column=2, padx=40, pady=35)
sr_lbl = CTkLabel(orders_page5, text="P 150", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
sr_lbl.place(x=780, y=340) 

shoyu_img = Image.open(resource_path("images/SHOYURAMEN.png")).resize((150, 150))
shoyu_img_tk = ImageTk.PhotoImage(shoyu_img)
shoyu_order = CTkButton(orders_page5, text="Shoyu Ramen", compound= "top",image=shoyu_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Shoyu Ramen", 200), border_width=10, border_color="#D34A24")
shoyu_order.grid(row=2, column=0, padx=40, pady=35)
shoyu_lbl = CTkLabel(orders_page5, text="P 200", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
shoyu_lbl.place(x=120, y=620) 

th_img = Image.open(resource_path("images/TOKUSHIMA.png")).resize((150, 150))
th_img_tk = ImageTk.PhotoImage(th_img)
th_order = CTkButton(orders_page5, text="Tokushima", compound= "top",image=th_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Tokushima", 250), border_width=10, border_color="#D34A24")
th_order.grid(row=2, column=1, padx=40, pady=35)
th_lbl = CTkLabel(orders_page5, text="P 250", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
th_lbl.place(x=460, y=620) 

yg_img = Image.open(resource_path("images/YAMAGATA.png")).resize((150, 150))
yg_img_tk = ImageTk.PhotoImage(yg_img)
yg_order = CTkButton(orders_page5, text="Yamagata", compound= "top",image=yg_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Yamagata", 150), border_width=10, border_color="#D34A24")
yg_order.grid(row=2, column=2, padx=40, pady=35)
yg_lbl = CTkLabel(orders_page5, text="P 150", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
yg_lbl.place(x=780, y=620) 

ty_img = Image.open(resource_path("images/TAKAYAMARAMEN.png")).resize((150, 150))
ty_img_tk = ImageTk.PhotoImage(ty_img)
ty_order = CTkButton(orders_page5, text="Takayama Ramen", compound= "top",image=ty_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Takayama", 200), border_width=10, border_color="#D34A24")
ty_order.grid(row=3, column=0, padx=40, pady=35)
ty_lbl = CTkLabel(orders_page5, text="P 200", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
ty_lbl.place(x=120, y=900) 

shio_img = Image.open(resource_path("images/SHIORAMEN.png")).resize((150, 150))
shio_img_tk = ImageTk.PhotoImage(shio_img)
shio_order = CTkButton(orders_page5, text="Shio Ramen", compound= "top",image=shio_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Shio Ramen", 200), border_width=10, border_color="#D34A24")
shio_order.grid(row=3, column=1, padx=10, pady=35)
shio_lbl = CTkLabel(orders_page5, text="P 200", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
shio_lbl.place(x=460, y=900) 

miso_img = Image.open(resource_path("images/MISORAMEN.png")).resize((150, 150))
miso_img_tk = ImageTk.PhotoImage(miso_img)
miso_order = CTkButton(orders_page5, text="Miso Ramen", compound= "top",image=miso_img_tk, height=120, width=250, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Miso Ramen", 200), border_width=10, border_color="#D34A24")
miso_order.grid(row=3, column=2, padx=10, pady=35)
miso_lbl = CTkLabel(orders_page5, text="P 200", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
miso_lbl.place(x=780, y=900) 

drinks_label = CTkLabel(orders_page5, text="Drinks",font=("Segoe Script", 50, "bold"), text_color="#FFCE21")
drinks_label.grid(row=4, column=0)

ts_img = Image.open(resource_path("images/ICEDTEA.png")).resize((160, 250))
ts_img_tk = ImageTk.PhotoImage(ts_img)
ts_order = CTkButton(orders_page5, text="Iced Tea", compound="top", image=ts_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Iced Tea", 30), border_width=10, border_color="#D34A24")
ts_order.grid(row=5, column=0, padx=15, pady=25)
ts_lbl = CTkLabel(orders_page5, text="P 30", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
ts_lbl.grid(row=6, column=0)

mat_img = Image.open(resource_path("images/MATCHA.png")).resize((160, 250))
mat_img_tk = ImageTk.PhotoImage(mat_img)
mat_order = CTkButton(orders_page5, text="Matcha ", compound="top", image=mat_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Matcha", 50), border_width=10, border_color="#D34A24")
mat_order.grid(row=5, column=1, padx=15, pady=25)
mat_lbl = CTkLabel(orders_page5, text="P 50", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
mat_lbl.grid(row=6, column=1)

cok_img = Image.open(resource_path("images/COKE.png")).resize((160, 250))
cok_img_tk = ImageTk.PhotoImage(cok_img)
cok_order = CTkButton(orders_page5, text="Coke", compound="top", image=cok_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Coke", 40), border_width=10, border_color="#D34A24")
cok_order.grid(row=5, column=2, padx=15, pady=25)
cok_lbl = CTkLabel(orders_page5, text="P 40", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
cok_lbl.grid(row=6, column=2)

############# PAGE 3 (LOGIN PAGE)
## RAMEN IMAGE
login_image_left = Image.open(resource_path("images/INTRO_PIC.png")).resize((650, 720))
login_image_left_tk = ImageTk.PhotoImage(login_image_left)
login_image_show = CTkLabel(leftframe, text="", image=login_image_left_tk)
login_image_show.pack(side=LEFT)

go_back = CTkButton(rightframe, text="< Previous Page", font=("Roboto", 15, "bold"), text_color="#FFCE21", command=lambda:show_page(page1, "Welcome Page"), fg_color="#D34A24", hover_color="#D34A24")
go_back.place(x=70, y=34)

welcome_lbl = CTkLabel(rightframe, text="WELCOME BACK!", font=("Roboto", 50, "bold"), text_color="#FFCE21")
welcome_lbl.place(x=70, y=160)

welc_sign = CTkLabel(rightframe, text="Sign in to your account, Crew!", font=("Roboto", 20))
welc_sign.place(x=70, y=230)

usn_lbl = CTkLabel(rightframe, text="Username:", font=("Roboto", 20), text_color="#FFCE21")
usn_lbl.place(x=70, y=280)

usn_ent = CTkEntry(rightframe, placeholder_text="", height=40, width=400, border_color="#FFCE21", fg_color="#D34A24", font=("Roboto", 15))
usn_ent.place(x=70, y=310)

pass_lbl = CTkLabel(rightframe, text="Password:", font=("Roboto", 20), text_color="#FFCE21")
pass_lbl.place(x=70, y=380)

pass_ent = CTkEntry(rightframe, show="*", placeholder_text="", height=40, width=400, border_color="#FFCE21", fg_color="#D34A24", font=("Roboto", 15))
pass_ent.place(x=70, y=410)

login_button = CTkButton(rightframe, text="Login", width=400, fg_color="#FFCE21", hover_color="#D34A24", font=("Roboto", 15, "bold"), command=login)
login_button.place(x=70, y=510)


############# PAGE 4 (CREW PAGE)
## DINE IN AND TAKE OUT BUTTON
dine_in_btn = CTkRadioButton(header_frame, text="Dine In", value="Dine In", variable=radio_var, font=("Roboto", 20), fg_color="#FFCE21", hover_color="#A72413")
dine_in_btn.place(x=1000, y=10)

take_out_btn = CTkRadioButton(header_frame, text="Take Out", value="Take Out", variable=radio_var, font=("Roboto", 20), fg_color="#FFCE21", hover_color="#A72413")
take_out_btn.place(x=1000, y=40)

pwd_radio_btn = CTkRadioButton(header_frame, text="PWD", variable=customer_type_var, value="PWD", font=("Roboto", 20), fg_color="#FFCE21", hover_color="#A72413")
pwd_radio_btn.place(x=800, y=10)

senior_radio_btn = CTkRadioButton(header_frame, text="Senior Citizen", variable=customer_type_var, value="Senior Citizen", font=("Roboto", 20), fg_color="#FFCE21", hover_color="#A72413")
senior_radio_btn.place(x=800, y=40)

discount_button = CTkButton(receipt_frame, text="Discount", width=50, fg_color="#A72413", hover_color="#D34A24", font=("Roboto", 15, "bold"), text_color="#FFCE21", command=apply_discount)
discount_button.place(x=160, y=565)

checkout_button = CTkButton(receipt_frame, text="Check Out", width=50, fg_color="#A72413", hover_color="#D34A24", font=("Roboto", 15, "bold"), text_color="#FFCE21", command=checkout)
checkout_button.place(x=320, y=565)

reset_button = CTkButton(receipt_frame, text="Reset", width=50, fg_color="#A72413", hover_color="#D34A24", font=("Roboto", 15, "bold"), text_color="#FFCE21", command=reset_item)
reset_button.place(x=20, y=565)

## TABVIEW
tabview = customtkinter.CTkTabview(item_frame, width=730, height=390, corner_radius=1, fg_color="transparent", border_width=0, segmented_button_fg_color="#A72413", segmented_button_selected_color="#D34A24", text_color="#FFCE21", segmented_button_unselected_color="#A72413")
tabview._segmented_button.configure(corner_radius=10,font=("Roboto", 15, "bold"))

tabview.place(x=10, y=5)
tabview.add("Ramen Menu")
tabview.add("Drinks Menu")

## FRAMES
ramen_menu_frame = customtkinter.CTkScrollableFrame(tabview.tab("Ramen Menu"), width=730, height=410, corner_radius=25, orientation="horizontal", fg_color="#A72413", scrollbar_button_color="#D34A24", scrollbar_button_hover_color="#A72413")
ramen_menu_frame.pack(fill="both", expand=True)

drinks_menu_frame = customtkinter.CTkScrollableFrame(tabview.tab("Drinks Menu"), width=730, height=410, corner_radius=25, orientation="horizontal", fg_color="#A72413", scrollbar_button_color="#D34A24", scrollbar_button_hover_color="#D34A24")
drinks_menu_frame.pack(fill="both", expand=True)

add_on_frame = CTkFrame(page4, width=800, height=70, corner_radius=15, fg_color="#D34A24")
add_on_frame.place(x=10, y=630)

## CONTENTS OF PAGE 4
title_header = CTkLabel(header_frame, text="RAMENILA", font=("Segoe Script", 50, "bold", "italic"), text_color="#FFCE21")
title_header.place(x=300, y=0)

time_header = CTkLabel(header_frame, text=strftime("%H:%M"), font=("Roboto", 20), text_color="white")
time_header.place(x=1180, y=40)

go_back_login = CTkButton(header_frame, text="< Previous Page", font=("Roboto", 20, "bold"), text_color="#FFCE21", command=lambda:show_page(page3, "Login Page"), fg_color="#D34A24", hover_color="#D34A24")
go_back_login.place(x=20, y=25)

crew_mode = CTkButton(header_frame, text="ADMIN MODE", width=20, font=("Roboto", 18), fg_color="#A72413", hover_color="#D34A24", text_color="#FFCE21", command=login1)
crew_mode.place(x=1105, y=10)

receipt_lbl = CTkLabel(receipt_frame, text="RECEIPT", font=("Segoe Script", 30, "bold"), text_color="#FFCE21")
receipt_lbl.place(x=150, y=10)

## ORDERS FOR RAMEN MENU
hako_img = Image.open(resource_path("images/HAKODATE.png")).resize((300, 280))
hako_img_tk = ImageTk.PhotoImage(hako_img)
hako_order = CTkButton(ramen_menu_frame, text="P 150", compound="top", image=hako_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Hakodate", 150), border_width=10, border_color="#D34A24")
hako_order.grid(row=0, column=0, padx=10, pady=10)
hako_lbl = CTkLabel(ramen_menu_frame, text="Hakodate", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
hako_lbl.grid(row=1, column=0, padx=10) 

ktkt_img = Image.open(resource_path("images/KITAKITA.png")).resize((300, 280))
ktkt_img_tk = ImageTk.PhotoImage(ktkt_img)
ktkt_order = CTkButton(ramen_menu_frame, text="P 270", compound="top", image=ktkt_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Kitakata", 270), border_width=10, border_color="#D34A24")
ktkt_order.grid(row=0, column=1, padx=10, pady=10)
ktkt_lbl = CTkLabel(ramen_menu_frame, text="Kitakata", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
ktkt_lbl.grid(row=1, column=1, padx=10)

sr_img = Image.open(resource_path("images/SPICYRAMEN.png")).resize((300, 280))
sr_img_tk = ImageTk.PhotoImage(sr_img)
sr_order = CTkButton(ramen_menu_frame, text="P 150", compound="top", image=sr_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Spicy Ramen", 150), border_width=10, border_color="#D34A24")
sr_order.grid(row=0, column=2, padx=10, pady=10)
sr_lbl = CTkLabel(ramen_menu_frame, text="Spicy Ramen", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
sr_lbl.grid(row=1, column=2, padx=10)

shoyu_img = Image.open(resource_path("images/SHOYURAMEN.png")).resize((300, 280))
shoyu_img_tk = ImageTk.PhotoImage(shoyu_img)
shoyu_order = CTkButton(ramen_menu_frame, text="P 200", compound="top", image=shoyu_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Shoyu Ramen", 200), border_width=10, border_color="#D34A24")
shoyu_order.grid(row=0, column=3, padx=10, pady=10)
shoyu_lbl = CTkLabel(ramen_menu_frame, text="Shoyu Ramen", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
shoyu_lbl.grid(row=1, column=3, padx=10)

th_img = Image.open(resource_path("images/TOKUSHIMA.png")).resize((300, 280))
th_img_tk = ImageTk.PhotoImage(th_img)
th_order = CTkButton(ramen_menu_frame, text="P 250", compound="top", image=th_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Tokushima", 250), border_width=10, border_color="#D34A24")
th_order.grid(row=0, column=4, padx=10, pady=10)
th_lbl = CTkLabel(ramen_menu_frame, text="Tokushima", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
th_lbl.grid(row=1, column=4, padx=10)

yg_img = Image.open(resource_path("images/YAMAGATA.png")).resize((300, 280))
yg_img_tk = ImageTk.PhotoImage(yg_img)
yg_order = CTkButton(ramen_menu_frame, text="P 150", compound="top", image=yg_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Yamagata", 150), border_width=10, border_color="#D34A24")
yg_order.grid(row=0, column=5, padx=10, pady=10)
yg_lbl = CTkLabel(ramen_menu_frame, text="Yamagata", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
yg_lbl.grid(row=1, column=5, padx=10)

ty_img = Image.open(resource_path("images/TAKAYAMARAMEN.png")).resize((300, 280))
ty_img_tk = ImageTk.PhotoImage(ty_img)
ty_order = CTkButton(ramen_menu_frame, text="P 200", compound="top", image=ty_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Takayama", 200), border_width=10, border_color="#D34A24")
ty_order.grid(row=0, column=6, padx=10, pady=10)
ty_lbl = CTkLabel(ramen_menu_frame, text="Takayama Ramen", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
ty_lbl.grid(row=1, column=6, padx=10)

shio_img = Image.open(resource_path("images/SHIORAMEN.png")).resize((300, 280))
shio_img_tk = ImageTk.PhotoImage(shio_img)
shio_order = CTkButton(ramen_menu_frame, text="P 200", compound="top", image=shio_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Shio Ramen", 200), border_width=10, border_color="#D34A24")
shio_order.grid(row=0, column=7, padx=10, pady=10)
shio_lbl = CTkLabel(ramen_menu_frame, text="Shio Ramen", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
shio_lbl.grid(row=1, column=7, padx=10)

miso_img = Image.open(resource_path("images/MISORAMEN.png")).resize((300, 280))
miso_img_tk = ImageTk.PhotoImage(miso_img)
miso_order = CTkButton(ramen_menu_frame, text="P 200", compound="top", image=miso_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Miso Ramen", 200), border_width=10, border_color="#D34A24")
miso_order.grid(row=0, column=8, padx=10, pady=10)
miso_lbl = CTkLabel(ramen_menu_frame, text="Miso Ramen", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
miso_lbl.grid(row=1, column=8, padx=10)

## DRINKS MENU
ts_img = Image.open(resource_path("images/ICEDTEA.png")).resize((160, 250))
ts_img_tk = ImageTk.PhotoImage(ts_img)
ts_order = CTkButton(drinks_menu_frame, text="P 30", compound="top", image=ts_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Iced Tea", 30), border_width=10, border_color="#D34A24")
ts_order.grid(row=0, column=0, padx=15, pady=25)
ts_lbl = CTkLabel(drinks_menu_frame, text="Iced Tea", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
ts_lbl.grid(row=1, column=0, padx=10)

mat_img = Image.open(resource_path("images/MATCHA.png")).resize((160, 250))
mat_img_tk = ImageTk.PhotoImage(mat_img)
mat_order = CTkButton(drinks_menu_frame, text="P 50 ", compound="top", image=mat_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Matcha", 50), border_width=10, border_color="#D34A24")
mat_order.grid(row=0, column=1, padx=15, pady=25)
mat_lbl = CTkLabel(drinks_menu_frame, text="Matcha", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
mat_lbl.grid(row=1, column=1, padx=10)

cok_img = Image.open(resource_path("images/COKE.png")).resize((160, 250))
cok_img_tk = ImageTk.PhotoImage(cok_img)
cok_order = CTkButton(drinks_menu_frame, text="P 40", compound="top", image=cok_img_tk, height=100, fg_color="#D34A24", hover_color="#A72413", font=("Roboto", 25, "bold"), text_color="#FFCE21", corner_radius=20, command=lambda: add_to_receipt("Coke", 40), border_width=10, border_color="#D34A24")
cok_order.grid(row=0, column=2, padx=15, pady=25)
cok_lbl = CTkLabel(drinks_menu_frame, text="Coke", font=("Segoe Script", 25, "bold"), text_color="#FFCE21")
cok_lbl.grid(row=1, column=2, padx=10)

## ADD-ONS
add_ons_lbl = CTkLabel(add_on_frame, text="ADD-ONS:", font=("Segoe Script", 21, "bold"), text_color="#FFCE21")
add_ons_lbl.grid(row=0, column=0, padx=20, pady=10) 

egg_img = Image.open(resource_path("images/EGG.png")).resize((50, 50))
egg_img_tk = ImageTk.PhotoImage(egg_img)
egg_add = CTkButton(add_on_frame, text="", image=egg_img_tk, fg_color="transparent", hover_color="#A72413", command=lambda: add_to_receipt("Egg", 15))
egg_add.grid(row=0, column=1, padx=10, pady=10)

rice_cake_img = Image.open(resource_path("images/TUBOL.png")).resize((50, 50))
rice_cake_img_tk = ImageTk.PhotoImage(rice_cake_img)
rice_cake_add = CTkButton(add_on_frame, text="", image=rice_cake_img_tk, fg_color="transparent", hover_color="#A72413", command=lambda: add_to_receipt("Rice Cake", 20))
rice_cake_add.grid(row=0, column=2, padx=10, pady=10)

noodle_img = Image.open(resource_path("images/NOODLE.png")).resize((50, 50))
noodle_img_tk = ImageTk.PhotoImage(noodle_img)
noodle_add = CTkButton(add_on_frame, text="", image=noodle_img_tk, fg_color="transparent", hover_color="#A72413", command=lambda: add_to_receipt("Noodle", 25))
noodle_add.grid(row=0, column=3, padx=10, pady=10)

weed_img = Image.open(resource_path("images/WEED.png")).resize((50, 50))
weed_img_tk = ImageTk.PhotoImage(weed_img)
weed_add = CTkButton(add_on_frame, text="", image=weed_img_tk, fg_color="transparent", hover_color="#A72413", command=lambda: add_to_receipt("Seaweed", 10))
weed_add.grid(row=0, column=4, padx=10, pady=10)

show_page(page1, "Welcome Page")

title_menu.mainloop()

##########MAIN_CODER_DELOSREYES APPRECIATION LINE OF CODE: I LOVE MY GIRLFRIEND WITH ALL MY HEART#############