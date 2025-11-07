-- Assignment 5: Simple Database Creation
-- Creating a database and table with name and address fields

-- Create the database
CREATE DATABASE SimpleContactDB;

-- Use the database
USE SimpleContactDB;

-- Create a table with name and address fields
CREATE TABLE Contacts (
    ContactID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255)
);

-- Insert some sample data
INSERT INTO Contacts (Name, Address) VALUES 
('John Smith', '123 Main Street, Anytown, ST 12345'),
('Jane Doe', '456 Oak Avenue, Another City, ST 67890'),
('Bob Johnson', '789 Pine Road, Some Town, ST 54321');

-- Query to view the data
SELECT * FROM Contacts;