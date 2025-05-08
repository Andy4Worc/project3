import math
import random
import bisect
import matplotlib.pyplot as plt

import ECC_test

import progressbar

#CS 5080
#4/27/2025
#Initial code written by chatGPT. Heavily modified by Anderson Worcester

#project 3 - part of deliverable 1 code

def sieve(n):
    """
    Generate list of primes up to n using the Sieve of Eratosthenes.
    """
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]


# Precompute primes up to (1,000)^2 for the first part of the assignment
MAX_N = 1000
_primes = sieve(MAX_N**2)


def empirical_false_positive(n, trials=10000):
    """
    Empirically estimate the false positive rate by simulating the fingerprint test
    with x = 0 and y = K (constructed adversarially) for a number of trials.
    """
    # primes in (n, n^2]
    lo = bisect.bisect_right(_primes, n - 1)
    hi = bisect.bisect_right(_primes, n * n)
    primes_range = _primes[lo:hi]

    # build adversarial K factors (same as theoretical selection)
    mult_total = 1
    for p in primes_range:
        if mult_total * p < 2**n:
            mult_total = mult_total * p
        else:
            break

    # mult total is Alice's "Y" that the adversary gives her to then send, but Alice still has control of "p" and parity
    y = mult_total
    fp_count_no_parity = 0
    fp_count_1_parity = 0
    fp_count_2_parity = 0
    fp_count_4_parity = 0

    no_parity_size, parity_1_size, parity_2_size, parity_4_size = 0, 0, 0, 0

    for _ in range(trials):
        p = random.choice(primes_range)
        hash = y % p
        p_1 = ECC_test.build_one_bit_ECC(p, y)
        p_2 = ECC_test.build_two_bit_ECC(p, y)
        p_4 = ECC_test.build_four_bit_ECC(p, y)

        # Bob is then given (by the adversary) X = 0. Bob knows the parity (pre communicated) and tries to decode and check.
        if hash == 0:
            fp_count_no_parity += 1

        p_from_1, parity_1 = ECC_test.decode_one_bit_ECC(p_1)
        if hash == 0 and parity_1 == 0:
            fp_count_1_parity += 1

        p_from_2, parity_2 = ECC_test.decode_two_bit_ECC(p_2)
        if hash == 0 and parity_2 == 0:
            fp_count_2_parity += 1

        p_from_4, parity_4 = ECC_test.decode_four_bit_ECC(p_4)
        if hash == 0 and parity_4 == 0:
            fp_count_4_parity += 1

        if (p != p_from_1) or (p != p_from_2) or (p != p_from_4):
            exit("Primes decoded do not match what was sent!")

        # summing sizes of bits:
        hash_chosen_size = ECC_test.count_bits(hash)
        if hash == 0:
            no_parity_size += 1 + ECC_test.count_bits(p) # sending "0" result is 1 bit
            parity_1_size += 1 + ECC_test.count_bits(p_1)
            parity_2_size += 1 + ECC_test.count_bits(p_2)
            parity_4_size += 1 + ECC_test.count_bits(p_4)
        else:
            no_parity_size += ECC_test.count_bits(p) + hash_chosen_size
            parity_1_size += ECC_test.count_bits(p_1) + hash_chosen_size
            parity_2_size += ECC_test.count_bits(p_2) + hash_chosen_size
            parity_4_size += ECC_test.count_bits(p_4) + hash_chosen_size

    # After trials are over:
    if trials == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    else:
        no_parity_rate = fp_count_no_parity / trials
        parity_1_rate = fp_count_1_parity / trials
        parity_2_rate = fp_count_2_parity / trials
        parity_4_rate = fp_count_4_parity / trials

        avg_no_parity_size = no_parity_size / trials
        avg_parity_1_size = parity_1_size / trials
        avg_parity_2_size = parity_2_size / trials
        avg_parity_4_size = parity_4_size / trials

        data_size = ECC_test.count_bits(y)
        return no_parity_rate, parity_1_rate, parity_2_rate, parity_4_rate, avg_no_parity_size, avg_parity_1_size, avg_parity_2_size, avg_parity_4_size, data_size



def empirical_false_positive_remainder_experiment(n, trials=10000):
    """
    Empirically estimate the false positive rate by simulating the fingerprint test
    with x = 0 and y = K (constructed adversarially) for a number of trials.
    """
    # primes in (n, n^2]
    lo = bisect.bisect_right(_primes, n - 1)
    hi = bisect.bisect_right(_primes, n * n)
    primes_range = _primes[lo:hi]

    # build adversarial K factors (same as theoretical selection)
    mult_total = 1
    mult_total_remainder = 1
    for p in primes_range:
        if mult_total_remainder * p * 2 < 2**n:
            mult_total_remainder = mult_total_remainder * p
        else:
            break

    for p in primes_range:
        if mult_total * p < 2**n:
            mult_total = mult_total * p
        else:
            break

    # mult total is Alice's "Y" that the adversary gives her to then send, but Alice still has control of "p" and parity
    y_remainder = mult_total_remainder * 2 # Adversary does this is so that the remainder to X and Y is even for both
    y_reg = mult_total
    fp_count_no_remainder = 0
    fp_count_1_remainder = 0

    for _ in range(trials):
        p = random.choice(primes_range)
        hash_remainder = y_remainder % p
        hash_normal = y_reg % p
        p_1 = p * 2 + y_remainder % 2

        # Bob is then given (by the adversary) X = 0. Bob knows the parity (pre communicated) and tries to decode and check.
        if hash_normal == 0:
            fp_count_no_remainder += 1

        remainder = y_remainder % 2
        if hash_remainder == 0 and remainder == 0:
            fp_count_1_remainder += 1

    # After trials are over:
    if trials == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    else:
        no_remainder_rate = fp_count_no_remainder / trials
        remainder_1_rate = fp_count_1_remainder / trials

        return no_remainder_rate, remainder_1_rate


def run_fingerprint_experiments(n_min=6, n_max=1000, trials=10000):
    """
    Run both theoretical and empirical experiments for n in [n_min..n_max]
    and plot the results on the same matplotlib figure.
    """
    ns = list(range(n_min, n_max + 1))
    no_parity_rate_array = []
    parity_1_rate_array = []
    parity_2_rate_array = []
    parity_4_rate_array = []

    avg_no_parity_size_array = []
    avg_parity_1_size_array = []
    avg_parity_2_size_array = []
    avg_parity_4_size_array = []

    data_size_array = []

    bar = progressbar.ProgressBar(max_value=len(ns))

    for ix, n in enumerate(ns):
        no_parity_rate, parity_1_rate, parity_2_rate, parity_4_rate, avg_no_parity_size, avg_parity_1_size, avg_parity_2_size, avg_parity_4_size, data_size = empirical_false_positive(n, trials)
        no_parity_rate_array.append(no_parity_rate)
        parity_1_rate_array.append(parity_1_rate)
        parity_2_rate_array.append(parity_2_rate)
        parity_4_rate_array.append(parity_4_rate)

        avg_no_parity_size_array.append(avg_no_parity_size)
        avg_parity_1_size_array.append(avg_parity_1_size)
        avg_parity_2_size_array.append(avg_parity_2_size)
        avg_parity_4_size_array.append(avg_parity_4_size)

        data_size_array.append(data_size)

        bar.update(ix + 1)

    plt.figure()
    plt.plot(ns, no_parity_rate_array, label=f'No parity, ({trials} trials)', linewidth=2)
    plt.plot(ns, parity_1_rate_array, label=f'1-bit parity, ({trials} trials)', linewidth=1)
    plt.plot(ns, parity_2_rate_array, label=f'2-bit parity, ({trials} trials)', linewidth=0.7)
    plt.plot(ns, parity_4_rate_array, label=f'4-bit parity, ({trials} trials)', linewidth=0.4)
    plt.xlabel('n')
    plt.ylabel('Experimental False positive rate')
    plt.title('Fingerprinting: False Positive Rate, X/Y Parity Checked')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.plot(data_size_array, avg_no_parity_size_array, label=f'No parity, ({trials} trials)')
    plt.plot(data_size_array, avg_parity_1_size_array, label=f'1-bit parity, ({trials} trials)')
    plt.plot(data_size_array, avg_parity_2_size_array, label=f'2-bit parity, ({trials} trials)')
    plt.plot(data_size_array, avg_parity_4_size_array, label=f'4-bit parity, ({trials} trials)')
    plt.xlabel('data size of Y (bits)')
    plt.ylabel('Experimental Tranmission Size (bits)')
    plt.title('Fingerprinting: Transmission Size With Parity')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def run_remainder_experiment(n_min=6, n_max=1000, trials=10000):
    """
    This experiment shows what happens if Alice sent 1 extra bit with each "p" as the remainder of her "Y" value.
    The advesary ensures that Y and X both have a remainder of "0" by doubling the size of "Y". However, the adversary
    sometimes chooses less multiples of primes when forming this number to stay within the size constraints of 2**n
    :param n_min: smallest n value to run
    :param n_max: max n value to end at
    :param trials: for each n, average accross how many trials.
    :return: None
    """


    ns = list(range(n_min, n_max + 1))
    no_remainder_rate_array = []
    remainder_1_rate_array = []

    bar = progressbar.ProgressBar(max_value=len(ns))

    for ix, n in enumerate(ns):
        no_remainder_rate, remainder_1_rate = empirical_false_positive_remainder_experiment(
            n, trials)
        no_remainder_rate_array.append(no_remainder_rate)
        remainder_1_rate_array.append(remainder_1_rate)

        bar.update(ix + 1)

    plt.figure()
    plt.plot(ns, no_remainder_rate_array, label=f'Regular Fingerprinting, ({trials} trials)', linewidth=2)
    plt.plot(ns, remainder_1_rate_array, label=f'1-bit remainder added, ({trials} trials)', linewidth=1)
    plt.xlabel('n')
    plt.ylabel('Experimental False positive rate')
    plt.title('Fingerprinting: False Positive Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Part 1 & 2: plot theoretical and empirical false positive rates for n=6..1000
    # run_fingerprint_experiments()
    run_remainder_experiment()

