"""
Function：output a delay-probability curve graph
"""
from decimal import *
import math

def get_factorial(x):
    """
    Calculate the factorial of integer
    input:
        x:integer
    return:factorial(阶乘)
    """
    dat = int(x)
    p = 1
    if dat != 0:
        for i in range(1,dat+1):
             p *= i 
    return p

def tdma_delay_bound(arrival_rate, link_rate, portion, max_packet_length):
    """
    Get a function about the relationship of delay and probability
    input:
        arrival_rate: the rate of possion process(fixed number)
        link_rate: the rate of the various link(list）
        portion: the propotion of business in various link(list)
        max_packet_length： (fixed number)
    return: a function(given delay return probability)
    """
    assert(len(link_rate) == len(portion))
    t = 30
    def get_pro(x): #x:T delay 
        getcontext().prec = 8
        bound_delay = Decimal(0)
        delay_T = 0

        for i in range(len(link_rate) - 1):
            delay_T += max_packet_length / (link_rate[i] * portion[i])

        r = min([(i+1) * (j+1) for i, j in zip(link_rate, portion)])      
        if x > delay_T:
            y = r * (x - delay_T)
            for i in range(0, math.ceil(y + arrival_rate * t) - 1):
                bound_delay += Decimal(math.exp(-arrival_rate * t)) *\
                ((arrival_rate * t) ** i) / get_factorial(i)
            bound_delay = 1 - bound_delay
            return bound_delay.quantize(Decimal('0.0000'))#decimal -> float
        else:
            return 1  
    return get_pro
    # return a function: given delay return probability


if __name__ == "__main__":
    """
    test
    """
    max_packet_length = 256
    arrival_rate = 12
    link_rate = [4, 10, 15]
    portion = [1, 1, 0.5]
    bound = tdma_delay_bound(arrival_rate,link_rate,portion,max_packet_length)

    xs = range(0, 100)
    pro = [bound(x) for x in xs]
    
    #print(list(zip(xs, pro)))