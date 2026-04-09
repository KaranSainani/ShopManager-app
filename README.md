# ShopManager-app

**Retail Inventory & Sales Manager**

A desktop-based GUI application built with Python and SQLite designed to manage product inventory and streamline the sales process in a retail environment.

🚀 **Overview**


This project serves as a functional prototype for a retail Point of Sale (POS) system. It allows users to browse products, manage real-time stock levels, and process purchases through an intuitive graphical interface.

<br>
<br>

✨ **Key Features**

• Dynamic Inventory Display: Automatically renders products from a local database.

• Smart Stock Logic: Visual indicators (Green/Orange/Red) based on availability thresholds.

• Safety Controls: Prevents negative stock levels and "Out of Stock" selections via hardware-level logic.

• Real-time Cart Management: Incremental/decremental counters for item selection.

• Database Persistence: Full integration with SQLite for reliable data storage and inventory updates.

<br>
<br>

📂 **Project Structure**


• 🐍 virtualShop.py: The core application script managing the Graphical User Interface (GUI) and its interactive functions.

• 🗄️ database.py: Handles all database operations, including data retrieval (SELECT) and inventory updates (UPDATE). It ensures data integrity through secure transaction management (Commits).

• 💾 ShopManager.db: A lightweight SQLite database containing a single "Producto" (Product) table with all necessary columns for inventory management.

<br>
<br>

🛠️ **Libraries & Dependencies**


The following libraries were used to build this desktop application:

• 🆔 uuid: Utilized for generating Universally Unique Identifiers to ensure each sales bill has a distinct, non-repeatable ID.

• 📅 datetime: Implemented to track, record, and manipulate timestamps (date and time).

• 🖼️ tkinter: Python's standard library for creating the GUI (Graphical User Interface).

• 📄 reportlab: A powerful engine used to generate PDF documents, specifically for creating professional sales bills.

