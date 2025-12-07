# Secure Database Connection Example

## Overview
This document provides a example of secure code for a website using JavaScript and PHP for database connection. It demonstrates essential security practices to prevent SQL injection, XSS attacks, and insecure password storage.

---

## PHP Code (login.php)

```php
<?php
// Database connection using PDO
$pdo = new PDO(
    "mysql:host=localhost;dbname=mydatabase",
    "dbuser",
    "dbpassword",
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);

session_start();

// Get user input
$username = $_POST['username'];
$password = $_POST['password'];

// SECURE: Use prepared statement to prevent SQL injection
$stmt = $pdo->prepare("SELECT id, password_hash FROM users WHERE username = :username");
$stmt->bindParam(':username', $username);
$stmt->execute();
$user = $stmt->fetch();

// SECURE: Verify password with hash
if ($user && password_verify($password, $user['password_hash'])) {
    $_SESSION['user_id'] = $user['id'];
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['error' => 'Invalid credentials']);
}
?>
```

### Why This is Secure:
1. **Prepared Statements**: Uses `:username` placeholder instead of concatenating user input directly into SQL
2. **Password Hashing**: Passwords are hashed with `password_hash()` and verified with `password_verify()`
3. **Session Management**: Uses PHP sessions to track authenticated users

---

## JavaScript Code (app.js)

```javascript
// Login function
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch('login.php', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    });
    
    const data = await response.json();
    
    if (data.success) {
        alert('Login successful!');
    } else {
        alert(data.error);
    }
}

// Display user data safely
function displayData(name) {
    // SECURE: Use textContent instead of innerHTML to prevent XSS
    document.getElementById('user-name').textContent = name;
}
```

### Why This is Secure:
1. **URL Encoding**: Uses `encodeURIComponent()` to safely encode user input
2. **XSS Prevention**: Uses `textContent` instead of `innerHTML` to prevent script injection
3. **Async/Await**: Modern JavaScript for handling server responses

---

## Key Security Concepts

### 1. SQL Injection Prevention
**Problem**: Attackers can inject malicious SQL code
```php
// INSECURE - Don't do this!
$query = "SELECT * FROM users WHERE username = '$username'";
```

**Solution**: Use prepared statements
```php
// SECURE - Always do this!
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = :username");
$stmt->bindParam(':username', $username);
```

### 2. Password Security
**Problem**: Storing passwords in plain text
```php
// INSECURE - Don't do this!
$password = $_POST['password'];
$query = "INSERT INTO users (password) VALUES ('$password')";
```

**Solution**: Hash passwords
```php
// SECURE - Always do this!
$hashed = password_hash($password, PASSWORD_DEFAULT);
$stmt = $pdo->prepare("INSERT INTO users (password_hash) VALUES (:hash)");
```

### 3. XSS Prevention
**Problem**: User input displayed as HTML can execute scripts
```javascript
// INSECURE - Don't do this!
element.innerHTML = userInput;
```

**Solution**: Use textContent
```javascript
// SECURE - Always do this!
element.textContent = userInput;
```

---

## Database Setup

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Insert test user with hashed password
INSERT INTO users (username, password_hash) VALUES 
('testuser', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');
```

---

## Summary

**Three Essential Security Practices:**
1. **Use prepared statements** to prevent SQL injection
2. **Hash passwords** with `password_hash()` and `password_verify()`
3. **Use `textContent`** in JavaScript to prevent XSS attacks

## References

1. Kohnfelder, L. (2021). *Designing Secure Software*. Random House Publishing Services. https://reader2.yuzu.com/books/9781718501935

2. Richardson, T., & Thies, C. N. (2012). *Secure Software Design*. Jones & Bartlett Learning. https://reader2.yuzu.com/books/9781284102680
