/**
 * MSCS 535 Assignment 3 - Basic Implementation
 * Main class to demonstrate both security components
 */
public class Assignment3Basic {
    
    public static void main(String[] args) {
        System.out.println("MSCS 535 - Assignment 3 (Basic Version)");
        System.out.println("========================================\n");
        
        // Part 1: Application Layer Security
        System.out.println("PART 1: Application Layer Security Protection");
        System.out.println("---------------------------------------------");
        BasicApplicationSecurity.demo();
        
        System.out.println("\n" + "=".repeat(50) + "\n");
        
        // Part 2: One-Time Pad Encryption
        System.out.println("PART 2: One-Time Pad Encryption");
        System.out.println("--------------------------------");
        BasicOneTimePad.demo();
        
        System.out.println("\nAssignment Complete!");
    }
}