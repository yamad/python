import unittest

class Heap:
    def __init__(self):
        self._heap = [None]     # don't use self._heap[0], makes arithmetic easier

    def __len__(self):
        return len(self._heap) - 1

    def __getitem__(self, index):
        return self._heap[index+1]

    def insert(self, key):
        self._heap.append(key)
        self._swim(len(self))

    def pop(self):
        if not len(self): return None
        h = self._heap
        maxV = h[1]
        h[1], h[-1] = h[-1], h[1]
        self._heap = self._heap[:-1]         # chop last value
        self._sink(1)
        return maxV

    def _sink(self, i):
        h = self._heap
        N = len(self)
        while (2*i <= N):
            j = 2*i
            if (j < N and not self.compare(j, j+1)):
                j += 1
            if self.compare(i, j):
                break

            h[i], h[j] = h[j], h[i]
            i = j

    def _swim(self, i):
        h = self._heap
        while (i > 1):
            j = self._parent(i)
            if self.compare(i, j):
                h[j], h[i] = h[i], h[j]
            i = j

    def _parent(self, i):
        return i // 2

    def _leftchild(self, i):
        return 2*i

    def _rightchild(self, i):
        return 2*i + 1

    def compare(self, a, b):
        # by arbitrary default, Heap is a min priority queue
        return self._heap[a] < self._heap[b]

    def __iter__(self):
        while len(self):
            yield self.pop()

class TestHeap(unittest.TestCase):
    def test_length(self):
        h = Heap()
        self.assertEqual(len(h), 0)
        h.insert("A")
        self.assertEqual(len(h), 1)

    def test_swim(self):
        h = Heap()
        h.insert("D")
        h.insert("A")
        self.assertEqual(h[0], "A")

    def test_pop(self):
        h = Heap()
        h.insert("D")
        h.insert("A")
        h.insert("C")
        h.insert("B")
        a = h.pop()
        self.assertEqual(a, "A")

    def test_generator(self):
        import random
        h = Heap()
        input = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # push onto heap in shuffled order
        shuf = list(input)
        random.shuffle(shuf)
        self.assertNotEqual(input, ''.join(shuf))
        for c in shuf:
            h.insert(c)

        # should pop off head in sorted order
        res = []
        for c in h:
            res.append(c)
        self.assertEqual(input, ''.join(res))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
