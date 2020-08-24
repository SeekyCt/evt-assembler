# Evt Script Assembler
An assembler for Super Paper Mario text evt scripts into a C/C++ array (can support TTYD with minor edits)

## Usage
Enter the path to the text file containing your script when the program runs or with --infile / -i
Only official opcode names are supported (ie. not ttyd-asm's, although that can be changed with minor edits) and the unnoficial name end_script has been given to opcode 2
The format for each line is "instruction operand1, operand2, operand3, ... final operand" - splitting is done based on the spaces, commas are optional, and any extra whitespace is ignored (including indentation and blank lines)
A # can be used to comment out the rest of a line

## Credits
This is heavily based off of the research done by everyone involved in the creation of ttyd-asm
https://github.com/PistonMiner/ttyd-tools