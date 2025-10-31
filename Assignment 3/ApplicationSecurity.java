/**
 * Basic Application Layer Security Protection (OSI Layer 7)
 * Simple implementation of common security measures
 */
public class BasicApplicationSecurity {
    
    /**
     * Sanitize input to prevent XSS attacks
     */
    public static String sanitizeInput(String input) {
        if (input == null) return "";
        
        return input.replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\"", "&quot;")
                   .replace("'", "&#x27;")
                   .replace("&", "&amp;");
    }
    
    /**
     * Check for SQL injection patterns
     */
    public static boolean isSQLInjection(String input) {
        if (input == null) return false;
        
        String[] badPatterns = {"'", "\"", ";", "--", "DROP", "DELETE", "INSERT", "UPDATE"};
        String upperInput = input.toUpperCase();
        
        for (String pattern : badPatterns) {
            if (upperInput.contains(pattern)) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Simple password hashing
     */
    public static String hashPassword(String password) {
        return Integer.toString(password.hashCode());
    }
    
    /**
     * Validate input length
     */
    public static boolean isValidLength(String input, int maxLength) {
        return input != null && input.length() <= maxLength;
    }
    
    /**
     * Demo method
     */
    public static void demo() {
        System.out.println("=== Basic Application Layer Security Demo ===\n");
        
        // XSS Prevention
        String xssInput = "<script>alert('hack')</script>";
        System.out.println("1. XSS Prevention:");
        System.out.println("Input: " + xssInput);
        System.out.println("Sanitized: " + sanitizeInput(xssInput));
        System.out.println();
        
        // SQL Injection Detection
        String sqlInput = "'; DROP TABLE users; --";
        System.out.println("2. SQL Injection Detection:");
        System.out.println("Input: " + sqlInput);
        System.out.println("Is SQL Injection: " + isSQLInjection(sqlInput));
        System.out.println();
        
        // Password Hashing
        String password = "mypassword123";
        System.out.println("3. Password Hashing:");
        System.out.println("Password: " + password);
        System.out.println("Hashed: " + hashPassword(password));
        System.out.println();
        
        // Input Validation
        String longInput = "This is a very long input string that exceeds normal limits";
        System.out.println("4. Input Length Validation:");
        System.out.println("Input: " + longInput);
        System.out.println("Valid (max 20): " + isValidLength(longInput, 20));
        System.out.println("Valid (max 100): " + isValidLength(longInput, 100));
    }
    
    public static void main(String[] args) {
        demo();
    }
}