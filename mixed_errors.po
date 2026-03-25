// Test Case 3: Mixed Valid and Invalid — Scanner Recovery
// Scanner should continue past errors and tokenize valid tokens
 
{
    result = 100;
    result = result + 20~5;   // ~ is illegal
    check = x & y;            // & alone is not a MiniLang operator
    pi = 3;
    out = "done";
    print(out);
}
 