# Securing an Online Payment System

Purpose: Provide concise pseudocode and guidance for protecting an online payment system from SQL Injection and Cross-Site Scripting (XSS).

## Contract 
- Inputs: user-supplied payment form fields (amount, card number, cardholder name, user id, optional description).
- Outputs: safe DB writes and safe HTML/API responses; errors returned for invalid/unsafe inputs.
- Success criteria: never concatenate untrusted input into SQL; never render unescaped user input into HTML without encoding/sanitization.

## Edge cases to consider 
- Empty or very large inputs.
- Unicode / UTF-8 encodings and mixed-direction characters.
- Stored XSS: user-submitted data later displayed to other users.
- DOM-based XSS: client-side template/DOM APIs used unsafely.
- Malformed numbers, rounding/precision for amounts.

---

## 1) SQL Injection 

Goal: Ensure database queries never treat untrusted user data as SQL. Use parameterized queries (prepared statements) or a safe ORM. Validate and normalize inputs (whitelists), apply least-privilege DB accounts, and avoid dynamic SQL.

Key points:
- Use prepared statements / parameterized queries.
- Whitelist and normalize expected formats (e.g., currency decimal, card digits pattern).
- Hash/salt sensitive data (never store raw card numbers unless PCI compliant; ideally tokenize via a payment processor).
- Use DB accounts with minimal permissions (INSERT/UPDATE for app user, no DDL).

Pseudocode (server-side request handler):

```
function handlePaymentRequest(request):
    // 1) Parse & normalize
    amount = parseDecimal(request.params.amount)
    if amount <= 0 or amount > MAX_PAYMENT: return error("invalid amount")

    user_id = parseInteger(request.auth.user_id)

    // 2) Whitelist & basic validation
    card_number = removeNonDigits(request.params.card_number)
    if not matchesRegex(card_number, "^[0-9]{13,19}$"): return error("invalid card")

    // 3) Tokenize or hash sensitive data (prefer external tokenization)
    // If using a payment gateway: send card to gateway and receive token
    card_token = paymentGateway.tokenize(card_number, request.params.expiry)
    if card_token is null: return error("payment tokenization failed")

    // 4) Use parameterized query (never string-concatenate)
    query = "INSERT INTO payments (user_id, amount_cents, card_token, created_at) VALUES (?, ?, ?, ?)"
    stmt = db.prepare(query)
    stmt.bind(1, user_id)
    stmt.bind(2, toCents(amount))
    stmt.bind(3, card_token)
    stmt.bind(4, now())
    stmt.execute()

    return success("payment recorded")
```

Notes:
- If you must call a stored procedure, call it with parameters, not by concatenating SQL strings.
- ORM usage example: Payment.create({ userId: user_id, amountCents: toCents(amount), cardToken: card_token }) — most ORMs parameterize internally.
- Never log full card numbers.

Quick safe validation rules (whitelist examples):
- amount: decimal with max two fractional places, range check.
- card_number: digits only, length 13–19, pass Luhn check if applicable.

---

## 2) Cross-Site Scripting (XSS)

Goal: Prevent injection of executable script into pages viewed by other users or into the client DOM. Always escape/encode untrusted data when inserting into HTML, use strict Content Security Policy (CSP), and sanitize only when you intentionally allow limited HTML.

Key points:
- Encode/escape on output (context-sensitive: HTML text, attribute, JS, URL, CSS).
- Sanitize only when allowing HTML — use a vetted HTML sanitizer library with an allowlist of tags and attributes.
- Use HTTP headers: Strict CSP, X-Content-Type-Options: nosniff, X-Frame-Options or frame-ancestors, Referrer-Policy, and set cookies with HttpOnly and Secure.
- Avoid using innerHTML / document.write on client-side with user data. Prefer textContent or safe templating libraries that auto-escape.

Pseudocode (server-side rendering and storage):

```
// When accepting a free-text field (e.g., description): store the raw text, but do not allow raw HTML without sanitization.
function acceptDescription(request):
    desc = request.params.description or ""
    // Normalize (trim, limit length)
    desc = truncate(trim(desc), 1000)
    // Option A (safe): store raw text and escape on output
    db.save("insert into comments (user_id, text) values (?, ?)", [user_id, desc])

    // Option B (if HTML is allowed): sanitize then store sanitized HTML
    safeHtml = sanitizeHTML(desc, allowTags=["b","i","ul","li","p","a"], allowAttrs={"a":["href"]})
    db.save("insert into comments (user_id, html) values (?, ?)", [user_id, safeHtml])
```

Pseudocode (rendering to HTML template):

```
function renderCommentRow(comment):
    // For plain text fields: escape HTML entities
    out("<div class='comment'>")
    out("<div class='author'>" + escapeHtml(comment.author) + "</div>")
    out("<div class='body'>" + escapeHtml(comment.text) + "</div>")
    // If stored as sanitized HTML (Option B), still ensure it was sanitized by a safe library
    out("</div>")
```

Client-side safe DOM insertion (avoid innerHTML):

```
function addCommentToPage(comment):
    el = document.createElement('div')
    el.className = 'comment'
    author = document.createElement('div')
    author.textContent = comment.author   // textContent auto-escapes
    body = document.createElement('div')
    body.textContent = comment.text       // use textContent not innerHTML
    el.appendChild(author)
    el.appendChild(body)
    document.getElementById('comments').appendChild(el)
```

Security headers (server):

```
setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self';")
setHeader('X-Content-Type-Options', 'nosniff')
setHeader('Referrer-Policy', 'no-referrer')
setCookie('session', sessionId, { HttpOnly: true, Secure: true, SameSite: 'Lax' })
```

Notes:
- CSP should be tuned for your application and tested incrementally; start strict and add safe exceptions when needed.
- Use nonces or hashes for inline scripts if you must keep trusted inline scripts.

## 3. References

1. Kohnfelder, L. (2021). *Designing Secure Software*. Random House Publishing Services. https://reader2.yuzu.com/books/9781718501935

2. Richardson, T., & Thies, C. N. (2012). *Secure Software Design*. Jones & Bartlett Learning. https://reader2.yuzu.com/books/9781284102680

