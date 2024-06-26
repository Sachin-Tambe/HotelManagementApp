import tkinter as tk
from tkinter import messagebox, simpledialog
from openpyxl import Workbook
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import qrcode
from PIL import Image, ImageTk
from datetime import datetime
import webview  # Import pywebview
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Hotel:
    def __init__(self):
        self.restaurant_name = ''
        self.restaurant_menu = {}
        self.entries = {}
        self.overall_bill = 0
        self.root = None
        self.sales_record = []
        self.owner_upi_id = "tabajitambe76-1@okhdfcbank"
        self.owner_name = "Sachin Tambe"
        self.qr_image = None  # Keep a reference to the image object
        self.curr_date = datetime.now().strftime('%d-%m-%Y--%H:%M:%S')
        self.recipient_email = ""


    def read_details_from_file(self, filename):
        with open(filename) as file:
            user_input = file.readlines()
        for line in user_input:
            lines = line.strip().split(',')
            self.restaurant_name = lines[0].strip()
            self.restaurant_menu = eval(','.join(lines[1:]))

    def confirm_order(self):
        total_bill = 0
        sale_record = []
        for food, entry in self.entries.items():
            try:
                quantity = int(entry.get())
                if quantity < 0:
                    raise ValueError
                price = self.restaurant_menu[food]
                if quantity > 0:
                    total_bill += price * quantity
                    sale_record.append((food, price, quantity))
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid quantity for {food}. Please enter a valid non-negative number.")
        self.overall_bill += total_bill
        self.sales_record.append(sale_record)

        messagebox.showinfo("Order Confirmation", "Your order placed successfully".title())
        choice = messagebox.askyesno("More Order", "Do you want more order".title())
        if choice:
            self.root.destroy()
            self.show_menu()
        else:
            self.root.destroy()
            messagebox.showinfo("Bill", f"Your Bill is {self.overall_bill + (18/100) * self.overall_bill}")
            self.save_sales_record_to_excel()
            self.get_online_payment()
            self.show_image()
            self.show_bill()
            self.overall_bill = 0

    def save_sales_record_to_excel(self):
        sale_data = []
        for sale in self.sales_record:
            for food, price, quantity in sale:
                sale_data.append({ 'Customer_email': self.recipient_email , 'Food Item': food, 'price': price, 'Quantity': quantity, 'Date And Time': self.curr_date, 'Total Bill': quantity*price, 'Margin': (quantity*price) * (40/100)})
        df = pd.DataFrame(sale_data)
        file_path = 'sales_record.xlsx'
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            final_df = pd.concat([existing_df, df], ignore_index=True)
        else:
            final_df = df
        final_df.to_excel(file_path, index=False)

    def show_bill(self):
        pdf_filename = "bill.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 40, f"Bill From {self.restaurant_name}")
        c.drawString(100, height - 60, f"Total Bill + 18% GST ₹{self.overall_bill + (18/100) * self.overall_bill}")
        c.drawString(100, height - 80, f"Date And Time{self.curr_date}")

        y = height - 100
        c.drawString(100, y, "Food Item")
        c.drawString(300, y, "Price")
        c.drawString(400, y, "Quantity")
        y -= 20

        for sale_record in self.sales_record:
            for food, price, quantity in sale_record:
                c.drawString(100, y, food)
                c.drawString(300, y, str(price))
                c.drawString(400, y, str(quantity))
                y -= 20

        c.save()

####################################    #############################################
    def send_email_with_attachment(self):
        # Email account credentials
        email_address = "sachintambe907@gmail.com"
        email_password = "xmgf rthj ylmd hdkd"

        # SMTP server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # For STARTTLS

        # Recipient's email address
        recipient_email = self.recipient_email

        # Email content
        subject = "Restaurant Bill"
        body = """
        Dear Customer,

        Please find attached your bill from our restaurant.

        Thank you for dining with us!

        Best regards,
        Restaurant Team
        """

        # Path to the PDF file (bill) to be attached
        file_path = "bill.pdf"
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # Open PDF file in binary mode
        with open(file_path, 'rb') as attachment:
            # Add file as application/octet-stream
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {file_path}',
        )

        # Attach the attachment to the MIMEMultipart object
        msg.attach(part)

        try:
            # Create a secure SSL context and login
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(email_address, email_password)
                text = msg.as_string()
                server.sendmail(email_address, recipient_email, text)
        except Exception as e:
            pass
################################################
    def get_online_payment(self):
        if self.overall_bill > 0:
            upi_url = f"upi://pay?pa={self.owner_upi_id}&pn={self.owner_name}&am={self.overall_bill + (18/100) * self.overall_bill}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            qr.add_data(upi_url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save('payment.jpg')
        else:
            pass

    def show_image(self):
        if self.overall_bill > 0:
            payment_window = tk.Toplevel()
            payment_window.title("Payment Window")
            payment_window.geometry('500x500')

            image_path = r"C:\Users\sachi\OneDrive\Desktop\sachin python\payment.jpg"

            try:
                image = Image.open(image_path)
                self.qr_image = ImageTk.PhotoImage(image)
                label_image = tk.Label(payment_window, image=self.qr_image)
                label_image.pack()
            except FileNotFoundError:
                messagebox.showerror("Error", "Image file not found.")

            payment_window.mainloop()

    def show_menu(self):
        self.root = tk.Tk()
        self.root.title("Launch Menu")
        self.root.geometry("400x400")
        self.root.configure(bg="#F0F0F0")

        heading_label = tk.Label(self.root, text="Menu", font=("Arial", 20, "bold"), bg="#F0F0F0")
        heading_label.pack(pady=10)

        for food, price in self.restaurant_menu.items():
            frame = tk.Frame(self.root, bg="#F0F0F0")
            frame.pack(fill=tk.X, padx=10, pady=5)
            food_label = tk.Label(frame, text=f'{food}', bg="#F0F0F0")
            food_label.pack(side='left', padx=(10, 50))
            price_label = tk.Label(frame, text=f'₹{price}', bg="#F0F0F0")
            price_label.pack(side='right')
            entry = tk.Entry(frame, width=5)
            entry.insert(0, '0')  # Set the default value to 0
            entry.pack(side='right', padx=(0, 10))
            self.entries[food] = entry

        confirm_order_button = tk.Button(self.root, text='Place Order', command=self.confirm_order, bg="#4CAF50", fg="white")
        confirm_order_button.pack(pady=10)

        self.root.mainloop()

    def show_feedback_form(self):
        feedback_window = tk.Toplevel()
        feedback_window.title("Feedback Form")
        feedback_window.geometry('300x200')

        feedback_label = tk.Label(feedback_window, text="Please provide your feedback:", pady=10)
        feedback_label.pack()

        feedback_text = tk.Text(feedback_window, height=5, width=30)
        feedback_text.pack()

        submit_button = tk.Button(feedback_window, text="Submit Feedback", command=lambda: self.submit_feedback(feedback_text.get("1.0", tk.END)))
        submit_button.pack(pady=10)

        feedback_window.mainloop()

    def submit_feedback(self, feedback):
        with open("feedback.txt", "a") as file:
            file.write(feedback + "\n")
        messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")

    def show_power_bi_dashboard(self):
        # URL of the Power BI dashboard
        power_bi_url = 'https://somaiya0-my.sharepoint.com/:u:/g/personal/sachin_tambe_somaiya_edu/EeCLVZHhPvNAj-CpflG_1K4BqrVJZHUE_mQYN2cJekCmbQ?e=zU9FAR'
        # Open the Power BI dashboard in a new window using pywebview
        webview.create_window('Power BI Dashboard', power_bi_url)
        webview.start()

    def start_app(self):
        window = tk.Tk()
        window.title(self.restaurant_name)
        window.geometry('300x300')
        window.configure(bg="#F0F0F0")

        button_styles = {
            "font": ("Arial", 12),
            "bg": "#2196F3",
            "fg": "white",
            "padx": 10,
            "pady": 5,
            "bd": 0,
            "relief": tk.FLAT,
            "width": 20
        }

        def save_receptionist_email():
            self.recipient_email = receptionist_email_entry.get()
            messagebox.showinfo("Email Saved", f"Receptionist Email Saved: {self.recipient_email}")

        # Label and Entry for receptionist email
        receptionist_email_label = tk.Label(window, text="Receptionist Email:", bg="#F0F0F0")
        receptionist_email_label.pack(pady=(10, 5))

        receptionist_email_entry = tk.Entry(window, width=30)
        receptionist_email_entry.pack(pady=(0, 10))

        # Button to save receptionist email
        save_email_button = tk.Button(window, text="Save Email", command=save_receptionist_email, **button_styles)
        save_email_button.pack()

        # Menu buttons
        menu_buttons_frame = tk.Frame(window, bg="#F0F0F0")
        menu_buttons_frame.pack(pady=10)

        breakfast_button = tk.Button(menu_buttons_frame, text='Breakfast Menu', command=self.show_breakfast_menu, **button_styles)
        breakfast_button.pack(side=tk.TOP, pady=5)
        brunch_button = tk.Button(menu_buttons_frame, text='Brunch Menu', command=self.show_Brunch_menu, **button_styles)
        brunch_button.pack(side=tk.TOP, pady=5)
        lunch_button = tk.Button(menu_buttons_frame, text='Lunch Menu', command=self.show_Lunch_menu, **button_styles)
        lunch_button.pack(side=tk.TOP, pady=5)
        afternoon_tea_button = tk.Button(menu_buttons_frame, text='Afternoon Tea Menu', command=self.show_Afternoon_Tea_menu, **button_styles)
        afternoon_tea_button.pack(side=tk.TOP, pady=5)
        dinner_button = tk.Button(menu_buttons_frame, text='Dinner Menu', command=self.show_Dinner_menu, **button_styles)
        dinner_button.pack(side=tk.TOP, pady=5)

        # Additional buttons
        feedback_button = tk.Button(window, text='Feedback', command=self.show_feedback_form, **button_styles)
        feedback_button.pack(pady=5)
        dashboard_button = tk.Button(window, text='Power BI Dashboard', command=self.show_power_bi_dashboard, **button_styles)
        dashboard_button.pack(pady=5)

        window.mainloop()


    def show_breakfast_menu(self):
        self.read_details_from_file('Breakfast.txt')
        self.show_menu()

    def show_Brunch_menu(self):
        self.read_details_from_file('Brunch.txt')
        self.show_menu()

    def show_Lunch_menu(self):
        self.read_details_from_file('Lunch.txt')
        self.show_menu()

    def show_Afternoon_Tea_menu(self):
        self.read_details_from_file('Afternoon_Tea.txt')
        self.show_menu()

    def show_Dinner_menu(self):
        self.read_details_from_file('Dinner.txt')
        self.show_menu()

if __name__ == "__main__":
    rest = Hotel()
    rest.start_app()
    rest.send_email_with_attachment()
