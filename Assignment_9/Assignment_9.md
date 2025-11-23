# AMSCS535 - Assignment_9

## Question 1: Why is it beneficial to develop a software system in a language that is well known to the development team? 

Developing software in a language familiar to the development team provides important security advantages:

1. **Fewer Security Vulnerabilities**: Developers who know a language well understand its common security pitfalls and how to avoid them. Inexperience can lead to flaws like buffer overflows or injection vulnerabilities.

2. **Better Code Reviews**: Team members can quickly spot security issues during reviews when they're familiar with the language's patterns and best practices.

3. **Proper Use of Security Features**: Experienced developers know how to use built-in security mechanisms effectively, rather than accidentally bypassing them or creating insecure workarounds.

4. **Faster Bug Detection**: Familiarity allows developers to recognize suspicious code patterns quickly and fix issues before they become security problems

---

## Question 2: Provide and explain an example code of how Java deals with objects and variables passed by value and objects and variables passed by reference. 

### Key Concept

Java is **pass-by-value** for all variables:
- **Primitives**: The actual value is copied
- **Objects**: The reference (memory address) is copied, not the object itself

### Example Code

```java
public class PassByValueDemo {
    
    public static void main(String[] args) {
        // Example 1: Primitive Type
        int number = 10;
        System.out.println("Before: " + number);
        modifyPrimitive(number);
        System.out.println("After: " + number);
        // Output: Still 10 (unchanged)
        
        // Example 2: Object Reference
        Person person = new Person("Alice");
        System.out.println("Before: " + person.getName());
        modifyObject(person);
        System.out.println("After: " + person.getName());
        // Output: Changed to "Bob"
    }
    
    public static void modifyPrimitive(int value) {
        value = 999;  // Only changes the local copy
    }
    
    public static void modifyObject(Person p) {
        p.setName("Bob");  // Modifies the actual object
    }
}

class Person {
    private String name;
    
    public Person(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
}
```

### Explanation

**Primitive Example**: When `number` is passed to `modifyPrimitive()`, Java copies the value 10. Changing the copy to 999 doesn't affect the original variable.

**Object Example**: When `person` is passed to `modifyObject()`, Java copies the reference (memory address). Both the original and the copy point to the same `Person` object in memory, so changes to the object's properties are visible outside the method.

**Security Note**: This behavior can create security risks. Even though Java is pass-by-value, mutable objects can still be modified through copied references, potentially exposing sensitive data

---

## References

Kohnfelder, L. (2021). *Designing Secure Software*. Random House Publishing Services. https://reader2.yuzu.com/books/9781718501935

Richardson, T., & Thies, C. N. (2012). *Secure Software Design*. Jones & Bartlett Learning. https://reader2.yuzu.com/books/9781284102680
