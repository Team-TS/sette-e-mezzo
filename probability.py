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

def probDrawExactValue(value, cardsavailable):
    """Return the probability of drawing a card with exactly the value specified and the potential draws provided."""
    num_true = 0 # Number of cards which satisfy the condition required.
    num_false = len(cardsavailable) # Total
    for card in cardsavailable:
        if float(card.value) == value:
            num_true = num_true + 1
    
    prob = float(num_true / num_false)

    return prob

def probDrawValueOrLess(value, cardsavailable):
    """Return the probability of drawing a card with exactly the value specified and the potential draws provided."""
    num_true = 0 # Number of cards which satisfy the condition required.
    num_false = len(cardsavailable) # Total
    for card in cardsavailable:
        if float(card.value) <= value:
            num_true = num_true + 1
    
    prob = float(num_true / num_false)

    return prob