import re

global variable_holder 
global registers
global text_array
global memory_addresses 
global regexTerms

text_array = []
variable_holder = {}
regexTerms = []
regexTerms.append(r"^([a-zA-Z]+)( |\t)*,( |\t)*( |\t)*([a-zA-Z]+|-?[0-9]+)$") #Variable Declaration
regexTerms.append(r"^([a-zA-Z]+)( |\t)*([a-zA-Z]+)( |\t)*,( |\t)*(([a-zA-Z]+)|-?[0-9]+)$")
regexTerms.append(r"^( )*$")
regexTerms.append(r"^([a-zA-Z]+)( |\t)*(\:)( |\t)*$")
regexTerms.append(r"^( |\t)*([a-zA-Z]+)( |\t)*$")

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
        if re.match(regexTerms[0], f):
            #print f
            text_array[text_array.index(f)] = re.split(",", f) # Strings split at commas (spaces included in strings however)
            text_array[lineNumber - 1][0] = text_array[lineNumber - 1][0].strip()
            text_array[lineNumber - 1][1] = text_array[lineNumber - 1][1].strip()
        elif re.match(regexTerms[1], f):
            #print "In second: ", f
            index = text_array.index(f)
            text_array[index] = re.split(",", f)
            print text_array[index], "Before"
            text_array[index][0] = text_array[index][0].strip()
            text_array[index][1] = text_array[index][1].strip()
            temp = text_array[index][0].split(" ")
            text_array[index].remove(text_array[index][0])
            text_array[index].insert(0,temp[0])
            text_array[index].insert(1,temp[-1])
            print text_array[index], "After"
        elif re.match(regexTerms[2], f):
            text_array[text_array.index(f)] = ""
        elif re.match(regexTerms[3], f):
            temp = "".join(f.split())    
            text_array[text_array.index(f)] = [temp[:len(temp) -1],temp[-1]]
        elif re.match(regexTerms[4], f):
            text_array[text_array.index(f)] = text_array[text_array.index(f)].strip().upper()
        else:
            print "Syntax Error on line", lineNumber, ": ", f
            print "Terminating Program"
            exit(1)
        #print lineNumber + text_array[lineNumber]
        lineNumber = lineNumber + 1
        

def execute():
	lineNumber = 1
	while lineNumber - 1 < len(text_array):
	    print "lineNumber", lineNumber
	    instruction = text_array[lineNumber -1]
	    
	    print "Instruction:", instruction

	    if len(instruction) == 0:
	            lineNumber = lineNumber + 1
	            continue

	    if len(instruction) == 2: # Variable/register declaration
	        key = instruction[0].strip()
	        key2 = instruction[1].strip()
	        if key in registers:
	            if key2 in registers:
	                registers[key] = registers[key2]
	            elif key2 in variable_holder:
	                registers[key] = variable_holder[key2]
	            else:
	                registers[key] = isValidNumber(key2, lineNumber)
	        elif key in variable_holder:
	            if key2 in registers:
	                variable_holder[key] = registers[key2]
	            elif key2 in variable_holder:
	                variable_holder[key] = variable_holder[key2]
	            elif key2 == "INPUT":
	                variable_holder[key] = int(raw_input("Enter Input: "))
	            else:
	                variable_holder[key] = isValidNumber(key2, lineNumber)
	        elif key2 == ':':
	            variable_holder[key] = lineNumber
	        elif key == 'JUMP':
	            lineNumber = jump(instruction)
	            #continue
	        elif key == "PRINT":
	            if key2 in variable_holder:
	                print "Output: " + str(variable_holder[key2])
	            else:
	                print "Output: " + str(isValidNumber(key2,lineNumber))
	        else:
	            print "You little shit!"
	            variable_holder[key] = isValidNumber(key2, lineNumber)

	    # Checks for instruction with length of 3
	    elif len(instruction) == 3:

	        opCode = instruction[0] #the read opCode
	        print opCode
	        if opCode == "ADD":
	            add(instruction)
	        elif opCode == "SUBT":
	            subt(instruction)
	        elif opCode == "MULT":
	            mult(instruction)
	        elif opCode == "DIV":
	            div(instruction)
	        elif opCode == "ARRADD":
	            addToArray(instruction)
	        elif opCode == "ARRAT":
	            loadArrayAt(instruction)
	        elif opCode == "ARRFIND":
	            findVal(instruction)

	        elif (opCode == "SKIPE" or opCode == "SKIPL" or opCode == "SKIPG"):
	            print "Got a skip"
	            lineNumber = skip(instruction,lineNumber)
	            #continue
	        else:
	            print "Wrong operation code!\n"
	            print instruction
	    
	    elif len(instruction) == 1:
	        if instruction[0] == "HALT":
	            print "HALT"
	            break
	    print instruction
	    lineNumber += 1


def add(instruction):
    print instruction
    left_num = 0
    right_num = 0
    print variable_holder
    left_num = int(variable_holder[instruction[1]])
    right_num = int(instruction[2])

    variable_holder[instruction[1]] += right_num
    #print variable_holder[instruction[1]]


def subt(instruction):
    left_num = 0
    right_num = 0
    
    left_num = int(variable_holder[instruction[1]])
    right_num = int(instruction[2])

    variable_holder[instruction[1]] -= right_num

    #print variable_holder[instruction[1]]

def mult(instruction):
    left_num = 0
    right_num = 0
    
    left_num = int(variable_holder[instruction[1]])
    right_num = int(instruction[2])

    variable_holder[instruction[1]] *= right_num

    print variable_holder[instruction[1]]

def div(instruction, lineNum):
    left_num = 0
    right_num = 0
    
    left_num = int(variable_holder[instruction[1]])
    right_num = int(instruction[2])

    try: 
    	right_num != 0
        variable_holder[instruction[1]] /= right_num
        #print variable_holder[instruction[1]]
    except: 
        print "Error on Line", lineNum, ": Cannot divide by 0"
        exit(1)

def jump(instruction):
    print(instruction)
    if instruction[1] in variable_holder:
        return variable_holder[instruction[1]]
    elif instruction[1] in registers:
        return variable_holder[instruction[1]]
    else:
        print("ERROR: " + instruction[2] + " was not declared.")

def skip(instruction, lineNum):
    if instruction[1] in variable_holder:
        left = variable_holder[instruction[1]]
    else:
        left = isValidNumber(instruction[1],lineNum)

    if instruction[2] in variable_holder:
        right = variable_holder[instruction[2]]
    else:
        right = isValidNumber(instruction[2],lineNum)


    if(instruction[0] == "SKIPE"):
        print "Made SKIPE"
        if(left == right):
            print left == right
            
            i = lineNum
            print i
            while text_array[i] == "":
                i = i + 1
                print i
            return i+1
    elif(instruction[0] == "SKIPG"):
        if(left > right):
            print left == right
            
            i = lineNum
            print i
            while text_array[i] == "":
                i = i + 1
                print i
            return i+1
    elif(instruction[0] == "SKIPL"):
        if(left < right):
            print left == right
            
            i = lineNum
            print i
            while text_array[i] == "":
                i = i + 1
                print i
            return i+1
    
    

    return lineNum


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
execute()
print variable_holder['ass']
