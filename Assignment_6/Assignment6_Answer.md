# Assignment 6 - Generic Classes and Vehicle Inheritance

## Question 1: Why are generic classes both useful and dangerous in programming?

### Useful Aspects of Generic Classes

Generic classes provide several significant advantages in modern programming:

#### 1. **Type Safety at Compile Time**
- Generics catch type-related errors during compilation rather than at runtime
- Prevents `ClassCastException` errors that could occur with raw types
- Example: `List<String>` ensures only String objects can be added

#### 2. **Code Reusability**
- Write once, use with multiple types
- Reduces code duplication and maintenance overhead
- A single generic class can work with any reference type

#### 3. **Elimination of Type Casting**
- No need for explicit casting when retrieving objects from collections
- Cleaner, more readable code
- Compiler automatically handles type conversions

#### 4. **Performance Benefits**
- Eliminates the overhead of boxing/unboxing in some cases
- Reduces memory usage by avoiding unnecessary object creation

### Dangerous Aspects of Generic Classes

Despite their benefits, generics can introduce certain risks:

#### 1. **Type Erasure at Runtime**
- Generic type information is removed during compilation
- Can lead to unexpected behavior when using reflection
- Makes debugging more difficult in some scenarios

#### 2. **Complex Syntax**
- Wildcard types (`? extends`, `? super`) can be confusing
- Nested generics can become difficult to read and understand
- Learning curve for developers new to generics

#### 3. **Runtime Type Checking Limitations**
- Cannot perform `instanceof` checks with parameterized types
- Type safety is only guaranteed at compile time
- Potential for heap pollution in certain scenarios

#### 4. **Compatibility Issues**
- Raw types and generic types can be mixed, leading to warnings
- Legacy code integration can be challenging
- Version compatibility concerns across different Java versions

#### References
- Kohnfelder, L. (2021). Designing Secure Software. Random House Publishing Services. https://reader2.yuzu.com/books/9781718501935
- Richardson, T., & Thies, C. N. (2012). Secure Software Design. Jones & Bartlett Learning. https://reader2.yuzu.com/books/9781284102680