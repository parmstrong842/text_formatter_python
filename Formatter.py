class Formatter:
    """Formatter class for output"""

    def __init__(self, formatDict, varDict):
        self.output = ""
        self.overflow = ""
        self.flow = ""
        self.endOfParagraph = False
        self.startingParagraph = False
        self.formatFlush = False
        self.formatDict = formatDict
        self.varDict = varDict

    def formatOutput(self, output):
        """Substitutes @variables for their values

        Args:
             output (str): The string to modify
        """
        self.output = ""
        didWeSubstitute = False
        tokens = output.split()
        i = 0
        # look at each token for an @variable
        for token in tokens:
            if token[0] == '@':
                didWeSubstitute = True
                if token[-1] != ".":
                    tokens[i] = self.varDict.get(token[1:], "")
                if token[-1] == ".":
                    tokens[i] = self.varDict.get(token[1:-1], "")
                    tokens[i] = tokens[i] + "."
                if token[-1] == ",":
                    tokens[i] = self.varDict.get(token[1:-1], "")
                    tokens[i] = tokens[i] + ","
            i += 1

        # if no substitution happened then just print the line
        if didWeSubstitute:
            for token in tokens:
                self.output = self.output + token + " "
            if self.output and self.output[-1] == " ":
                self.output = self.output[:-1]
        else:
            self.output = output

        self.formatPrint()

    def formatPrint(self):
        """Uses the format dictionary to format the output"""
        LM = int(self.formatDict["LM"])
        RM = int(self.formatDict["RM"])

        # add bullet point
        if self.startingParagraph and self.formatDict["JUST"] == "BULLET":
            self.output = self.formatDict["BULLET"] + " " + self.output

        # add extra indent
        if self.formatDict["JUST"] == "BULLET" and not self.startingParagraph and not self.flow:
            LM = LM + 2
        elif self.formatDict["JUST"] == "BULLET":
            self.startingParagraph = False

        # add flow string to output
        if self.flow:
            self.output = self.flow + self.output
            self.flow = ""

        # add overflow to output
        self.output = self.overflow + self.output
        for i in range(LM - 1):
            self.output = " " + self.output

        tokens = self.output.split()

        # save flow string if necessary
        if len(self.output) < RM and self.formatDict["FLOW"] == "YES" and not self.endOfParagraph:
            self.output = self.output[LM-1:]
            self.flow = self.output + " "
            return

        # calculate end of output string
        length = LM - 1
        for token in tokens:
            if length + len(token) <= RM:
                length = length + len(token) + 1
            else:
                break
        length -= 1

        # check for overflow
        if len(self.output) > RM:
            self.overflow = self.output[length:] + " "
            if self.overflow[0] == " ":
                self.overflow = self.overflow[1:]
            self.output = self.output[:length]
        else:
            self.overflow = ""

        print(self.output)

    def flushOverflow(self):
        """If any overflow remains after a paragraph ends print it all out"""
        self.output = ""
        self.flow = ""
        if not self.formatFlush:
            self.startingParagraph = False
        self.endOfParagraph = True
        while self.overflow != "":
            self.output = ""
            self.formatPrint()
            if self.overflow and self.overflow[0] == " ":
                self.overflow = ""
        self.endOfParagraph = False

    def checkFlow(self):
        """if any flow remains after a paragraph ends print it all out"""
        if self.flow:
            for i in range(int(self.formatDict["LM"]) - 1):
                self.flow = " " + self.flow
            print(self.flow)
            self.flow = ""
