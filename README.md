# BloodLife - Blood Donation Website

A simple blood donation website built with **Python Flask** and **MySQL**. Users can find blood donors, register as donors, and admins can manage the database.

## Quick Start (3 Steps)

### Step 1: Install Requirements
- [Python 3.x](https://www.python.org/downloads/) (check "Add to PATH" during install)
- [XAMPP](https://www.apachefriends.org/) (for MySQL database)

### Step 2: Setup Database
1. Start **XAMPP** → Start **MySQL**
2. Open **phpMyAdmin**: http://localhost/phpmyadmin
3. Click **SQL** tab
4. Paste contents of `database/init.sql`
5. Click **Go**

### Step 3: Run the Project
**Option A:** Double-click `run.bat`

**Option B:** Open terminal and run:
```bash
pip install flask pymysql
python app.py
```

### Open in Browser
- **Home:** http://localhost:5000
- **Find Donors:** http://localhost:5000/donors
- **Register:** http://localhost:5000/register
- **Admin:** http://localhost:5000/admin (username: `admin`, password: `admin123`)

---

## Project Structure
```
blood-donation-python/
├── app.py                  # Main Python file (all logic)
├── run.bat                 # Double-click to run
├── requirements.txt        # Python packages needed
├── database/
│   └── init.sql            # Database setup script
├── templates/
│   ├── base.html           # Common layout
│   ├── index.html          # Home page
│   ├── donors.html         # Find donors
│   ├── register.html       # Register form
│   ├── donor_detail.html   # Donor profile
│   ├── admin.html          # Admin login
│   └── dashboard.html      # Admin dashboard
└── static/
    ├── style.css           # All styles
    └── script.js           # Navigation toggle
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Home Page** | Shows stats and blood groups |
| **Find Donors** | Search by name/location, filter by blood group |
| **Register** | Form to become a blood donor |
| **Donor Profile** | View full donor details |
| **Admin Panel** | Login, view all donors, add/delete donors |

---

## Tech Stack
- **Backend:** Python + Flask
- **Database:** MySQL (XAMPP)
- **Frontend:** HTML + CSS + JavaScript
- **API:** JSON REST API

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/stats` | Get statistics |
| GET | `/api/donors` | List all donors (supports `?search=`, `?blood=`, `?location=`) |
| GET | `/api/donors/<id>` | Get one donor |
| POST | `/api/donors` | Add new donor (JSON body) |
| DELETE | `/api/donors/<id>` | Delete donor (admin only) |
| POST | `/api/login` | Admin login |
| POST | `/api/logout` | Admin logout |

---

## Common Issues

**"Python not found"**
- Reinstall Python and check "Add to PATH"

**"Can't connect to MySQL"**
- Make sure XAMPP MySQL is running (green status)

**"Database not found"**
- Run the `database/init.sql` script in phpMyAdmin first
