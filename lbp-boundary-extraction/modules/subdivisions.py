
# rounding up integers to the nearest hundred
def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100