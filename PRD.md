# Product Requirements Document (PRD)
## BloodLife - Blood Donation Website

---

### 1. Project Overview

**Project Name:** BloodLife
**Type:** Web Application (Student Project)
**Tech Stack:** Python Flask + MySQL + HTML/CSS/JS
**Purpose:** Connect blood donors with people who need blood

---

### 2. Problem Statement

When someone needs blood urgently, finding a matching donor is difficult. This website makes it easy to:
- Find donors by blood group and location
- Register as a blood donor
- Manage donor records (admin)

---

### 3. Target Users

| User | Description |
|------|-------------|
| **Donor** | Person who wants to register as a blood donor |
| **Patient/Relative** | Person looking for a blood donor |
| **Admin** | Person managing the donor database |

---

### 4. Features

#### 4.1 Home Page
- Display total donors, available donors, locations
- Show all 8 blood groups with donor counts
- "How It Works" section (3 steps)
- Buttons to Find Donors and Register

#### 4.2 Find Donors Page
- Search bar (search by name, location, phone)
- Filter by blood group (dropdown)
- Filter by location (dropdown)
- Donor cards showing: name, blood group, phone, location
- Call button and View Profile button

#### 4.3 Register Page
- Form fields: Name, Blood Group, Phone, Email, Location, Age, Gender, Address
- Required fields: Name, Blood Group, Phone, Location
- Form validation
- Success message after registration

#### 4.4 Donor Profile Page
- Full donor information
- Call button
- Back to Donors button

#### 4.5 Admin Panel
- Login with username/password
- Dashboard with stats
- List all donors in table
- Add new donor
- Delete donor
- Logout

---

### 5. Database Design

**Table: donors**

| Column | Type | Required |
|--------|------|----------|
| id | INT (auto) | Yes |
| name | VARCHAR(100) | Yes |
| blood_group | ENUM(A+,A-,B+,B-,AB+,AB-,O+,O-) | Yes |
| phone | VARCHAR(20) | Yes |
| email | VARCHAR(100) | No |
| location | VARCHAR(100) | Yes |
| address | TEXT | No |
| age | INT | No |
| gender | ENUM(Male,Female) | No |
| last_donation | DATE | No |
| is_available | BOOLEAN | Yes (default: true) |
| created_at | TIMESTAMP | Auto |

---

### 6. API Design

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/stats | Get website statistics |
| GET | /api/donors | List donors (with filters) |
| GET | /api/donors/:id | Get one donor |
| POST | /api/donors | Add new donor |
| DELETE | /api/donors/:id | Delete donor |
| POST | /api/login | Admin login |
| POST | /api/logout | Admin logout |

---

### 7. Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | / | Landing page with stats |
| Find Donors | /donors | Search and filter donors |
| Register | /register | Donor registration form |
| Donor Profile | /donor/:id | Individual donor details |
| Admin Login | /admin | Admin authentication |
| Dashboard | /admin/dashboard | Admin management panel |

---

### 8. Design Guidelines

- **Colors:** Blue primary (#2563EB), Orange accent
- **Font:** Inter (Google Fonts)
- **Style:** Clean, minimal, modern
- **Responsive:** Works on mobile, tablet, desktop
- **Icons:** Simple HTML entities (&#10084;, &#128222;, &#128205;)

---

### 9. Success Criteria

- [ ] User can search donors by name/location
- [ ] User can filter donors by blood group
- [ ] User can register as a donor
- [ ] Admin can login
- [ ] Admin can add/delete donors
- [ ] Website works on mobile devices
- [ ] All 8 blood groups supported

---

### 10. Future Enhancements (Optional)

- Donor availability toggle
- Blood request system
- Email notifications
- Donor edit functionality
- Location map integration
- Donor search history
