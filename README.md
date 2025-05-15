# README

_CS 5080_\
_Spring 2025_\
_Author: Anderson Worcester_

## Project 3

NOTE: that to save the plots of either deliverable, I used the snipping tool as each plot appeared. I am not
"saving" the plot as an image in the scripts themselves.

### Deliverable 1

**Explanation:**

This explores the Fingerprinting problem with experiments on attempting to increase its defense
compared to the original problem as presented in class. I was able to at least partially do so in these 2
experiments. Although the effectiveness is limited as discussed further in the report.

**Files:**
- `ECC_test.py`: Here, I wrote some utility functions for computing and de-computing parity, counting the number of
  bits within a number, etc....
- `fingerprinting_setup.py`: Here, I wrote the main part of the code that sets up the binary representations of
  the strings that are to be compared, using prime numbers and ranges based on _n_. This also runs both experiments. 


**How to run:**

Run `fingerprinting_setup.py` script after installing dependencies (just the modules that are imported).

### Deliverable 2

**Explanation:**

This explores the Miller-Rabin Primality Test. I explore 3 experiments all revolving around the effectiveness of the
"A" bases chosen for the algorithm when determining if a number is a Strong Probable Prime or not.
I explore liars as well. Ultimately I am pleased with how effective the algorithm is at being nearly deterministic and is
usually quite far from its worst case false positive rate. The experiments and results are detailed further in the
report.

**Files:**
- `Deliverable_2.py`: Here, I run all 3 experiments using Miller Rabin base code. I also am using the Sieve of
Eratosthenes to determine fully deterministically whether a given number is prime or not.

**How to run:**

Run `Deliverable_2.py` script after installing dependencies (just the modules that are imported).
