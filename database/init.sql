CREATE DATABASE IF NOT EXISTS blood_donation;
USE blood_donation;

CREATE TABLE IF NOT EXISTS donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    blood_group ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    location VARCHAR(100) NOT NULL,
    age INT,
    gender ENUM('Male','Female','Other'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO donors (name, blood_group, phone, email, location, age, gender) VALUES
('Ahmed Rahman', 'A+', '01712345678', 'ahmed@email.com', 'Dhanmondi, Dhaka', 28, 'Male'),
('Fatima Khan', 'B+', '01812345679', 'fatima@email.com', 'Gulshan, Dhaka', 25, 'Female'),
('Rahim Uddin', 'O+', '01912345680', 'rahim@email.com', 'Uttara, Dhaka', 32, 'Male'),
('Nusrat Jahan', 'AB+', '01612345681', 'nusrat@email.com', 'Mirpur, Dhaka', 30, 'Female'),
('Kamal Hossain', 'A-', '01512345682', 'kamal@email.com', 'Banani, Dhaka', 35, 'Male'),
('Sabrina Akter', 'B-', '01312345683', 'sabrina@email.com', 'Motijheel, Dhaka', 27, 'Female'),
('Tanvir Ahmed', 'O-', '01412345684', 'tanvir@email.com', 'Mohammadpur, Dhaka', 29, 'Male'),
('Maliha Begum', 'AB-', '01712345685', 'maliha@email.com', 'Tejgaon, Dhaka', 26, 'Female'),
('Sakib Hassan', 'A+', '01812345686', 'sakib@email.com', 'Bashundhara, Dhaka', 31, 'Male'),
('Tasnim Ahmed', 'B+', '01912345687', 'tasnim@email.com', 'Lalmatia, Dhaka', 24, 'Female'),
('Imran Khan', 'O+', '01612345688', 'imran@email.com', 'Farmgate, Dhaka', 33, 'Male'),
('Ruma Akter', 'A+', '01512345689', 'ruma@email.com', 'Shahbag, Dhaka', 28, 'Female');
