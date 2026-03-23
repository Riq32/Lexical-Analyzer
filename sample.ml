// MiniLang Sample Program
// Uses only: if, while, print | numbers | identifiers | strings
//            arithmetic (+,-,*,/) | relational (<,>,==) | assign (=) | separators
 
{
    // Variable assignments
    x = 10;
    y = 3;
    result = 0;
    name = "Alice";
 
    // Arithmetic operations
    result = x + y;
    result = x - y;
    result = x * y;
    result = x / y;
 
    // if statement with relational operator
    if (x > y) {
        print("x is greater");
    }
 
    if (x == 10) {
        print("x is ten");
    }
 
    // while loop
    counter = 0;
    while (counter < 5) {
        print(counter);
        counter = counter + 1;
    }
 
    // Nested if inside while
    i = 1;
    while (i < 4) {
        if (i == 2) {
            print("i is two");
        }
        i = i + 1;
    }
 
    print(name);
    print(result);
}
 