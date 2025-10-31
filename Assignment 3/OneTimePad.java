/**
 * Basic One-Time Pad Encryption
 * Simple implementation for encrypting "MY NAME IS UNKNOWN"
 */
public class BasicOneTimePad {
    
    /**
     * Encrypt text using XOR with a key
     */
    public static String encrypt(String text, String key) {
        StringBuilder result = new StringBuilder();
        
        for (int i = 0; i < text.length(); i++) {
            char textChar = text.charAt(i);
            char keyChar = key.charAt(i % key.length());
            char encrypted = (char) (textChar ^ keyChar);
            result.append(encrypted);
        }
        
        return result.toString();
    }
    
    /**
     * Decrypt text using XOR with the same key
     */
    public static String decrypt(String encryptedText, String key) {
        // XOR is its own inverse, so decryption is the same as encryption
        return encrypt(encryptedText, key);
    }
    
    /**
     * Convert string to hex for display
     */
    public static String toHex(String text) {
        StringBuilder hex = new StringBuilder();
        for (char c : text.toCharArray()) {
            hex.append(String.format("%02X ", (int) c));
        }
        return hex.toString().trim();
    }
    
    /**
     * Demo method
     */
    public static void demo() {
        System.out.println("=== Basic One-Time Pad Encryption Demo ===\n");
        
        String message = "MY NAME IS UNKNOWN";
        String key = "SECRETKEYFORENCRYP"; // Same length as message
        
        System.out.println("Original Message: " + message);
        System.out.println("Key:              " + key);
        System.out.println();
        
        // Encrypt
        String encrypted = encrypt(message, key);
        System.out.println("Encrypted (text): " + encrypted);
        System.out.println("Encrypted (hex):  " + toHex(encrypted));
        System.out.println();
        
        // Decrypt
        String decrypted = decrypt(encrypted, key);
        System.out.println("Decrypted: " + decrypted);
        System.out.println("Success:   " + message.equals(decrypted));
        System.out.println();
        
        // Show XOR operation for first few characters
        System.out.println("XOR Details (first 5 characters):");
        for (int i = 0; i < 5; i++) {
            char m = message.charAt(i);
            char k = key.charAt(i);
            char e = (char) (m ^ k);
            System.out.printf("'%c' XOR '%c' = '%c' (%d XOR %d = %d)\n", 
                             m, k, e, (int)m, (int)k, (int)e);
        }
    }
    
    public static void main(String[] args) {
        demo();
    }
}