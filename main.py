import matplotlib.pyplot as plt
from dcf_delay import dcf_delay_bound
from tdma_delay import tdma_delay_bound

# maximum transmission try
k = 6
# maximum content window grow times
m = 4
# initial content window size
cw = 32
# number of nodes in the same communication range
n = 10
# channel busy slot number because of success send
ts = 256
# channel busy slot number because of collision
tc = 5

sigma = 0.01 # slot duration (unit: second)

xs = range(300, 1000, 50)
p1 = [dcf_delay_bound(x, n, k, m, cw, ts, tc, sigma) for x in xs]
# p2 = [service_bound2(x, n, k, m, cw, ts, tc, sigma) for x in xs]

fig, ax = plt.subplots()
ax.plot([x * sigma for x in xs], p1)
# ax.plot([x * sigma for x in xs], p2)

ax.set(xlabel='delay (s)', ylabel='Probability',
        title='Stochastic Service Curve of 802.11 DCF')
ax.grid()
fig.savefig("imgs/dcf_delay.png")
plt.show()


arrival_rate = 10
link_rate = [4, 3, 5]
portion = [1, 1, 0.5]
max_packet_length = 12
bound = tdma_delay_bound(
        arrival_rate,
        link_rate,
        portion,
        max_packet_length)

xs = range(5, 20)
prob = [bound(x) for x in xs]

sigma = 0.1

fig, ax = plt.subplots()
ax.plot([x * sigma for x in xs], prob)

ax.set(xlabel='delay (s)', ylabel='Probability',
        title='TDMA Stochastic Delay Upper Bound')
ax.grid()
fig.savefig("imgs/tdma_delay.png")
plt.show()