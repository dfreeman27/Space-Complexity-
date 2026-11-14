import random
import time


def reverse_string(s):
    """Return s reversed.

    Space: O(n). Slicing builds a new string with n characters.
    """
    return s[::-1]


def count_letters(text):
    """Return a dict mapping each character in text to its frequency.

    Space: O(k), where k is the number of UNIQUE characters in the input.
    The dictionary gets one entry per distinct character, so it grows with
    k, not with the length of the text. Repeating the same characters a
    million times adds no new keys. k <= n, and for ASCII k is capped at
    128, so it is small in practice. With full Unicode, k can be much
    larger.
    """
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def matrix_identity(n):
    """Return the n x n identity matrix as a list of lists.

    Space: O(n^2). The function builds n lists, each holding n integers,
    so it stores n * n = n^2 values. Doubling n quadruples the number of
    stored elements. (Setting the diagonal adds no storage, since it only
    overwrites entries that already exist.)
    """
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
    return matrix


def running_sum(numbers):
    """Return the total of all numbers.

    Space: O(1). Only a single accumulator (`total`) is stored, no matter
    how many numbers are processed.
    """
    total = 0
    for x in numbers:
        total += x
    return total


random.seed(42)
domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
unique_emails = [f"user{i}@{domains[i % len(domains)]}" for i in range(8_000)]
_dupes        = random.choices(unique_emails, k=2_000)
all_emails    = unique_emails + _dupes
random.shuffle(all_emails)
NUM_EMAILS = len(all_emails)


def find_duplicates_set(emails):
    """Return a set of email addresses that appear more than once.

    Time: O(n) on average (single pass).
    Space: O(u) extra space, where u is the number of UNIQUE email
    addresses encountered (not the total number processed, n).
    `seen` grows to at most u entries; `duplicates` grows to at most
    d entries (d = number of unique addresses that repeat, d <= u).
    Feeding this the same u addresses many more times (larger n)
    would not grow memory use, since u stays fixed.
    """
    seen = set()
    duplicates = set()

    for email in emails:
        if email in seen:
            duplicates.add(email)
        else:
            seen.add(email)
    return duplicates


def find_duplicates_sort(emails):
    """Return a set of email addresses that appear more than once.

    Time: O(n log n), dominated by the sort.
    Space: O(n) extra space, NOT O(1). sorted() always allocates a
    new list holding references to all n input elements -- it never
    sorts in place -- so `sorted_emails` alone costs O(n). On top of
    that, `duplicates` costs O(d), where d is the number of unique
    duplicate keys found (d <= n). Using emails.sort() (in place) would
    use less memory, but it mutates the caller's list and CPython's
    sort still allocates temporary merge space, so it is not true O(1).
    """
    sorted_emails = sorted(emails)
    duplicates = set()

    for i in range(1, len(sorted_emails)):
        if sorted_emails[i] == sorted_emails[i - 1]:
            duplicates.add(sorted_emails[i])
    return duplicates


def benchmark(func, data, label, repeats=5):
    """Return (result, best time in ms) over several runs."""
    best = float("inf")
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = func(data)
        best = min(best, (time.perf_counter() - start) * 1000)
    return result, best


if __name__ == "__main__":
    print("=" * 60)
    print(f"Duplicate Email Detection ({NUM_EMAILS:,} emails)")
    print("=" * 60)

    dupes_set,  t_set  = benchmark(find_duplicates_set,  all_emails, "set")
    dupes_sort, t_sort = benchmark(find_duplicates_sort, all_emails, "sort")

    print(f"  Set approach    : {len(dupes_set) if dupes_set is not None else 'not implemented':>5} duplicates  {t_set:.3f} ms")
    print(f"  Sort+scan       : {len(dupes_sort) if dupes_sort is not None else 'not implemented':>5} duplicates  {t_sort:.3f} ms")
    if dupes_set is not None and dupes_sort is not None:
        print(f"  Both agree      : {dupes_set == dupes_sort}")

    # ------------------------------------------------------------------
    # Tradeoff decision: sort-and-scan vs. set approach
    #
    # Rough memory estimates (10,000 emails, ~8,000 unique, ~1,770
    # distinct duplicated addresses). Container memory only; the string
    # objects themselves are shared by both approaches.
    #
    #   Sort-and-scan : ~80 KB (list of 10,000 pointers)
    #                   + ~130 KB (`duplicates` set)
    #                   = ~210 KB.  Time: O(n log n).
    #   Set approach  : ~520 KB (`seen` set, ~8,000 entries)
    #                   + ~130 KB (`duplicates` set)
    #                   = ~650 KB.  Time: O(n) average, single pass.
    #
    # Decision: if memory is the tighter constraint, use sort-and-scan
    # (about 3x less memory, at the cost of O(n log n) time). If speed
    # matters more, or n will grow large, use the set approach for
    # single-pass performance and accept ~440 KB of extra memory. At
    # 10,000 emails both costs are tiny, so the set approach is the
    # simpler and faster choice here.
    # ------------------------------------------------------------------
