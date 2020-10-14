import sys
import pprint
from Attribute import setVariable, setFormat
from Formatter import *

# checks for valid commandline arguments
if len(sys.argv) < 2:
    print("Filename needed as command argument")
    sys.exit(1)

file = open(sys.argv[1], "r", errors="ignore")
varDict = {}
formatDict = {"FLOW": "YES"
              , "LM": "1"
              , "RM": "80"
              , "JUST": "LEFT"
              , "BULLET": "o"}
formatter = Formatter(formatDict, varDict)

while True:
    # reads line and checks for end of file
    inputLine = file.readline()
    if inputLine == "":
        formatter.flushOverflow()
        break
    if inputLine == "\n":
        formatter.checkFlow()
        formatter.flushOverflow()
        formatter.startingParagraph = True
        print()
        continue
    inputLine = inputLine.rstrip('\n')
    inputLine = inputLine.rstrip()

    # checks for valid command and runs it
    tokens = inputLine.split()
    if inputLine[0:2] == "@.":
        if tokens[1] == "VAR":
            setVariable(inputLine[7:], varDict)
        elif tokens[1] == "FORMAT":
            formatter.formatFlush = True
            formatter.flushOverflow()
            formatter.formatFlush = False
            setFormat(inputLine[10:], formatDict)
        elif tokens[1] == "PRINT" and len(tokens) == 3:
            if tokens[2] == "VARS":
                pprint.pprint(varDict, width=30)
            elif tokens[2] == "FORMAT":
                pprint.pprint(formatDict, width=30)
            else:
                print("*** Invalid command: %s" % inputLine)
    else:
            formatter.formatOutput(inputLine)
