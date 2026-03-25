// Test Case 2: Unterminated String Literal
// A string that is never closed with a matching "
 
{
    msg = "Hello World;    // missing closing quote — scanner reads past this line
    name = "Alice";        // valid string
    x = 42;
}
 