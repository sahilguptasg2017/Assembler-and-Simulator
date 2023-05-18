# CSE112-Assignment

Code for the assembler assignment of CSE112 - Computer Organisation

## Team Members

- Sahil Gupta, 2022430 (github username- sahilguptasg2017)
- Rachit Arora, 2022384 (github username- rcht)
- Tanmay Singhal, 2022535 (github username- pecpo)
- Saksham Kapoor, 2022431 (github username- SakshamKapoor12) 

## Evaluation

Evaluation is in the standard format. The source code for the assembler is in the file `Simple-Assembler/main.py`.

To test, change your working directory to `automatedTesting` and run the evaluator with `./run --no-sim`.

## Code Documentation

The assembler has been made in Python 3.

At the top of the code are definitions for global variables like register to binary conversion which will be used throughout the program.

The `isvalid` function checks whether a string is a valid memory location or not.

Then there are 5 functions `ins_typeA` to `ins_typeE` which handle spefic instructions.

Rest of the code is either handling non-trivial errors, parsing, etc.

Input and Output are always `stdin` and `stdout` respectively.
