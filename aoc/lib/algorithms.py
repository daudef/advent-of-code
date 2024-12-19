import typing


def binary_search(n_elem: int, key: typing.Callable[[int], int]):
    """Return the index of a searched element in a sorted indexed structure.

    the key takes an integer index and return a negative number, 0 or a positive number respectivly
    if the value of the index is greater equal or less then the searched value.
    """
    left = 0
    right = n_elem
    while left < right:
        mid = (left + right) // 2
        direction = key(mid)
        if direction < 0:
            right = mid
        elif direction > 0:
            left = mid + 1
        else:
            return mid
    return left
