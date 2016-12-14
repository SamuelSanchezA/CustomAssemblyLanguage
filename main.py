import re

global variable_holder 
global registers
global text_array
global memory_addresses 
global regexTerms

text_array = []
variable_holder = {}
regexTerms = []
regexTerms.append(r"^([a-zA-Z]+)( |\t)*,( |\t)*(\d+)( |\t)*-?[0-9]+$") #Variable Declaration
regexTerms.append(r"^([a-zA-Z]+)( |\t)*([a-zA-Z]+)( |\t)*,( |\t)*(([a-zA-Z]+)|-?[0-9]+)$")
regexTerms.append(r"^( )*$")
regexTerms.append(r"^([a-zA-Z]+)( |\t)*(\:)( |\t)*$")

registers = {"R1": 0,"R2":0, "R3":0, "R4":0,"R5":0,"R6":0,"R7":0,"R8":0, "R9":0, "R10":0,
         "R11": 0, "R12":0, "R13":0, "R14":0,"R15":0,"R16":0,"R17":0,"R18":0, "R19":0, "R20":0,
         "R21": 0, "R22":0, "R23":0, "R24":0,"R25":0, "R26":0,"R27":0,"R28":0, "R29":0, "R30":0,
         "R31": 1, "R32":0, "R33":0, "R34":0,"R35":0, "R36":0,"R37":0,"R38":0, "R39":0, "R40":0,
         "R41": 1, "R42":0, "R43":0, "R44":0,"R45":0, "R46":0,"R47":0,"R48":0, "R49":0, "R50":0,
         "R51": 1, "R52":0, "R53":0, "R54":0,"R55":0, "R56":0,"R57":0,"R58":0, "R59":0, "R60":0,
         "R61": 1, "R62":0, "R63":0, "R64":0}

def readLine():
    try:
        textFile = open("Benchmark2.txt", 'r')
        for line in textFile: # This for loop will place all lines into a list for syntax check
            line = line.strip()
            text_array.append(line)
    except:
        print ("File does not exist")
        exit(1)

def verifySyntax():
    lineNumber = 1
    for f in text_array:
        print f
        if re.match(regexTerms[0], f):
            text_array[text_array.index(f)] = re.split(",", f) # Strings split at commas (spaces included in strings however)
        elif re.match(regexTerms[1], f):
            text_array[text_array.index(f)] = re.split(",", f)
        elif re.match(regexTerms[2], f):
            text_array[text_array.index(f)] = ""
        elif re.match(regexTerms[3], f):
            temp = "".join(f.split())
            
            text_array[text_array.index(f)] = [temp[:len(temp) -1],temp[-1]]
        else:
            print "Syntax Error on line", lineNumber, ": ", f
            print "Terminating Program"
            exit(1)
        lineNumber += 1
"""
def execute():
    lineNumber = 1
    for instruction in text_array:
        if len(instruction) == 2: # Variable/register declaration
            key = instruction[0].split()
            key2 = instruction[0].split()
            if key in registers:
                if key2 in registers:
                    registers[key] = registers[key2]
                elif key2 in variable_holder:
                    registers[key] = variable_holder[key2]
                else
                    registers[key] = isValidNumber(key2, lineNumber)
            elif key in variable_holder:
                if key2 in registers:
                    variable_holder[key] = registers[key2]
                elif key2 in variable_holder:
                    variable_holder[key] = variable_holder[key2]
                else
                    variable_holder[key] = isValidNumber(key2, lineNumber)
            else:
                variable_holder[key] = isValidNumber(key2, lineNumber)
        
        elif len(instruction) == 1:
            if instruction[0] == "HALT":
                break

        lineNumber += 1
"""
def isValidNumber(var, lineNum):
    try:
        var = int(var)
        return var
    except:
        print "Error on line", lineNum, ": ", var, " is neither a variable, register, nor an integer"
        print "Terminating Program"
        exit(1)

memory_addresses = [0 for i in range(10000)] # Memory addresses for array purposes

readLine()
verifySyntax() # Checks for syntax errors
print text_array