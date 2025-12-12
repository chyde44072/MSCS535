# Database Roles and Access Control

## Differences Between Roles and Access

**Access** refers to the specific permissions that allow users to perform actions on database objects. These include permissions like SELECT, INSERT, UPDATE, DELETE, CREATE, and DROP.

**Roles** are collections of permissions that can be assigned to users. Instead of giving each user individual permissions, roles group related permissions together and can be assigned to multiple users at once.

### Key Differences:
- **Access**: Individual permissions (what you can do)
- **Roles**: Groups of permissions (job-based permission sets)

## Importance in Organizations

Establishing roles and access controls is important because:

1. **Security**: Limits what users can access and modify, reducing risk of data breaches
2. **Efficiency**: Easier to manage permissions for groups rather than individuals
3. **Compliance**: Helps meet regulatory requirements for data protection
4. **Accountability**: Makes it clear who has access to what data
5. **Least Privilege Principle**: Users only get the permissions they need for their job

## Secure Role Setup Instructions

### 1. Create a Database

```sql
CREATE DATABASE company_db;
```

### 2. Connect to the Database

```sql
\c company_db
```

### 3. Create Users

```sql
CREATE USER john_doe WITH PASSWORD 'SecurePass123!';
CREATE USER jane_smith WITH PASSWORD 'SecurePass456!';
CREATE USER bob_johnson WITH PASSWORD 'SecurePass789!';
```

### 4. Create Roles

```sql
CREATE ROLE read_only;
CREATE ROLE data_entry;
CREATE ROLE admin_role;
```

### 5. Grant Permissions to Roles

```sql
-- Read-only role: can only view data
GRANT CONNECT ON DATABASE company_db TO read_only;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only;

-- Data entry role: can view and add data
GRANT CONNECT ON DATABASE company_db TO data_entry;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO data_entry;

-- Admin role: full control
GRANT ALL PRIVILEGES ON DATABASE company_db TO admin_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_role;
```

### 6. Assign Roles to Users

```sql
GRANT read_only TO john_doe;
GRANT data_entry TO jane_smith;
GRANT admin_role TO bob_johnson;
```

## Summary

By setting up roles and access controls properly, organizations can protect their data while making it accessible to those who need it. Roles simplify management and ensure that security policies are consistently applied across all users.

## References

Kohnfelder, L. (2021). *Designing Secure Software*. Random House Publishing Services. https://reader2.yuzu.com/books/9781718501935

Richardson, T., & Thies, C. N. (2012). *Secure Software Design*. Jones & Bartlett Learning. https://reader2.yuzu.com/books/9781284102680
