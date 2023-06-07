# CSE112-Assignment

Code for the assembler assignment of CSE112 - Computer Organisation

## Team Members

- Sahil Gupta, 2022430 (github username- sahilguptasg2017)
- Rachit Arora, 2022384 (github username- rcht)
- Tanmay Singhal, 2022535 (github username- pecpo)
- Saksham Kapoor, 2022431 (github username- SakshamKapoor12) 

## Evaluation

Evaluation is in the standard format. The source code for the assembler is in the file `Simple-Assembler/main.py` and `SimpleSimulator/simulator.py` for the simulator.

To test, change your working directory to `automatedTesting` and run the evaluator with `./run`, or `./run --no-sim` if only the assembler is to be evaluated.

## Code Documentation

### Assembler and Simulator

The assembler and simulator have been made in Python 3.

At the top of the code are definitions for global variables like register to binary conversion which will be used throughout the program.

Then there are utility functions like `isvalid` in the assembler and `isValidImmediate` in the simulator which help do certain tasks in the program.

In the main loop of both, different instruction types are handled separately. 

Input and Output are always `stdin` and `stdout` respectively.

### Floating point support

In commit `2557b5`, support for the floating point instructions `addf`, `subf` and `movf` was added to the assembler and simulator.

### Bonus- Extra instructions

We added the `nop` instruction as the bonus part.

It has no argument, and it simply does nothing.

Its opcode is `10011`.
