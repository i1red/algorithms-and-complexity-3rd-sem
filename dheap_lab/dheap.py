class DHeap:
    def __init__(self, d):
        self.heap = [6, 7, 8, 9, 9, 7, 8, 9]
        self.d = d

    def _emersion(self, i):
        p = (i - 1) // self.d
        while i > 0 and self.heap[p] > self.heap[i]:
            self.heap[p], self.heap[i] = self.heap[i], self.heap[p]
            i = p
            p = (i - 1) // self.d

    def _min_child(self, i):
        if i * self.d + 1 >= len(self.heap):
            return 0

        s = i * self.d + 1
        min_key = self.heap[s]
        last = (i + 1) * self.d

        if last >= len(self.heap):
            last = len(self.heap) - 1

        for j in range(s + 1, last + 1):
            if self.heap[j] < min_key:
                min_key, s = self.heap[j], j

        return s

    def _immersion(self, i):
        s = self._min_child(i)
        while s > 0 and self.heap[i] > self.heap[s]:
            self.heap[i], self.heap[s] = self.heap[s], self.heap[i]
            i = s
            s = self._min_child(i)

    def insert(self, value):
        self.heap.append(value)
        self._emersion(len(self.heap) - 1)

    def pop(self, i):
        self.heap[i] = self.heap[-1]
        self.heap.pop()
        if i > 0 and self.heap[i] < self.heap[(i - 1) // self.d]:
            self._emersion(i)
        else:
            self._immersion(i)

    def decrease_key(self, i, k):
        self.heap[i] -= k
        self._emersion(i)

    def _heapify(self):
        for i in range((len(self.heap) - 1) // self.d, -1, -1):
            self._immersion(i)

a = DHeap(3)
a.decrease_key(2, 3)
print(a.heap)
import random
random.shuffle(a.heap)
a._heapify()
print(a.heap)