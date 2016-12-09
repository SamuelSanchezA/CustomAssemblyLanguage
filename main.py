import re

global variable_holder 
global registers
global text_array
global memory_addresses 
global regexTerms

text_array = []
variable_holder = {}
regexTerms = []
regexTerms.append(r"( |\t)*([a-zA-Z]+)( |\t)*,( |\t)*(\d+)( |\t)*")
regexTerms.append(r"( |\t)*([a-zA-Z]+)( |\t)*([a-zA-Z]+)( |\t)*,( |\t)*(([a-zA-Z]+)|(\d+))( |\t)*")

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
        for line in textFile:
            line = line.strip()
            #lineArray = line.split(' ')
            text_array.append(line)
            print line
        #execute()
    except:
        print ("File does not exist")
        exit(1)
def matches():
    lineNumber = 1
    for f in text_array:
        if re.match(regexTerms[0], f):
            print f, " Matches first"
        elif re.match(regexTerms[1], f):
            print f, " Matches second"
        else:
            print "Syntax Error on line", lineNumber, ": ", f
            exit(1)
        lineNumber += 1
"""
def execute():
    print text_array
    for instruction in text_array:
        if instruction[0] == "ADD":
            key = instruction[1]
            if key in registers:
                registers[key] += instruction[2]
            elif key in variable_holder:
                variable_holder[key] += instruction[2]
            else:
                print Key, " is not a register nor variable"
                exit(1)
        elif instruction[0] == "HALT":
            break
        else: # Catches variable naming and initialization
            if isValidNumber(instruction[1]):
                variable_holder[instruction[0]] = int(instruction[1])
                text_array.remove(instruction)
            else:
                print "Are you stupid? Can\'t convert to int dummy."

def isValidNumber(var):
    try:
        int(var)
        return True
    except:
        return False
        
memory_addresses = [0 for i in range(10000)] # Memory addresses for array purposes

"""
readLine()
matches()
