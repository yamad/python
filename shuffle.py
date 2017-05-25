from random import randint

def knuth_shuffle(arr):
    """Knuth-Fisher-Yates shuffle. see Knuth, TAOCP vol 2, Algorithm P
    invariant: items j->len(arr) are shuffled

    intuition: in each iteration, a randomly selected item from
    arr[0:j] is added to shuffled array
    """
    for j in range(len(arr) - 1, 1, -1):
        k = randint(0, j)
        arr[j], arr[k] = arr[k], arr[j]
    return arr

def main():
    ls = [x for x in range(10)]
    return knuth_shuffle(ls)

if __name__ == '__main__':
    main()
