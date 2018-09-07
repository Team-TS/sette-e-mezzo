from random import random

def prob(chance):
    """Takes an argument of an integer between 1 and 99 and returns true or false based on that % chance."""
    if isinstance(chance, int) and chance >= 1 and chance <= 99:
        check = random() * 100
        if check < chance:
            return True
        else:
            return False
    else:
        raise TypeError("Argument chance must be an interger between 1-99.")