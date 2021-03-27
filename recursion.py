import math

"""Pyhton file for recursion exercise from module 3
"""

def reverseDigits(n:int) -> int:
    """Reverse the order of the digits of n 
    """
    
    if n == 0:
        return 0
    else:
        l = int(math.log10(n)) 
        m = n % 10
        q = 10 ** l
        # print(q)
        return m * (q) + reverseDigits(n//10)
        
        
def reverseDigits2(n:int, m:int=0) -> int:
    # print(n,m)
    if n == 0:
        return m
    else:
        m = m * 10 + (n % 10)
        return reverseDigits2(n // 10, m)
        
    
print(reverseDigits(123456))
print(reverseDigits2(123456))
