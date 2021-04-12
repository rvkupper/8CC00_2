import math

"""Pyhton file for recursion exercise from module 3
"""

def reverseDigits(n:int, m:int=0) -> int:
    """Reverse the order of the digits of n 
    """
    if n == 0:
        return m
    else:
        m = m * 10 + (n % 10)
        return reverseDigits(n // 10, m)      
    

print(reverseDigits(123456))
