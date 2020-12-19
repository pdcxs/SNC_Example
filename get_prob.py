"""
Function: get the attempt probability(pa),the collision probability(pc)
          and the probability of successful transmission(p_suc)
"""

from math import log, exp

def get_window(i, k, m, cw):
    """
    Calculate the size of window
    input:
        i : the ith backoff stage
        k : maximum retransmission 
        m : maximum content window grow times
        cw: initial content window size
    return:the window of the ith retansmission
    """
    assert (k > m and i <= k)

    return 2**min(i, m)*cw

def get_total_window(k, m, cw):
    """
    Calculate the size of the total window
    input:
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size 
    return:the size of the total window
    """
    s = 0
    for i in range(k + 1):
        s += get_window(i, k, m, cw) - 1
    return s

def get_stage_average(i, k, m, cw):
    """
    Calculate the mean of window size at the ith backoff stage
    input:
        i: the ith backoff stage
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
    return: u_k
    """
    return (get_window(i, k, m, cw) - 1) / 2

def get_stage_variance(i, k, m, cw):
    """
    Calculate the varirance of window size at the ith backoff stage
    input:
        i: the ith backoff stage
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
    return: sigma_k^2
    """
    w = get_window(i, k, m, cw)
    return (w - 1.0) * (w - 1.0) / 12.0

def get_total(p, k, m, cw):
    """
    Calculate the sum of u_k * pc(M_B1)
    input:
        p: the collision probability
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
    return: M_B1

    """
    return sum([get_stage_average(i, k, m, cw) * p**i\
            for i in range(k+1)])

def get_duration(func, min_, max_):
    """
    Calculate the range of independent variable with opposite sign values
    input:
        func: any equation
        min_, max_: the maximum range of independent variable with opposite sign values

    return: a range(left,right)
    """
    assert max_ > min_
    r = max_ - min_
    div = 2
    step = r / div

    results = [func(min_ + step * i) for i in range(div)]

    for i in range(div - 1):
        if results[i] * results[i + 1] <= 0:
            return (min_ + i * step, min_ + (i + 1) * step)

    return (max_ - step, max_)

def get_prob(n, k, m, cw, eps):
    """
    Caculate the attempt probability(pa),the collision probability(pc)
    input:
        n: number of nodes in the same communication range
        eps: the accuracy
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
    return: pa,pc
    """
    equation = lambda p : \
        get_trans_prob(n, p) - \
        (p ** (k + 1) - 1) / (p - 1) / \
        get_total(p, k, m, cw)

    l, u = 0, 1
    while u - l >= eps:
        l, u = get_duration(equation, l, u)
    
    assert(l < 1 and u < 1 and l > 0 and u > 0)
    if abs(equation(l)) < abs(equation(u)):
        return (get_trans_prob(n, l), l)
    else:
        return (get_trans_prob(n, u), u)

def get_collision_prob(n, trans_prob):
    """
    Get the expression for pc in terms of pa
    input:
        n：number of nodes in the same communication range
        trans_prob: the attempt probability(pa)
    return: the expression for pc in terms of pa
    """
    return 1 - exp((1 - n) * trans_prob)

def get_trans_prob(n, colls_prob):
    """
    Get the expression for pc in terms of pa
    input:
        n：number of nodes in the same communication range
        colls_prob: the collision probability(pa)
    return: the expression for pa in terms of pc
    """
    return log(1 - colls_prob) / (1 - n)

def get_success_prob(n, pa):
    """
    Calculate the probability of successful transmission
    input:
        n: number of nodes in the same communication range
        pa: the attempt probability (pa)
    return: the probability of successful transmission
    """
    return (n - 1) * pa * (1 - pa) ** (n - 2)

if __name__ == "__main__":
    """
    test
    """
    k = 6
    m = 4
    cw = 32
    n = 10
    print(get_prob(n, k, m, cw, 1e-6))
