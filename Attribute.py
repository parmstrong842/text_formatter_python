def setVariable (atString, varDictionary):
    """Checks if the atString is valid and then puts
    the key and value pair into the variable dictionary.

    Args:
        atString (str): A string containing the key and value pair.
        varDictionary (dictionary): The dictionary to store the pair
    """
    # check for '@' at beginning of string
    if atString[0] != '@':
        print("*** Invalid atString: %s" % atString)
        return
    atString = atString[1:]
   
    # checks for missing token
    tokens = atString.split('=')
    if tokens[0] == '' or tokens[1] == '':
        print("*** Invalid atString: %s" % atString)
        return

    # remove quotes from string
    if tokens[1][0] == '"':
        tokens[1] = tokens[1][1:-1]

    varDictionary[tokens[0]] = tokens[1]


def setFormat (atString, formatDictionary):
    """Checks if the atString is valid and then puts
    the key and value pairs into the format dictionary.

    Args:
        atString (str): A string containing the key and value pairs.
        formatDictionary (dictionary): The dictionary to store the pairs
    """
    tokens = atString.split()
    for token in tokens:
        pair = token.split("=")

        # checks if key is valid
        is_valid = False
        for key in formatDictionary.keys():
            if pair[0] == key:
                is_valid = True
                break
        if not is_valid:
            print("*** Invalid format, found: %s" % atString)
            return

        # if key is 'JUST', checks if the value is valid
        if pair[0] == "JUST":
            is_valid = False
            if pair[1] == "LEFT" or pair[1] == "RIGHT" \
                    or pair[1] == "BULLET" or pair[1] == "CENTER":
                is_valid = True
        if not is_valid:
            print("*** Bad value for JUST=, found: %s" % pair[1])
            return

        formatDictionary[pair[0]] = pair[1]
