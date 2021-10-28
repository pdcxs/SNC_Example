"""
Function: caculate the bound of the packet service time on IEEE 802.11 DCF
          and get the delay_bound curve graph
"""
from get_prob import *

get_B_first_moment = get_total

def get_B_second_moment(pc, k, m, cw):
    """
    Calculate the second moments of the sum of backoff intervals(M_B^2)
    input:
        pc: the collision probability
        k : maximum retransmission 
        m : maximum content window grow times
        cw: initial content window size
    return: M_B^2
    """
    s1 = 0
    s2 = 0

    for i in range(k + 1):
        s1 += (get_stage_average(i, k, m, cw) ** 2 +
               get_stage_variance(i, k, m, cw)) * pc ** i
        if i > 0:
            s3 = 0
            for j in range(i - 1):
                s3 += get_stage_average(j, k, m, cw)

            s2 += get_stage_average(i, k, m, cw) * \
                  (pc ** k) * s3
    
    return s1 + 2 * s2

def get_X_first_moment(n, pc, sigma, ts, tc):
    """
    Calculate the first moments of 𝑋𝑖 
    (𝑋𝑖 denote the duration that the backoff counter decrements by 1)
    input:
        n: number of nodes in the same communication range
        pc：the collision probability
        sigma：one slot tine
        ts: channel busy slot number because of success transmission
        tc: channel busy slot number because of collision
    return: M_X1
    """
    p_suc = get_success_prob(n, get_trans_prob(n, pc))
    return ((1 - pc) + p_suc * (ts - tc) + pc * tc) * sigma

def get_X_second_moment(n, pc, sigma, ts, tc):
    """
    Calculate the second moments of 𝑋𝑖 
    input:
        n: number of nodes in the same communication range
        pc：the collision probability
        sigma：one slot tine
        ts: channel busy slot number because of success transmission
        tc: channel busy slot number because of collision
    return: M_X2
    """
    p_suc = get_success_prob(n, get_trans_prob(n, pc))
    return ((1 - pc) + 
        p_suc * (ts * ts - tc * tc) + 
        pc * tc * tc) * sigma * sigma

def get_BI_first_moment(n, pc, k, m, cw, sigma, ts, tc):
    """
    Calculate the first moments of a compound random variable（specific explanation in ReadMe.md)
    input:
        n: number of nodes in the same communication range
        pc：the collision probability
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
        sigma：one slot tine
        ts: channel busy slot number because of success transmission
        tc: channel busy slot number because of collision
    return: the first moments of a compound random variable(M_B+I_1)
    (see it in ReadMe.md)
    """
    mb = get_B_first_moment(pc, k, m, cw)
    mx = get_X_first_moment(n, pc, sigma, ts, tc)
    return mb * mx

def get_BI_second_moment(n, pc, k, m, cw, sigma, ts, tc):
    """
    Calculate the second moments of a compound random variable（specific explanation in ReadMe.md)
    input:
        n: number of nodes in the same communication range
        pc：the collision probability
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
        sigma：one slot tine
        ts: channel busy slot number because of success transmission
        tc: channel busy slot number because of collision
    return: the second moments of a compound random variable(M_B+I_2)
    (see it in ReadMe.md)
    """
    mb1 = get_B_first_moment(pc, k, m, cw)
    mx1 = get_X_first_moment(n, pc, sigma, ts, tc)

    mb2 = get_B_second_moment(pc, k, m, cw)
    mx2 = get_X_second_moment(n, pc, sigma, ts, tc)

    return mb1 * mx2 + (mb2 - mb1) * mx1 * mx1

def get_C_first_moment(k, pc, tc):
    """
    Calculate the first moments of the sum of collision 
    input:
        k: maximum retransmission 
        pc：the collision probability
        tc: channel busy slot number because of collision
    return: the first moments of the sum of collision(M_C1)
    """
    return tc * sum([pc ** i for i in range(1, k+1)])

def get_C_second_moment(k, pc, tc):
    """
    Calculate the second moments of the sum of collision 
    input:
        k: maximum retransmission 
        pc：the collision probability
        tc: channel busy slot number because of collision
    return: the second moments of the sum of collision(M_C1)
    """
    return tc * tc * sum([(2 * i - 1) * pc ** i for i in range(1, k + 1)])

def get_service_first_moment(n, pc, k, m, cw, sigma, ts, tc):
    """
    Calculate the first moment of the service time 𝛿
    input:
        n: number of nodes in the same communication range
        pc：the collision probability
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
        sigma：one slot tine
        ts: channel busy slot number because of success transmission
        tc: channel busy slot number because of collision
    return: the first moment of the service time 𝛿(M_ 𝛿1)
   
    """
    mbi = get_BI_first_moment(n, pc, k, m, cw, sigma, ts, tc)
    mc = get_C_first_moment(k, pc, tc)
    return mbi + mc + ts


def get_total_first_moment(n, pc, k, m, cw, sigma, ts, tc):
    """
    Calculate M_Delta^1(Delta = C + B*sigma + I)
    input:
        n: number of nodes in the same communication range
        pc：the collision probability
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
        sigma：one slot tine
        ts: channel busy slot number because of success transmission
        tc: channel busy slot number because of collision
    return:  M_Delta^1
    """
    mbi = get_BI_first_moment(n, pc, k, m, cw, sigma, ts, tc)
    mc = get_C_first_moment(k, pc, tc)
    return mbi + mc

def get_total_second_moment(n, pc, k, m, cw, sigma, ts, tc):
    """
    Calculate M_Delta^2(Delta = C + B*sigma + I)
    input:
        n: number of nodes in the same communication range
        pc：the collision probability
        k: maximum retransmission 
        m: maximum content window grow times
        cw: initial content window size
        sigma：one slot tine
        ts: channel busy slot number because of success transmission
        tc: channel busy slot number because of collision
    return:  M_Delta^2
    """
    mbi1 = get_BI_first_moment(n, pc, k, m, cw, sigma, ts, tc)
    mc1 = get_C_first_moment(k, pc, tc)

    mbi2 = get_BI_second_moment(n, pc, k, m, cw, sigma, ts, tc)
    mc2 = get_C_second_moment(k, pc, tc)

    return mc2 + mbi2 + 2 * mc1 * mbi1


def dcf_delay_bound(x, n, k, m, cw, ts, tc, sigma):
    """
    Caculate the bound of the packet service time on IEEE 802.11 DCF
    input:
        x: delay(service time equals to delay for single packet)
        n: number of nodes in the same communication range
        k: maximum transmission
        m: maximum content window grow times
        cw: initial content window size
        ts: channel busy slot number because of success send
        tc: channel busy slot number because of collision
        sigma: one solt time
    return: the bound of the packet service time
    """
    if x <= ts:
        return 
    _, pc = get_prob(n, k, m, cw, 1e-6)
    m1 = get_total_first_moment(n, pc, k, m, cw, sigma, ts, tc)
    m2 = get_total_second_moment(n, pc, k, m, cw, sigma, ts, tc)
    return min(m1 / (x - ts), m2 / (x - ts) / (x - ts), 1)

if __name__ == "__main__":
    k = 6
    m = 4
    cw = 32
    n = 5
    ts = 256
    tc = 5
    sigma = 0.0001

    xs = range(10000, 20000, 1000)
    p = [Dcf_bound(x, n, k, m, cw, ts, tc, sigma) for x in xs]
    print(list(zip([sigma * x for x in xs], p)))