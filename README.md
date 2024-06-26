# HotelManagementApp
A comprehensive hotel management application built with Python, Tkinter, and various libraries for managing restaurant menus, customer orders, generating bills, handling online payments, sending email notifications, collecting feedback, and displaying sales data.

## Overview

HotelManagementApp is a comprehensive solution designed to streamline the management of a hotel's restaurant operations. The application provides functionalities such as managing restaurant menus, taking customer orders, generating bills with GST, handling online payments via UPI, sending email notifications, collecting customer feedback, and displaying sales data through Power BI dashboards.

## Features

- **Restaurant Menu Management:** Load and display different menus (breakfast, brunch, lunch, afternoon tea, dinner) from text files.
- **Order Processing:** Take customer orders, validate input, and calculate the total bill including GST.
- **Billing:** Generate PDF bills for customers.
- **Sales Record:** Save sales records to an Excel file.
- **Online Payment:** Generate QR codes for UPI payments.
- **Email Notifications:** Send email with bill attached to customers.
- **Customer Feedback:** Collect and save customer feedback.
- **Power BI Dashboard:** Display sales data through a Power BI dashboard.

## Technologies Used

- Python
- Tkinter
- openpyxl
- pandas
- reportlab
- qrcode
- Pillow
- pywebview
- smtplib

## Setup Instructions

### Prerequisites

Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/).

Install the required Python packages:
```bash
pip install tkinter openpyxl pandas reportlab qrcode pillow webview smtplib
```

### Running the Application

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/HotelManagementApp.git
    ```
2. Navigate to the project directory:
    ```bash
    cd HotelManagementApp
    ```
3. Run the application:
    ```bash
    python hotel_management_app.py
    ```

### Download Executable File

You can also download the executable file from the following Google Drive link:
[Download HotelManagementApp.exe](https://drive.google.com/drive/folders/1uGrFlx7Yr23GpmH5mSmRnabHG7QT2yLA?usp=drive_link)

## Usage

1. **Start the Application:** The main window allows you to input the receptionist's email, and choose different menus or functionalities like feedback and Power BI dashboard.
2. **Select Menu:** Choose from breakfast, brunch, lunch, afternoon tea, or dinner menus. The menu will be displayed with options to place orders.
3. **Place Order:** Enter the quantity for each item and confirm the order. You can continue ordering or proceed to generate the bill.
4. **Generate Bill:** A PDF bill will be generated and saved. The sales record is saved to an Excel file.
5. **Online Payment:** A QR code for UPI payment is generated and displayed.
6. **Send Email:** The bill is sent to the receptionist's email.
7. **Feedback:** Provide feedback which is saved for review.
8. **View Dashboard:** View sales data through a Power BI dashboard.

## File Structure

```
HotelManagementApp/
│
├── menus/
│   ├── Breakfast.txt
│   ├── Brunch.txt
│   ├── Lunch.txt
│   ├── Afternoon_Tea.txt
│   └── Dinner.txt
│
├── sales_record.xlsx
├── bill.pdf
├── payment.jpg
├── feedback.txt
│
└── hotel_management_app.py
```

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss your changes.


## Contact

For any inquiries, please contact Sachin Tambe at sachin.tabaji.tambe@gmail.com.

---

Thank you for using HotelManagementApp!
