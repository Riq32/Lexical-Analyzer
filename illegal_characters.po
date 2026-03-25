// Test Case 1: Illegal / Unknown Characters
// Characters @, #, $, ^ are not part of MiniLang
 
{
    x = 10;
    y = x @ 5;      // @ is illegal
    z = 3 # 2;      // # is illegal
    name = $user;   // $ is illegal
    flag = x ^ 2;   // ^ is illegal
}