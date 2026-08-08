Here's a step-by-step guide:
Step 1: Start XAMPP MySQL

1. Open XAMPP Control Panel
2. Click Start next to MySQL (turn green)
   Step 2: Initialize Database
3. Click Admin in XAMPP (opens phpMyAdmin)
4. Click SQL tab
5. Paste the entire contents of database/init.sql
6. Click Go — this creates the blood_donation database, donors table, admin table, and 12 sample donors
   Step 3: Install Python Dependencies
   Open terminal in the project folder and run:
   pip install flask pymysql
   Step 4: Start the Flask Server
   python app.py
   You'll see:
   Open: http://localhost:5000
   Admin: http://localhost:5000/admin
   Step 5: Open in Browser

- Homepage: http://localhost:5000
- Find Donors: http://localhost:5000/donors
- Register: http://localhost:5000/register
- Admin Panel: http://localhost:5000/admin (login: admin / admin123)
  Alternative: Instead of Steps 3-4, just double-click run.bat — it installs dependencies and starts the server automatically.
