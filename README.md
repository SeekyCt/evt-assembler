# Evt Script Assembler
An assembler for Super Paper Mario text evt scripts (can support TTYD with minor edits)

## Assembling
Either run main.py and it will prompt you to enter the path, or use the command line arguments (recommended)

### --infile path, -i path
Path to the text file containing the evt script to be assembled

### --outfile path, -o path
Path to the file to store the result to (will print to console if not specified, not recommended)

### --symbol name, -s name
Sets the symbol name for the array created (ignored for binary format)

### --map path, -m path
Path to the symbol map to look up named symbol operands from

### --binary, -b
Makes the output plain binary (or hex if printing to console) instead of a C/C++ array

## Scripting

Only official instruction names are supported (ie. not ttyd-asm's, although that can be changed with minor edits) and the unnoficial name end_script has been given to opcode 2

The format for each line is "instruction operand1, operand2, operand3, ... final operand" - splitting is done based on the spaces, so commas are optional, and any extra whitespace is ignored (including indentation and blank lines)

A hash can be used to comment out the rest of a line

## Potential Update Plans
- TTYD support
- Pre-processor stuff (basic math expressions, name definitions)
- ttyd-asm instruction name support

## Credits
This is heavily based off of the research done by everyone involved in the creation of ttyd-asm
https://github.com/PistonMiner/ttyd-tools