# Task 1 & 2: Miller–Rabin implementation, testing, plotting, and base‐impact analysis

import math
import random
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import progressbar

# 1. Generate prime list via sieve (100–1_000_000)
def sieve(n):
    sieve = [True] * (n+1)
    sieve[0:2] = [False, False]
    for p in range(2, int(n**0.5)+1):
        if sieve[p]:
            for multiple in range(p*p, n+1, p):
                sieve[multiple] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

PRIMES = sieve(10_000_000)
PRIME_SET = set(PRIMES)

# 2. Miller‑Rabin test
def miller_rabin(n, bases=None, k=5):
    """Return False for composite, True for probably prime."""
    if n < 2:
        return False
    # small primes check
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n == p:
            return True
        if n % p == 0:
            return False
    # write n-1 = d * 2^s
    d, s = n-1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Alternative method doesn't take advantage of %n improvements each iteration so is much longer for large "n":
    """
    if bases is None:
        bases = [random.randrange(2, n-1) for _ in range(k)]
    for a in bases:
        spp = False
        x1 = pow(a, d)
        x = x1 % n
        if x == 1 or x == n-1:
            spp = True
        if not spp:
            for _ in range(s-1):
                x1 = pow(x1, 2)
                x2 = x1 % n
                if x2 == n-1:
                    spp = True
                    break
        if not spp:
            return False
    return True
    """
    # choose bases
    if bases is None:
        bases = [random.randrange(2, n - 1) for _ in range(k)]
    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# 3. Unit tests
# pick some known primes/composites
test_primes = [101, 103, 1009, 50021, 999983]
test_composites = [100, 102, 1000, 50020, 999981]
assert all(miller_rabin(p, bases=[2,7,61]) for p in test_primes)
assert all(not miller_rabin(c, bases=[2,7,61]) for c in test_composites)

# 4. Task 1: false-positive rolling average
max_n = 10_000_000
window = 100_000
fps = []  # 1 if false positive at n, else 0
ns = []
for n in range(100, max_n+1):
    if n in PRIME_SET:
        # skip true primes
        fps.append(0)
    else:
        fps.append(1 if miller_rabin(n, bases=[2,7,61]) else 0) # ,7,61
    ns.append(n)

# compute rolling average
rolling = []
dq = deque()
sum_fp = 0
for i, val in enumerate(fps):
    dq.append(val)
    sum_fp += val
    if len(dq) > window:
        sum_fp -= dq.popleft()
    rolling.append(sum_fp / len(dq))

# plot
plt.figure()
plt.plot(ns, rolling)
plt.xlabel("n")
plt.ylabel(f"False-positive rate (window={window})")
plt.title("Rolling false-positive rate of Miller–Rabin (bases [2, 7, 61])") #try just [2] also
plt.tight_layout()
plt.show()

# 5. Task 2: impact of single-base tests
bases_to_test = [2,3,4,5,10,11,12,16,17,19,25,29,31,32]


false_counts_all = {}
for ix, a in enumerate(bases_to_test):
    count = 0
    for n in range(100, int(max_n/100) +1 ):
        if n not in PRIME_SET and miller_rabin(n, bases=[a]):
            count += 1
    if a not in false_counts_all:
        false_counts_all[a] = [count, 0, 0]
    else:
        false_counts_all[a][0] = count


bar = progressbar.ProgressBar(max_value=len(bases_to_test))
for ix, a in enumerate(bases_to_test):
    count = 0
    for n in range(100, int(max_n/10) +1 ):
        if n not in PRIME_SET and miller_rabin(n, bases=[a]):
            count += 1
    if a not in false_counts_all:
        false_counts_all[a] = [0, count, 0]
    else:
        false_counts_all[a][1] = count
    bar.update(ix + 1)


liars_ranking = {}
bar = progressbar.ProgressBar(max_value=len(bases_to_test))
for ix, a in enumerate(bases_to_test):
    count = 0
    for n in range(100, max_n+1):
        if n not in PRIME_SET and miller_rabin(n, bases=[a]):
            count += 1
            if n not in liars_ranking:
                liars_ranking[n] = 1
            else:
                liars_ranking[n] += 1
    if a not in false_counts_all:
        false_counts_all[a] = [0, 0, count]
    else:
        false_counts_all[a][2] = count
    bar.update(ix + 1)

# print summary
print("False positives by base A:")
for a, cnt in sorted(false_counts_all.items(), key=lambda x: x[1][2], reverse=True):
    print(f"Base {a}: {cnt[2]} false positives")

#plot false counts of "A" across the 3 ranges of n to see change/trajectory:
plt.figure()
plot_count = 0
for a, cnt in sorted(false_counts_all.items(), key=lambda x: x[0], reverse=True):
    line_type = "-"
    if plot_count % 2 == 0:
        line_type = "--"
    plot_count += 1
    plt.plot([int(max_n/100), int(max_n/10), max_n], cnt, label=f"Base 'A' = {a}", linestyle=line_type)
plt.xscale('log')
plt.xlabel("n (log scale)")
plt.ylabel(f"FPs by Base 'A's chosen")
plt.title("Determining which Miller–Rabin 'A' bases yield more FPs")
#plt.tight_layout()
plt.legend()
plt.show()


#plot which composite numbers have the most liars
for n, cnt in sorted(liars_ranking.items(), key=lambda x: x[1], reverse=False):
    print(f"liar n= {n}, cheating {cnt} of the 'A' bases out of {len(bases_to_test)} possible bases")

all_dicts = []

biggest = 0
for n, cnt in sorted(liars_ranking.items(), key=lambda x: x[1], reverse=True):
    biggest = cnt
    break

for i in range(biggest):
    filtered_dict = dict(filter(lambda x: x[1] == i+1, liars_ranking.items()))
    all_dicts.append(len(filtered_dict))


categories = list(range(1, biggest + 1))
values = all_dicts

# Create the bar plot
plt.bar(categories, values, color='skyblue')

# Add labels and title
plt.xlabel(f"Number of times a Liar Lies out of {len(bases_to_test)} bases")
plt.ylabel(f'The Amount of Liars found, 0 to "n" = {max_n}')
plt.title('Showing Liars That Lie Multiple Times')

# Add value labels on top of bars
for index, value in enumerate(values):
    plt.text(index + 1, value + 0.5, str(value), ha='center', va='center')

# Show the plot
plt.show()