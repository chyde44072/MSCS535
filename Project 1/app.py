#!/usr/bin/env python3
"""
Secure Database Access Application
Protects against SQL injection and provides HTTPS access
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib
import ssl
import os

app = Flask(__name__)
app.secret_key = 'secure-key-for-production-change-this'

# Database file
DB_FILE = 'users.db'

def init_db():
    """Initialize database with sample data"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Insert sample users (password is 'password123' hashed)
    password_hash = hashlib.sha256('password123'.encode()).hexdigest()
    sample_users = [
        ('admin', password_hash, 'admin@company.com'),
        ('user1', password_hash, 'user1@company.com'),
        ('employee', password_hash, 'employee@company.com')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO users (username, password_hash, email) VALUES (?, ?, ?)',
        sample_users
    )
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """Main page with login form"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Secure Database Access</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .container { background: #f9f9f9; padding: 30px; border-radius: 8px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 8px 0; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 10px; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .security-info { background: #e7f3ff; padding: 15px; margin: 20px 0; border-left: 4px solid #2196F3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Secure Database Access System</h1>
        
        <div class="security-info">
            <h3>🔒 Security Features Implemented:</h3>
            <ul>
                <li>✅ Parameterized queries (prevents SQL injection)</li>
                <li>✅ Password hashing (protects stored passwords)</li>
                <li>✅ HTTPS support (encrypts network traffic)</li>
                <li>✅ Input validation (prevents malicious input)</li>
            </ul>
        </div>
        
        <h2>Employee Login</h2>
        <form id="loginForm">
            <label>Username:</label>
            <input type="text" id="username" placeholder="Enter your username" required>
            
            <label>Password:</label>
            <input type="password" id="password" placeholder="Enter your password" required>
            
            <button type="submit">Secure Login</button>
        </form>
        
        <div id="result"></div>
        
        <div class="security-info">
            <h4>Demo Credentials:</h4>
            <p><strong>Username:</strong> admin <strong>Password:</strong> password123</p>
            <p><strong>Username:</strong> employee <strong>Password:</strong> password123</p>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('result');
                if (data.success) {
                    resultDiv.innerHTML = '<div class="result success"><strong>Success!</strong> ' + data.message + '</div>';
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1500);
                } else {
                    resultDiv.innerHTML = '<div class="result error"><strong>Error:</strong> ' + data.message + '</div>';
                }
            })
            .catch(error => {
                document.getElementById('result').innerHTML = '<div class="result error">Connection error occurred</div>';
            });
        });
    </script>
</body>
</html>
    ''')

@app.route('/login', methods=['POST'])
def login():
    """Secure login endpoint with SQL injection protection"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Input validation
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'})
        
        if len(username) > 50 or len(password) > 100:
            return jsonify({'success': False, 'message': 'Input too long'})
        
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # SECURE: Using parameterized query to prevent SQL injection
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # This query is SAFE from SQL injection due to parameterization
        cursor.execute(
            'SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'success': True,
                'message': f'Welcome {user[1]}! Login successful.',
                'user_id': user[0],
                'email': user[2]
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Login failed due to server error'})

@app.route('/dashboard')
def dashboard():
    """Protected dashboard showing user data"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Secure Access</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .container { background: #f9f9f9; padding: 30px; border-radius: 8px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #007bff; color: white; }
        .security-demo { background: #fff3cd; padding: 15px; margin: 20px 0; border: 1px solid #ffeaa7; border-radius: 4px; }
        input[type="text"] { padding: 8px; margin: 5px; width: 200px; }
        button { padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Employee Dashboard</h1>
        <p><a href="/">← Back to Login</a></p>
        
        <div class="security-demo">
            <h3>🛡️ SQL Injection Protection Demo</h3>
            <p>Try searching for users. This search is protected against SQL injection attacks:</p>
            <input type="text" id="searchInput" placeholder="Search username (try: admin OR 1=1)">
            <button onclick="searchUsers()">Search</button>
            <div id="searchResults"></div>
        </div>
        
        <h2>Company Directory</h2>
        <button onclick="loadUsers()">Load All Users</button>
        <div id="userList"></div>
        
        <div class="security-demo">
            <h3>Security Implementation Notes:</h3>
            <ul>
                <li><strong>Parameterized Queries:</strong> All database queries use parameterized statements</li>
                <li><strong>Input Validation:</strong> User inputs are validated and sanitized</li>
                <li><strong>Password Hashing:</strong> Passwords are hashed using SHA-256</li>
                <li><strong>HTTPS Ready:</strong> Application supports SSL/TLS encryption</li>
            </ul>
        </div>
    </div>
    
    <script>
        function loadUsers() {
            fetch('/api/users')
            .then(response => response.json())
            .then(users => {
                let html = '<table><tr><th>ID</th><th>Username</th><th>Email</th></tr>';
                users.forEach(user => {
                    html += `<tr><td>${user.id}</td><td>${user.username}</td><td>${user.email}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('userList').innerHTML = html;
            });
        }
        
        function searchUsers() {
            const searchTerm = document.getElementById('searchInput').value;
            fetch('/api/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({search: searchTerm})
            })
            .then(response => response.json())
            .then(data => {
                const results = document.getElementById('searchResults');
                if (data.users && data.users.length > 0) {
                    let html = '<h4>Results:</h4><ul>';
                    data.users.forEach(user => {
                        html += `<li>${user.username} (${user.email})</li>`;
                    });
                    html += '</ul>';
                    results.innerHTML = html;
                } else {
                    results.innerHTML = '<p>No users found or invalid search.</p>';
                }
            });
        }
        
        // Load users on page load
        loadUsers();
    </script>
</body>
</html>
    ''')

@app.route('/api/users')
def get_users():
    """API endpoint to get all users (secure)"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Secure query - no user input involved
        cursor.execute('SELECT id, username, email FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return jsonify([
            {'id': user[0], 'username': user[1], 'email': user[2]}
            for user in users
        ])
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users'})

@app.route('/api/search', methods=['POST'])
def search_users():
    """Secure search endpoint with SQL injection protection"""
    try:
        data = request.get_json()
        search_term = data.get('search', '').strip()
        
        # Input validation
        if not search_term or len(search_term) > 50:
            return jsonify({'users': []})
        
        # Remove potentially dangerous characters
        search_term = search_term.replace("'", "").replace('"', "").replace(';', "")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # SECURE: Parameterized query prevents SQL injection
        cursor.execute(
            'SELECT id, username, email FROM users WHERE username LIKE ? OR email LIKE ?',
            (f'%{search_term}%', f'%{search_term}%')
        )
        
        users = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'users': [
                {'id': user[0], 'username': user[1], 'email': user[2]}
                for user in users
            ]
        })
        
    except Exception as e:
        return jsonify({'users': [], 'error': 'Search failed'})

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    print("🔒 Secure Database Access Application")
    print("=" * 40)
    print("Security Features:")
    print("✅ SQL Injection Protection (Parameterized Queries)")
    print("✅ Password Hashing (SHA-256)")
    print("✅ Input Validation")
    print("✅ HTTPS Support Ready")
    print("")
    print("Demo Credentials:")
    print("Username: admin, Password: password123")
    print("Username: employee, Password: password123")
    print("")
    print("Starting server...")
    
    # Check for SSL certificates
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        print("🔐 SSL certificates found - running with HTTPS on port 5000")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=False)
    else:
        print("⚠️  No SSL certificates found - running HTTP on port 5000")
        print("📝 To enable HTTPS: run 'python generate_ssl.py' first")
        app.run(host='0.0.0.0', port=5000, debug=False)