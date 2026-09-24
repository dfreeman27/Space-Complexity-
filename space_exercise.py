
import random
import time


def reverse_string(s):
    return s[::-1]

def count_letters(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

def matrix_identity(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
    return matrix

def running_sum(numbers):
    total = 0
    for x in numbers:
        total += x
    return total

NUM_EMAILS = 10_000
random.seed(42)
domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
unique_emails = [f"user{i}@{domains[i % len(domains)]}" for i in range(8_000)]
_dupes        = random.choices(unique_emails, k=2_000)
all_emails    = unique_emails + _dupes
random.shuffle(all_emails)

def find_duplicates_set(emails):
    """Return a set of email addresses that appear more than once.

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

    Space: O(n) extra space, NOT O(1). sorted() always allocates a
    new list holding references to all n input elements -- it never
    sorts in place -- so `sorted_emails` alone costs O(n). On top of
    that, `duplicates` costs O(d), where d is the number of unique
    duplicate keys found (d <= n). True O(1) extra space would
    require emails.sort() (in-place, destructive) instead, and even
    then `duplicates` would still be O(d).
    """
    sorted_emails = sorted(emails)
    duplicates = set()

    for i in range(1, len(sorted_emails)):
        if sorted_emails[i] == sorted_emails[i - 1]:
            duplicates.add(sorted_emails[i])
    return duplicates


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

    # Rough memory notes (10,000 emails, ~8,000 unique, ~2,000 duplicates):
    #   Set approach : ~8,000 set entries (seen) + ~2,000 set entries
    #                  (duplicates), ~50-70 bytes/entry -> ~500-700 KB
    #   Sort approach: 10,000-element list of pointers (~8 bytes each,
    #                  ~80 KB) + ~2,000 set entries (~100-140 KB)
    #                  -> ~180-220 KB total
    # Despite O(u) "looking smaller" than O(n), the sort approach uses
    # less RAM here because a list of pointers is far cheaper per
    # element than a hash set's per-entry overhead.


