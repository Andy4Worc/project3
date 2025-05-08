#CS 5080
#project 3 - code used in deliverable 1
#5/4/2025

#Author: Anderson (Andy) Worcester, with a minor function here
"""
Plan:
Implement 3 ECCs:
1. Add one bit parity at the end of the fingerprint sent that is based on "Y"s parity, not the parity of the
2. Add 2 and 4 bit parity at the end of the fingerprint sent.
Make examples and visually check results.

Analyze to see "what" the attacker/adversary should do differently to try to spoof it.
Ans: the attacker could pick "Y" to have a parity of 1s % 16 = 0. However, I don't need to
  implement this to prove the adversary could do well here....

Doing "remainder" would be a stronger attack than parity bits. The adversary wants to pick "Y" to be an odd
  number. However, sending the remainder bit would force the adversary against this, greatly weakening its approach.

"""

def count_bits(n):
  count = 0
  while n:
    n = n >> 1
    count += 1
  return count

def count_set_bits(n):
  """Counts the number of set bits (1s) in an integer.

  Args:
    n: The integer to count set bits in.

  Returns:
    The number of set bits in n.

  Author: this function written by chatGPT
  """
  count = 0
  while n:
    n &= (n - 1)
    count += 1
  return count


# For "Adversary-Alice" to use:

def build_one_bit_ECC(hash, y) -> int:
    bits = count_set_bits(y)
    parity = bits % 2

    return hash * 2 + parity

def build_two_bit_ECC(hash, y) -> int:
    bits = count_set_bits(y)
    parity = bits % 4

    return hash * 4 + parity

def build_four_bit_ECC(hash, y) -> int:
    bits = count_set_bits(y)
    parity = bits % 16

    return hash * 16 + parity


# For Bob to use:

def decode_one_bit_ECC(parity_hash) -> (int, int):
    parity = parity_hash  % 2 #extracting last bit
    remaining_hash = parity_hash >> 1

    return remaining_hash, parity

def decode_two_bit_ECC(parity_hash) -> (int, int):
    parity = parity_hash  % 4 #extracting last bit2
    remaining_hash = parity_hash >> 2

    return remaining_hash, parity

def decode_four_bit_ECC(parity_hash) -> (int, int):
    parity = parity_hash  % 16 #extracting last bit2
    remaining_hash = parity_hash >> 4

    return remaining_hash, parity


# test:
if __name__ == '__main__':
    print("ECC parity encode/decode test")

    print("\nnumbers to test - actual and / length:")

    print("nums shown:", 0, " ", 225, ", and lengths: ", count_bits(0), count_bits(225))
    print("nums shown:", 11, " ", 225, ", and lengths: ", count_bits(11), count_bits(225))
    print("nums shown:", 15, " ", 225, ", and lengths: ", count_bits(15), count_bits(225))
    print("nums shown:", 16, " ", 225, ", and lengths: ", count_bits(16), count_bits(225))
    print("nums shown:", 15, " ", 241, ", and lengths: ", count_bits(15), count_bits(241))
    print("nums shown:", 16, " ", 241, ", and lengths: ", count_bits(16), count_bits(241))

    print("\nnumbers to test - encoded actual and / lengths:")

    print("encoded num %d, with encoded length %d", build_one_bit_ECC(0, 225), count_bits(build_one_bit_ECC(0, 225)))
    print("encoded num %d, with encoded length %d", build_one_bit_ECC(11, 225), count_bits(build_one_bit_ECC(11, 225)))
    print("encoded num %d, with encoded length %d", build_one_bit_ECC(15, 225), count_bits(build_one_bit_ECC(15, 225)))
    print("encoded num %d, with encoded length %d", build_one_bit_ECC(16, 225), count_bits(build_one_bit_ECC(16, 225)))
    print("encoded num %d, with encoded length %d", build_one_bit_ECC(15, 241), count_bits(build_one_bit_ECC(15, 241)))
    print("encoded num %d, with encoded length %d", build_one_bit_ECC(16, 241), count_bits(build_one_bit_ECC(16, 241)))

    print("encoded num %d, with encoded length %d", build_two_bit_ECC(0, 225), count_bits(build_two_bit_ECC(0, 225)))
    print("encoded num %d, with encoded length %d", build_two_bit_ECC(11, 225), count_bits(build_two_bit_ECC(11, 225)))
    print("encoded num %d, with encoded length %d", build_two_bit_ECC(15, 225), count_bits(build_two_bit_ECC(15, 225)))
    print("encoded num %d, with encoded length %d", build_two_bit_ECC(16, 225), count_bits(build_two_bit_ECC(16, 225)))
    print("encoded num %d, with encoded length %d", build_two_bit_ECC(15, 241), count_bits(build_two_bit_ECC(15, 241)))
    print("encoded num %d, with encoded length %d", build_two_bit_ECC(16, 241), count_bits(build_two_bit_ECC(16, 241)))


    print("\nnumbers to test - decoded actual and / lengths:")

    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(0, 225))[0], count_bits(decode_two_bit_ECC(build_two_bit_ECC(0, 225))[0]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(11, 225))[0], count_bits(decode_two_bit_ECC(build_two_bit_ECC(11, 225))[0]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(15, 225))[0], count_bits(decode_two_bit_ECC(build_two_bit_ECC(15, 225))[0]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(16, 225))[0], count_bits(decode_two_bit_ECC(build_two_bit_ECC(16, 225))[0]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(15, 241))[0], count_bits(decode_two_bit_ECC(build_two_bit_ECC(15, 241))[0]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(16, 241))[0], count_bits(decode_two_bit_ECC(build_two_bit_ECC(16, 241))[0]))

    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(0, 225))[1], count_bits(decode_two_bit_ECC(build_two_bit_ECC(0, 225))[1]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(11, 225))[1], count_bits(decode_two_bit_ECC(build_two_bit_ECC(11, 225))[1]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(15, 225))[1], count_bits(decode_two_bit_ECC(build_two_bit_ECC(15, 225))[1]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(16, 225))[1], count_bits(decode_two_bit_ECC(build_two_bit_ECC(16, 225))[1]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(15, 241))[1], count_bits(decode_two_bit_ECC(build_two_bit_ECC(15, 241))[1]))
    print("encoded num %d, with encoded length %d", decode_two_bit_ECC(build_two_bit_ECC(16, 241))[1], count_bits(decode_two_bit_ECC(build_two_bit_ECC(16, 241))[1]))