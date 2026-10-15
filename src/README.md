# Binary Search: Locate the First Position of a Number

A study of searching a sorted list in Python: the problem, a plan, the code, the tests, and why binary search beats linear search.

---

## 1. The problem

You have a list of numbers **sorted from largest to smallest** (it may contain duplicates), like a row of cards laid out in decreasing order. Given a number to look for (the **target**), return the **position (index)** of its **first occurrence**. If the number isn't in the list, return `-1`.

Positions start at 0.

**Sample input and output**

| Input list | Target | Output |
|---|---|---|
| `[13, 11, 10, 7, 4, 3, 1, 0]` | `7` | `3` |
| `[6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1]` | `4` | `3` |

In the second row, the 4 appears at positions 3 and 4, and the answer is the first one: `3`.

---

## 2. Test inputs and expected outputs

Before writing code, I listed the cases a correct solution must handle:

| # | Situation | List | Target | Expected |
|---|---|---|---|---|
| 1 | Normal case | `[13, 11, 10, 7, 4, 3, 1, 0]` | `7` | `3` |
| 2 | Target is the first element | `[13, 11, 10, 7, 4, 3, 1, 0]` | `13` | `0` |
| 3 | Target is the last element | `[13, 11, 10, 7, 4, 3, 1, 0]` | `0` | `7` |
| 4 | Target is not in the list | `[13, 11, 10, 7, 4, 3, 1, 0]` | `5` | `-1` |
| 5 | Duplicates: must return the first | `[6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1]` | `4` | `3` |
| 6 | Duplicates at the very start | `[6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1]` | `6` | `0` |
| 7 | Duplicates at the very end | `[6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1]` | `1` | `10` |
| 8 | Empty list | `[]` | `3` | `-1` |
| 9 | One element, found | `[5]` | `5` | `0` |
| 10 | One element, not found | `[5]` | `4` | `-1` |
| 11 | All the same value | `[2, 2, 2, 2]` | `2` | `0` |

---

## 3. The idea, in plain English

The obvious approach is to check every number from the left until you find the target (linear search). But the list is **sorted**, which means one comparison can rule out half of the list.

1. Look at the **middle** number of the part of the list still in play.
2. **If it equals the target:** check the number just before it. If that is also the target, the first occurrence is further left, so keep going **left**. Otherwise, this is the first occurrence. **Done.**
3. **If it is smaller than the target:** the list goes from big to small, so the target must be on the **left**. Throw away the middle and everything on its right.
4. **If it is bigger than the target:** the target must be on the **right**. Throw away the middle and everything on its left.
5. Repeat. If nothing is left to search, the target is not in the list, so return `-1`.

**Worked example:** find `4` in `[6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1]`

| Round | Search range | Middle slot | Number there | Decision |
|---|---|---|---|---|
| 1 | positions 0 to 12 | 6 | 3 | 3 < 4, go **left** |
| 2 | positions 0 to 5 | 2 | 6 | 6 > 4, go **right** |
| 3 | positions 3 to 5 | 4 | 4 | match, but position 3 is also 4, go **left** |
| 4 | positions 3 to 3 | 3 | 4 | match, and position 2 is not 4. **Found at 3** |

---

## 4. The implementation

Full code: [`binarysearch.py`](binarysearch.py)

```python
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
```

Screenshot of the code and a test run:

![Code and results](Screenshot%202026-10-15%20092447.png)

---

## 5. Test cases and the things that needed fixing

All 11 cases from section 2 pass, and `linear` and `binary` give the same answer on each:

```
Test 1: expected 3, linear 3, binary 3  PASS
Test 2: expected 3, linear 3, binary 3  PASS
Test 3: expected 0, linear 0, binary 0  PASS
Test 4: expected 10, linear 10, binary 10  PASS
Test 5: expected -1, linear -1, binary -1  PASS
Test 6: expected -1, linear -1, binary -1  PASS
```

**Problems I found along the way, and how I fixed them**

| # | What was wrong | Why it mattered | Fix |
|---|---|---|---|
| 1 | The loop did `return mid - 1` or `return mid + 1` instead of shrinking the range | The search only ever looked at the middle once. It passed Test 1 by luck and gave wrong answers for `13`, `0` and `5` | Replace with `end = mid - 1` and `start = mid + 1` |
| 2 | One test list was **not sorted** (`[3, 3, 3, 4, 4, 6, 6, 6, 2, 2, 1, 1, 1]`) | Binary search only works on sorted data, so it returned `-1` for a number that was there | Use a properly sorted list: `[6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1]` |
| 3 | `linearOutput = print(...)` | `print` returns `None`, so the variable held nothing | Store the result and the time in separate variables |
| 4 | A `print` inside the loop while timing | Printing is much slower than the search, so it distorted the timing | Make it optional with `show_steps=False` |
| 5 | The helper was named `test` | `pytest` collects any function starting with `test`, which would confuse it later | Renamed to `direction` |

**Edge cases handled:** empty list, one element, target at either end, target missing, many duplicates.

---

## 6. Complexity analysis: linear search vs binary search

**Linear search** checks one number at a time from the left, so in the worst case it checks all `n` numbers: **O(n)** time, **O(1)** extra space.

**Binary search** halves what's left each round, so the number of rounds is about `log₂(n)`: **O(log n)** time, **O(1)** extra space.

| List size (n) | Linear search, worst case | Binary search, worst case |
|---|---|---|
| 1,000 | 1,000 checks | 10 rounds |
| 1,000,000 | 1,000,000 checks | 20 rounds |
| 1,000,000,000 | 1,000,000,000 checks | 30 rounds |

**The inefficiency in linear search:** it ignores the fact that the list is sorted. After comparing with one number, it learns almost nothing about the rest, so it must keep checking every slot.

---

## 7. How binary search overcomes it

Binary search uses the sorted order. One comparison at the middle tells it which half the target must be in, so the other half can be thrown away for good. A million numbers shrink like this:

1,000,000 → 500,000 → 250,000 → ... → 1, which takes **20 rounds**.

![Binary search on 1,000,000 numbers](Screenshot%202026-10-15%20094636.png)

**Measured result** (list of 1,000,000 numbers, target in the very last position, which is the worst case for linear search):

| Method | Time |
|---|---|
| Linear search | 39.6441 ms |
| Binary search | 0.0121 ms |

Binary search was roughly **3,000 times faster** on this run. A single timing like this is noisy, so the exact numbers will change from run to run, but the gap stays huge.

**Trade-offs to remember**
- Binary search only works if the list is **sorted**. Sorting an unsorted list first costs O(n log n), so it pays off when you search many times.
- For tiny lists, or when the target happens to be at the very front, linear search is just as good.

**Possible next steps:** the same idea with `lower_bound` / `upper_bound`, searching a rotated sorted list, and "binary search on the answer" problems.
