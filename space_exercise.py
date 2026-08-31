import random
import time


# ============================================================
# PART 1 — Classify Space Complexity
# For each function, fill in the Space O and explain why.
# ============================================================

def reverse_string(s):
    return s[::-1]
# TODO: What is the space complexity of reverse_string? Why?
# Space O: 0(n) Linear Space
# Reason: A new string is created.


def count_letters(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq
# TODO: What is the space complexity of count_letters? Why?
#       Hint: the dict grows based on how many UNIQUE characters appear.
# Space O: O(1)- Constant Space 
# Reason: There are only 2 variables.


def matrix_identity(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
    return matrix
# TODO: What is the space complexity of matrix_identity? Why?
# Space O: O(n2)- Quadratic Space
# Reason: The work multiplies based on input.


def running_sum(numbers):
    total = 0
    for x in numbers:
        total += x
    return total
# TODO: What is the space complexity of running_sum? Why?
#       Hint: how many variables does this function create, regardless of input size?
# Space O: O(1)-Constant Space
# Reason: There is no change in memory usage. It remains constant.


# ============================================================
# PART 2 — Duplicate Email Detection
# Implement both approaches, then answer the RAM question below.
# ============================================================

# --- Sample data ---
NUM_EMAILS = 10_000
random.seed(42)
domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
unique_emails = [f"user{i}@{domains[i % len(domains)]}" for i in range(8_000)]
_dupes        = random.choices(unique_emails, k=2_000)
all_emails    = unique_emails + _dupes
random.shuffle(all_emails)


# ---- Approach 1: Set-based -----------------------------------------------
# Time:  O(n)   — one pass; set add/lookup are O(1) average
# Space: O(n)   — the set can hold up to n email strings
def find_duplicates_set(emails):
    """Return a set of email addresses that appear more than once.

    Uses O(n) extra space (a 'seen' set + a 'duplicates' set).
    """
    # TODO: Implement using two sets: 'seen' and 'duplicates'.
    # Loop through emails once. If an email is already in 'seen', add it
    # to 'duplicates'. Otherwise add it to 'seen'. Return 'duplicates'.
    
    seen = set()
    duplicates = set()

    for email in emails:
        if email in seen:
            duplicates.add(email)
        else:
            seen.add(email)
    return duplicates


# ---- Approach 2: Sort-and-scan -------------------------------------------
# Time:  O(n log n) — dominated by the sort step
# Space: O(1) extra — no hash table, just scan adjacent sorted elements
def find_duplicates_sort(emails):
    """Return a set of email addresses that appear more than once.

    Uses O(1) extra space (beyond the sorted copy Python must create).
    """
    # TODO: Implement by:
    # 1. sorted_emails = sorted(emails)
    # 2. Loop from index 1 to the end.
    # 3. If sorted_emails[i] == sorted_emails[i - 1], it's a duplicate.
    # 4. Return a set of all duplicates found.
    
    sorted_emails = sorted(emails)
    duplicates = set()

    for i in range(1, len(sorted_emails)):
        if sorted_emails[i] == sorted_emails[i - 1]: 
            duplicates.add(sorted_emails[i])
    return duplicates 
    

# ============================================================
# TODO: Answer this question as a comment below.
# Which approach would you choose if you only had 4 GB of RAM?
# Which would you choose if you had 64 GB?
# Why?
# ============================================================
# 4 GB RAM  → I would choose 0(1) because with less RAM you have to prioritize space over speed.
# 64 GB RAM → I would choose 0(n) because you have enough RAM to that space wouldnt be an issue and you can focus on the time.


def benchmark(func, data, label):
    start = time.time()
    result = func(data)
    elapsed = (time.time() - start) * 1000
    return result, elapsed


if __name__ == "__main__":
    print("=" * 60)
    print(f"Duplicate Email Detection ({NUM_EMAILS:,} emails)")
    print("=" * 60)

    dupes_set,  t_set  = benchmark(find_duplicates_set,  all_emails, "set")
    dupes_sort, t_sort = benchmark(find_duplicates_sort, all_emails, "sort")

    print(f"  Set approach    : {len(dupes_set) if dupes_set else 'not implemented':>5} duplicates  {t_set:.3f} ms")
    print(f"  Sort+scan       : {len(dupes_sort) if dupes_sort else 'not implemented':>5} duplicates  {t_sort:.3f} ms")
    if dupes_set and dupes_sort:
        print(f"  Both agree      : {dupes_set == dupes_sort}")