# Assignment 5: Database Fundamentals

## Part 1: SQL Code for Simple Database Creation

The SQL code to create a simple database with a table containing name and address fields is provided in `database_creation.sql`.

### Key Components:
1. **Database Creation**: `CREATE DATABASE SimpleContactDB;`
2. **Table Creation**: Creates a `Contacts` table with:
   - `ContactID`: Primary key (auto-incrementing integer)
   - `Name`: VARCHAR(100) field for storing names
   - `Address`: VARCHAR(255) field for storing addresses

## Part 2: Difference Between Database and Database Management System

### Database
A **database** is a structured collection of related data that is organized and stored in a systematic way. It contains:
- Tables with rows and columns
- The actual data records
- Relationships between different data elements
- Indexes and constraints

**Example**: The actual customer information, product data, and order records stored in an e-commerce company's system.

### Database Management System (DBMS)
A **Database Management System (DBMS)** is the software application that provides the interface and tools to interact with databases. It includes:
- Software for creating, maintaining, and accessing databases
- Tools for data definition, manipulation, and control
- Query processing capabilities
- Security and backup features
- User interface and administration tools

**Examples**: MySQL, PostgreSQL, Oracle Database, Microsoft SQL Server, MongoDB

### Key Differences:

| Aspect | Database | Database Management System |
|--------|----------|----------------------------|
| **Nature** | Collection of data | Software application |
| **Function** | Stores information | Manages and controls data access |
| **Components** | Tables, records, relationships | Query processors, storage engines, security modules |
| **Example** | Customer records in a CRM | MySQL, Oracle, SQL Server |
| **Dependency** | Requires DBMS to function | Can exist without specific databases |

### Analogy:
Think of a **database** as a filing cabinet full of organized documents, while the **DBMS** is like the office management system that controls who can access the filing cabinet, how files are organized, and provides tools to find and update information efficiently.