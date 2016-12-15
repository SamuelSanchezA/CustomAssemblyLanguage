# CustomAssemblyLanguage
The following repository contains the code which takes some rudimentary text in a text file and uses it as a language to execute some form of code. The program utilizes Python.



How to create a variable:
(variables cannot contain anything but upper and lowercase letters)
(variables must be initialized with literals)

varA , 0

How to create an array: 
(must have a literal in the brackets)
(brackets contain the spaces allocated for the array)
(first is the variable that contains the starting address of the array)

aryA , [10]

Array access:

variable assignment: 
(after a variable is initialized you can assign it to another variable, an array element, or a literal)
varA , 12
varA , [araA]

How to skip the next line: 

(skip if varA is equal to varB)
SKIPE varA, varB

(skip if varA > varB)
SKIPG varA, varB

(skip if varA < varB)
SKIPL varA, varB

(all can also be used with literals instead of variables)

Saves line so you can jump back to it:
lineName:
 
how to jump back to a line:

JUMP, lineName

how to add one variable to another:
(result is stored in varA)
ADD varA, varB

how to subtract one variable from another:
(result is stored in varA)
SUBT varA, varB

how to do input:
(varA has to be initialized, and input is stored in varA)
varA, INPUT

how to do output:
(prints out what is stored in varA)
PRINT, varA
