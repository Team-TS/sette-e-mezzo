from math import ceil

def trimOnSpace(text, chars):
    """Returns a list of trimmed strings to the nearest space before chars"""
    strings = []
    lastspace = 0
    key = 0
    lastsplit = 0
    for char in text:
        check = float(key / chars)
        if check.is_integer() and key != 0:
            strings.append(text[lastsplit:lastspace])
            lastsplit = lastspace
        if char == " " or char == "\n":
            lastspace = key
        key = key + 1
    strings.append(text[lastsplit:])

    return strings
