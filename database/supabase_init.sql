-- ============================================================
-- BloodLife - Supabase (PostgreSQL) Database Initialization
-- Copy and paste this script into Supabase -> SQL Editor -> Run
-- ============================================================

-- 1. Create Donors Table
CREATE TABLE IF NOT EXISTS donors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    location VARCHAR(100) NOT NULL,
    address TEXT,
    message TEXT,
    age INT,
    gender VARCHAR(10),
    last_donation DATE,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create Admin Table
CREATE TABLE IF NOT EXISTS admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Insert Default Admin (Password: admin123)
INSERT INTO admin (username, password) 
VALUES ('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi')
ON CONFLICT (username) DO NOTHING;

-- 4. Insert Sample Donors Data
INSERT INTO donors (name, blood_group, phone, email, location, address, age, gender, last_donation, is_available) VALUES
('Ahmed Rahman', 'A+', '01712345678', 'ahmed@email.com', 'Dhanmondi, Dhaka', 'House 12, Road 5, Dhanmondi', 28, 'Male', '2026-01-15', TRUE),
('Fatima Khan', 'B+', '01812345679', 'fatima@email.com', 'Gulshan, Dhaka', 'Apartment 3B, Gulshan-2', 25, 'Female', '2026-02-20', TRUE),
('Rahim Uddin', 'O+', '01912345680', 'rahim@email.com', 'Uttara, Dhaka', 'Sector 7, House 8', 32, 'Male', '2025-12-10', TRUE),
('Nusrat Jahan', 'AB+', '01612345681', 'nusrat@email.com', 'Mirpur, Dhaka', 'Block C, House 15', 30, 'Female', '2026-03-05', TRUE),
('Kamal Hossain', 'A-', '01512345682', 'kamal@email.com', 'Banani, Dhaka', 'Road 11, House 3', 35, 'Male', '2026-01-28', TRUE),
('Sabrina Akter', 'B-', '01312345683', 'sabrina@email.com', 'Motijheel, Dhaka', 'Building 5, Floor 3', 27, 'Female', '2026-02-14', TRUE),
('Tanvir Ahmed', 'O-', '01412345684', 'tanvir@email.com', 'Mohammadpur, Dhaka', 'Street 8, House 22', 29, 'Male', '2026-03-10', TRUE),
('Maliha Begum', 'AB-', '01712345685', 'maliha@email.com', 'Tejgaon, Dhaka', 'Lane 3, Building 7', 26, 'Female', '2025-11-20', TRUE),
('Sakib Hassan', 'A+', '01812345686', 'sakib@email.com', 'Bashundhara, Dhaka', 'Block D, House 10', 31, 'Male', '2026-01-05', TRUE),
('Tasnim Ahmed', 'B+', '01912345687', 'tasnim@email.com', 'Lalmatia, Dhaka', 'Road 7, House 4', 24, 'Female', '2026-02-28', TRUE),
('Imran Khan', 'O+', '01612345688', 'imran@email.com', 'Farmgate, Dhaka', 'Building 12, Floor 2', 33, 'Male', '2026-03-15', TRUE),
('Ruma Akter', 'A+', '01512345689', 'ruma@email.com', 'Shahbag, Dhaka', 'House 6, Road 3', 28, 'Female', '2026-01-20', TRUE);
