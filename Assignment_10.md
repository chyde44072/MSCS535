# MSCS535 - Assignment_10

## How to Utilize Static Analysis Results

Static analysis examines source code without executing it to find security vulnerabilities and coding errors. You should use static analysis results by:

1. **Prioritizing critical security issues first** (hard-coded credentials, SQL injection, buffer overflows)
2. **Fixing vulnerabilities systematically** rather than ignoring findings
3. **Re-scanning code after fixes** to verify the issues are resolved
4. **Training developers** on common security mistakes found

---

## Security Issues Found in Original Code

### Original Server Code Problems:

**Problem 1: Hard-coded Password**
```java
String keystorePassword = "password";  // INSECURE!
```
**Risk:** Anyone with source code access gets the password.

**Problem 2: Generic Exception Handling**
```java
catch (Exception e) {
    e.printStackTrace();  // INSECURE!
}
```
**Risk:** Prints sensitive system details that attackers could use.

**Problem 3: Weak TLS Configuration**
```java
SSLContext.getInstance("TLS");  // INSECURE!
```
**Risk:** May allow old, vulnerable TLS versions.

**Problem 4: No Resource Cleanup**
```java
in.close();
out.close();  // INSECURE - resources leak if exception occurs!
```
**Risk:** System can run out of resources and crash.

---

## Improved Secure Code

### Secure Server (Fixed Version)

```java
import javax.net.ssl.*;
import java.io.*;
import java.security.KeyStore;

public class SecureServer {
    public static void main(String[] args) {
        // FIX 1: Use environment variables for passwords
        String keystoreFile = System.getenv("KEYSTORE_PATH");
        String keystorePassword = System.getenv("KEYSTORE_PASSWORD");

        try {
            KeyStore keyStore = KeyStore.getInstance("JKS");
            try (FileInputStream fis = new FileInputStream(keystoreFile)) {
                keyStore.load(fis, keystorePassword.toCharArray());
            }

            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            kmf.init(keyStore, keystorePassword.toCharArray());

            // FIX 2: Use specific TLS version
            SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
            sslContext.init(kmf.getKeyManagers(), null, null);

            SSLServerSocketFactory factory = sslContext.getServerSocketFactory();
            SSLServerSocket serverSocket = (SSLServerSocket) factory.createServerSocket(8443);

            System.out.println("Secure server started");

            // FIX 3: Use try-with-resources for automatic cleanup
            try (SSLSocket socket = (SSLSocket) serverSocket.accept();
                 BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                 PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

                String message = in.readLine();
                
                // FIX 4: Validate input
                if (message != null && message.length() <= 1024) {
                    out.println("Hello, client!");
                }
            }

        // FIX 5: Specific exception handling without stack traces
        } catch (FileNotFoundException e) {
            System.err.println("Keystore file not found");
        } catch (IOException e) {
            System.err.println("IO error occurred");
        } catch (Exception e) {
            System.err.println("Server error occurred");
        }
    }
}
```

### Secure Client (Fixed Version)

```java
import javax.net.ssl.*;
import java.io.*;
import java.security.KeyStore;

public class SecureClient {
    public static void main(String[] args) {
        // FIX 1: Use environment variables
        String truststoreFile = System.getenv("TRUSTSTORE_PATH");
        String truststorePassword = System.getenv("TRUSTSTORE_PASSWORD");

        try {
            KeyStore trustStore = KeyStore.getInstance("JKS");
            try (FileInputStream fis = new FileInputStream(truststoreFile)) {
                trustStore.load(fis, truststorePassword.toCharArray());
            }

            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            tmf.init(trustStore);

            // FIX 2: Specific TLS version
            SSLContext sslContext = SSLContext.getInstance("TLSv1.3");
            sslContext.init(null, tmf.getTrustManagers(), null);

            SSLSocketFactory factory = sslContext.getSocketFactory();

            // FIX 3: Try-with-resources
            try (SSLSocket socket = (SSLSocket) factory.createSocket("localhost", 8443);
                 BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                 PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

                out.println("Hello, server!");
                String response = in.readLine();
                System.out.println("Server says: " + response);
            }

        // FIX 4: Specific exception handling
        } catch (FileNotFoundException e) {
            System.err.println("Truststore file not found");
        } catch (IOException e) {
            System.err.println("Connection error");
        } catch (Exception e) {
            System.err.println("Client error occurred");
        }
    }
}
```

---

## Why These Fixes Make the Code Secure

**1. Environment Variables for Passwords**
- Passwords never stored in source code or version control
- Separating secrets from code is fundamental security practice

**2. Specific TLS Version (TLSv1.3)**
- Blocks downgrade attacks to vulnerable older protocols like SSLv3 or TLS 1.0
- Use latest secure protocols

**3. Try-with-Resources**
- Automatically closes connections even if errors occur
- Prevents resource exhaustion attacks (denial of service)

**4. Input Validation**
- Checks message size to prevent buffer overflow attacks
- Always validate input before processing

**5. No Stack Traces in Production**
- Generic error messages don't reveal system internals to attackers
- Prevents information disclosure vulnerability

---

## Summary

Static analysis helps find security problems before code runs. The key is to:
- **Fix high-priority issues** like hard-coded passwords and weak encryption
- **Use secure coding practices** like environment variables and try-with-resources
- **Validate all inputs** to prevent attacks
- **Handle errors securely** without revealing system details

---

## References

Kohnfelder, L. (2021). *Designing Secure Software*. Random House Publishing Services. https://reader2.yuzu.com/books/9781718501935

Richardson, T., & Thies, C. N. (2012). *Secure Software Design*. Jones & Bartlett Learning. https://reader2.yuzu.com/books/9781284102680
