from enum import Flag, auto
import sys

class ContraOps(Flag):
    printf = "printf"
    var = "var"

class Contra:
    def __init__(self, filename):
        with open(filename) as file:
            lines = file.readlines()
            self.lines = [line.rstrip() for line in lines]
            self.vars = {}
            self.compile(self.lines)
    def compile(self, data):
        lineNumber = 0
        i = -1
        while i < len(data)-1:
            i += 1
            #print("index:"+str(i))    
            line = data[i]
            lineNumber += 1
            tokens = line.split()
            if(len(tokens) <= 0): continue
            operation = tokens[0]
            if line[0] == "#": continue
            if(tokens[-1][-1] != ";" and tokens[-1][-1] != "{" and tokens[-1][-1] != "}"):
                self.print_line_error(line, lineNumber)
            tokens[-1] = tokens[-1].replace(";", "")
            if operation == "printf":
                if(len(tokens) <= 1): 
                    print("ERROR: line: " + str(lineNumber)  + " 'printf' requires 1 additional argument")
                    self.exit()
                if "'" in tokens[1]:
                    if tokens[1].count("'") == 1:  
                        self.print_line_error(line, lineNumber)
                if '"' in tokens[1]:
                    if tokens[1].count('"') == 1:      
                        self.print_line_error(line, lineNumber)
                if '"' not in tokens[1] and "'" not in tokens[1]:
                    if tokens[1] in self.vars.keys():
                        text = str(self.vars[tokens[1]])
                        text = text.replace("'", "")
                        text = text.replace('"', "")
                        print(text)
                        continue
                    else:
                        self.print_line_error(line, lineNumber)
                tokens[1] = tokens[1].replace("'", "")
                tokens[1] = tokens[1].replace('"', "")
                print(tokens[1])
            elif operation == "var":
                if(len(tokens) < 4):
                    self.print_line_error(line, lineNumber)
                if(tokens[2] == "="):
                    if "'" in tokens[3]:
                        if tokens[3].count("'") == 1:  
                            self.print_line_error(line, lineNumber)
                    if '"' in tokens[3]:
                        if tokens[3].count('"') == 1:      
                            self.print_line_error(line, lineNumber)
                    if tokens[3].isnumeric(): tokens[3] = int(tokens[3])
                    if tokens[3] == "true": tokens[3] = True
                    if tokens[3] == "false": tokens[3] = False
                    self.vars[tokens[1]] = tokens[3]
            elif operation == "if": 
                if(len(tokens) >= 4):
                    first = None
                    second = None
                    if tokens[1].count("'") == 2 or tokens[1].count('"') == 2 or tokens[1].isnumeric():
                        first = tokens[1]
                    elif tokens[1] == "true":
                        first = True
                    elif tokens[1] == "false":
                        first = False
                    else:
                        if tokens[1] in self.vars.keys():
                            first = self.vars[tokens[1]]
                        else:
                            self.print_line_error(line, lineNumber)

                    if tokens[3].count("'") == 2 or tokens[3].count('"') == 2  or tokens[3].isnumeric():
                        second = tokens[3]
                    elif tokens[3] == "true":
                        second = True
                    elif tokens[3] == "false":
                        second = False
                    else:
                        if tokens[3] in self.vars.keys():
                            second = self.vars[tokens[3]]
                        else:
                            self.print_line_error(line, lineNumber)
                    if(tokens[2] == "=="):
                        if first == second:
                            body = []
                            endLine = 0
                            for j in range(lineNumber, len(data)):
                                currentLine = self.lines[j]
                                currentLineTokens = currentLine.split()
                                endLine = j+1
                                if(currentLineTokens[-1][-1] == "}"): break
                                body.append(currentLine)
                            print(body)
                            self.compile(body)
                            i = endLine-1
                            # Find and execute body
                            # Skip lines
                        else:
                            endLine = 0
                            for j in range(lineNumber, len(data)):
                                currentLine = self.lines[j]
                                currentLineTokens = currentLine.split()
                                endLine = j+1
                                if(currentLineTokens[-1][-1] == "}"): break
                            i = endLine-1
                    if(tokens[2] == "!="):
                        if first != second:
                            body = []
                            endLine = 0
                            for j in range(lineNumber, len(data)):
                                currentLine = self.lines[j]
                                currentLineTokens = currentLine.split()
                                endLine = j+1
                                if(currentLineTokens[-1][-1] == "}"): break
                                body.append(currentLine)
                            self.compile(body)
                            i = endLine-1
                            # FInd and execute body
                            # Skip lines
                        else:
                            endLine = 0
                            for j in range(lineNumber, len(data)):
                                currentLine = self.lines[j]
                                currentLineTokens = currentLine.split()
                                endLine = j+1
                                if(currentLineTokens[-1][-1] == "}"): break
                            i = endLine-1
                else:
                    self.print_line_error(line, lineNumber)
            else:
                if(len(tokens) < 2):
                    if tokens[-1][-1] == "}":
                        continue
                    else:
                        self.print_line_error(line, lineNumber)
                if(tokens[1] == "+="):
                    if(tokens[0] in self.vars.keys()):
                        if tokens[2].count("'") == 2 or tokens[2].count('"') == 2:
                            if(type(self.vars[tokens[0]]) == type(tokens[2])):
                                self.vars[tokens[0]] += tokens[2]
                            else:
                                self.print_type_error(line, str(tokens[0]), str(tokens[2]), lineNumber, False)
                        else:
                            if(tokens[2].isnumeric()):
                                self.vars[tokens[0]] += int(tokens[2])
                            else:
                                if(tokens[2] in self.vars.keys()):
                                    if(type(self.vars[tokens[0]]) == type(self.vars[tokens[2]])):
                                        self.vars[tokens[0]] += self.vars[tokens[2]]
                                    else:
                                        self.print_type_error(line, str(tokens[0]), str(tokens[2]), lineNumber, True)
                                else:
                                    self.print_line_error(line, lineNumber) 
                if(tokens[1] == "="):
                    if tokens[2].count("''") == 2 or tokens[2].count('"') == 2:
                        self.vars[tokens[0]] = tokens[2]
                    else:
                        if(tokens[2].isnumeric()):
                            self.vars[tokens[0]] = int(tokens[2])
                        else:
                            if(tokens[2] in self.vars.keys()):
                                self.vars[tokens[0]] = self.vars[tokens[2]]
                            else:
                                self.print_line_error(line, lineNumber)

    def print_line_error(self, line, ln):
        print("ERROR: Invalid syntax: " + line + " | at " + str(ln))
        self.exit()
    def print_type_error(self, line, first, second, ln, mode_var):
        if mode_var:
            print("ERROR: Invalid type: " + line + " | "+ str(first) + " type: " + str(type(self.vars[first]))  + " whilst " + str(second) + " type: " + str(type(self.vars[second]))  + " | at " + str(ln))
        else:
            print("ERROR: Invalid type: " + line + " | "+ str(first) + " type: " + str(type(self.vars[first]))  + " whilst " + str(second) + " type: " + str(type(second))  + " | at " + str(ln))
        self.exit()
    def exit(self):
        sys.exit()

if __name__ == "__main__":
    if(len(sys.argv) <= 0): 
        print("ERROR: No input file give.")
        sys.exit()
    Contra(sys.argv[1])

