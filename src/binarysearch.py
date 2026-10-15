import time


# ------------------------------------------------------------
# Search functions (both work on lists sorted from biggest to smallest)
# Both return the position of the FIRST match, or -1 if not found.
# ------------------------------------------------------------


def direction(card, target, mid):
    """Decide what to do with the middle slot: 'Found', 'Left' or 'Right'."""
    midcard = card[mid]
    if midcard == target:
        # a match, but if the slot before it is also a match, keep going left
        if mid - 1 >= 0 and card[mid - 1] == target:
            return "Left"
        return "Found"
    elif midcard < target:
        return "Left"
    else:
        return "Right"


def binary(card, target, show_steps=False):
    start, end = 0, len(card) - 1

    while start <= end:
        mid = (start + end) // 2
        if show_steps:
            print("Start:", start, "| End:", end)

        result = direction(card, target, mid)
        if result == "Found":
            return mid
        elif result == "Left":
            end = mid - 1
        else:
            start = mid + 1
    return -1


def linear(card, target):
    for i in range(len(card)):
        if card[i] == target:
            return i
    return -1


def timed(func, *args):
    """Run func(*args) and return (result, time in milliseconds)."""
    start = time.perf_counter()
    result = func(*args)
    return result, (time.perf_counter() - start) * 1000


# ------------------------------------------------------------
# Test cases: (list, target, expected position)
# ------------------------------------------------------------

tests = [
    ([13, 11, 10, 7, 4, 3, 1, 0], 7, 3),
    ([6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1], 4, 3),   # duplicates: first 4 is at 3
    ([6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1], 6, 0),   # first element
    ([6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1], 1, 10),  # first of the last group
    ([6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1], 5, -1),  # not in the list
    ([], 3, -1),                                         # empty list
]

for number, (card, target, expected) in enumerate(tests, start=1):
    lin, bin_ = linear(card, target), binary(card, target)
    status = "PASS" if lin == bin_ == expected else "FAIL"
    print(f"Test {number}: expected {expected}, linear {lin}, binary {bin_}  {status}")


# ------------------------------------------------------------
# Timing on a big list
# ------------------------------------------------------------

big = list(range(1_000_000, 0, -1))  # 1000000, 999999, ... 3, 2, 1
query = 1                             # at the very end (worst case for linear)

linearOutput, linearTime = timed(linear, big, query)
binaryOutput, binaryTime = timed(binary, big, query)

print()
print(f"Linear: position {linearOutput}, {linearTime:.4f} ms")
print(f"Binary: position {binaryOutput}, {binaryTime:.4f} ms")