import re

global variable_holder 
global registers
global text_array
global memory_addresses 
global next_memory_address
global regexTerms


text_array = []
variable_holder = {}
next_memory_address = 0
regexTerms = []
regexTerms.append(r"^([a-zA-Z]+)( |\t)*,( |\t)*( |\t)*([a-zA-Z]+|-?[0-9]+)$") #Variable Declaration
regexTerms.append(r"^([a-zA-Z]+)( |\t)*([a-zA-Z]+)( |\t)*,( |\t)*(([a-zA-Z]+)|-?[0-9]+)$") # 3 Word op code
regexTerms.append(r"^( )*$") # Space
regexTerms.append(r"^([a-zA-Z]+)( |\t)*(\:)( |\t)*$") # Function
regexTerms.append(r"^( |\t)*([a-zA-Z]+)( |\t)*$") # Single word op
regexTerms.append(r"^( |\t)*([a-zA-Z]+)( |\t)*,( |\t)*\[([a-zA-Z]+|-?[0-9]+)\]( |\t)*$")# term index 5 array declaration access
regexTerms.append(r"^( |\t)*\[([a-zA-Z]+|-?[0-9]+)\]( |\t)*,( |\t)*([a-zA-Z]+|-?[0-9]+)( |\t)*$")


registers = {"R1": 0,"R2":0, "R3":0, "R4":0,"R5":0,"R6":0,"R7":0,"R8":0, "R9":0}

def readLine():
    try:
        textFile = open("Benchmark2.txt", 'r')
        for line in textFile: # This for loop will place all lines into a list for syntax check
            line = line.strip()
            text_array.append(line)
    except:
        print ("File does not exist")
        print "Terminating Program"
        exit(1)

def verifySyntax(): # Function to verify if code has correct syntax
    lineNumber = 1
    for f in text_array:
        if re.match(regexTerms[0], f):
            #print f
            index = text_array.index(f)
            text_array[index] = re.split(",", f) # Strings split at commas (spaces included in strings however)
            text_array[index][0] = text_array[index][0].strip()
            text_array[index][1] = text_array[index][1].strip()
            #print text_array[index]
        elif re.match(regexTerms[1], f):
            #print "In second: ", f
            index = text_array.index(f)
            text_array[index] = re.split(",", f)
            #print text_array[index], "Before"
            text_array[index][0] = text_array[index][0].strip()
            text_array[index][1] = text_array[index][1].strip()
            temp = text_array[index][0].split(" ")
            text_array[index].remove(text_array[index][0])
            text_array[index].insert(0,temp[0])
            text_array[index].insert(1,temp[-1])
            #print text_array[index], "After"
        elif re.match(regexTerms[2], f):
            text_array[text_array.index(f)] = ""
        elif re.match(regexTerms[3], f):
            temp = "".join(f.split())    
            text_array[text_array.index(f)] = [temp[:len(temp) -1],temp[-1]]
        elif re.match(regexTerms[4], f):
            text_array[text_array.index(f)] = text_array[text_array.index(f)].strip().upper().split()
        elif re.match(regexTerms[5], f):
            text_array[text_array.index(f)] = re.split(",", f)
        elif re.match(regexTerms[6], f):
            text_array[text_array.index(f)] = re.split(",", f) 
        else:
            print "Syntax Error on line", lineNumber, ": ", f
            print "Terminating Program"
            exit(1)
        #print lineNumber + text_array[lineNumber]
        lineNumber = lineNumber + 1
        

def execute():
    global next_memory_address
    lineNumber = 1
    while lineNumber - 1 < len(text_array):
        #print "lineNumber", lineNumber
        instruction = text_array[lineNumber -1]
        
        #print "Instruction:", instruction

        if len(instruction) == 0:
                lineNumber = lineNumber + 1
                continue
        elif len(instruction) == 1:
           if instruction[0] == "HALT":
               print "HALT detected: Ending Program"
               exit(1)

        elif len(instruction) == 2: # Variable/register declaration
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
                if key2[0] == '[':
                    if key2[1:-1] in variable_holder:
                        right = variable_holder[key2[1:-1]]
                    else:
                        right = isValidNumber(key2[1:-1],lineNumber)
                    variable_holder[key] = memory_addresses[right]    
                elif key2 in registers:
                    variable_holder[key] = registers[key2]
                elif key2 in variable_holder:
                    variable_holder[key] = variable_holder[key2]
                elif key2 == "INPUT":
                    variable_holder[key] = isValidNumber(raw_input("Enter Input: "),lineNumber)
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
            elif key[0] == "[":
                left = 0
                right = 0
                if key[1:-1] in variable_holder:
                    left = variable_holder[key[1:-1]]
                else:
                    left = isValidNumber(key[1:-1],lineNumber)
                if key2 in variable_holder:
                    right = variable_holder[key2]
                else:
                    right = isValidNumber(key2,lineNumber)
                memory_addresses[left] = right
            else:
                if key2[0] == '[':
                    variable_holder[key] = next_memory_address
                    next_memory_address = next_memory_address + isValidNumber(key2[1:-1],lineNumber)      
                else:   
                    variable_holder[key] = isValidNumber(key2, lineNumber)

        # Checks for instruction with length of 3
        elif len(instruction) == 3:

            opCode = instruction[0] #the read opCode
            #print opCode
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
                #print "Got a skip"
                lineNumber = skip(instruction,lineNumber)
               
            else:
                print "Error on line",lineNumber,":"
                print "\t\"",instruction[0],"\" Is not a valid op code!"
                print "Terminating Program"
                exit(1)
        
        #print instruction
        lineNumber += 1

def add(instruction):
    #print instruction
    left_num = 0
    right_num = 0
    #print variable_holder
    left_num = int(variable_holder[instruction[1]])

    if instruction[2] in variable_holder:
        right_num = int(variable_holder[instruction[2]])
    elif instruction[2] in registers:
        right_num = int(registers[instruction[2]])
    else:
        right_num = int(instruction[2])
    variable_holder[instruction[1]] += right_num
    #print variable_holder[instruction[1]]


def subt(instruction):
    #print instruction
    left_num = 0
    right_num = 0
    #print variable_holder
    left_num = int(variable_holder[instruction[1]])

    if instruction[2] in variable_holder:
        right_num = int(variable_holder[instruction[2]])
    elif instruction[2] in registers:
        right_num = int(registers[instruction[2]])
    else:
        right_num = int(instruction[2])
    variable_holder[instruction[1]] -= right_num
    #print variable_holder[instruction[1]]

def mult(instruction):
    #print instruction
    left_num = 0
    right_num = 0
    #print variable_holder
    left_num = int(variable_holder[instruction[1]])

    if instruction[2] in variable_holder:
        right_num = int(variable_holder[instruction[2]])
    elif instruction[2] in registers:
        right_num = int(registers[instruction[2]])
    else:
        right_num = int(instruction[2])
    variable_holder[instruction[1]] *= right_num
    #print variable_holder[instruction[1]]

def div(instruction, lineNum):
    #print instruction
    left_num = 0
    right_num = 0
    #print variable_holder
    left_num = int(variable_holder[instruction[1]])

    if instruction[2] in variable_holder:
        right_num = int(variable_holder[instruction[2]])
    elif instruction[2] in registers:
        right_num = int(registers[instruction[2]])
    else:
        right_num = int(instruction[2])
    variable_holder[instruction[1]] += right_num
    #print variable_holder[instruction[1]]

    try: 
        variable_holder[instruction[1]] /= right_num
        #print variable_holder[instruction[1]]
    except: 
        print "Error on Line", lineNum, ": Cannot divide by 0"
        exit(1)

def jump(instruction):
    #print(instruction)
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
        #print "Made SKIPE"
        if(left == right):
            #print left == right
            
            i = lineNum
            #print i
            while text_array[i] == "":
                i = i + 1
                #print i
            return i+1
    elif(instruction[0] == "SKIPG"):
        if(left > right):
            #print left == right
            
            i = lineNum
            #print i
            while text_array[i] == "":
                i = i + 1
                #print i
            return i+1
    elif(instruction[0] == "SKIPL"):
        if(left < right):
            #print left == right
            
            i = lineNum
            #print i
            while text_array[i] == "":
                i = i + 1
                #print i
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
#print text_array
execute()
