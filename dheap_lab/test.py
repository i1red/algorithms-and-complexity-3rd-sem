import math

class DHeap:
    def __init__(self, max_dgr, keys=None):
        self.max_dgr = max_dgr
        if keys is None:
            self.heap = []
        else:
            self.heap = []
            for i in keys:
                self.insert(i)

    def __repr__(self):
        return f'DHeap({self.max_dgr}, {self.heap})'

    def print(self):
        lvl = 0
        height = math.ceil(math.log(len(self.heap), self.max_dgr))
        i = 1
        j = 0
        while j < len(self.heap):
            while j < len(self.heap) and j < i:
                print(f"{' ' * ((height - lvl - 1) ** self.max_dgr)}", end='')
                print(self.heap[j], end=' ')
                j += 1
            print()
            lvl += 1
            i += self.max_dgr ** lvl

    def _heapify(self):
        for i in range((len(self.heap) - 1) // self.max_dgr, -1, -1):
            self._immersion(i)

    def _emersion(self, index):
        prev = (index - 1) // self.max_dgr
        while index > 0 and self.heap[prev] < self.heap[index]:
            self.heap[prev], self.heap[index] = self.heap[index], self.heap[prev]
            index = prev
            prev = (index - 1) // self.max_dgr

    def _immersion(self, index):
        nx = self._max_child(index)
        while nx > 0 and self.heap[nx] < self.heap[index]:
            self.heap[nx], self.heap[index] = self.heap[index], self.heap[nx]
            index = nx
            nx = self._max_child(index)

    def _max_child(self, index):
        nx = index * self.max_dgr + 1
        if nx >= len(self.heap):
            return 0

        max_key = self.heap[nx]
        last = (index + 1) * self.max_dgr
        if last >= len(self.heap):
            last = len(self.heap) - 1

        for i in range(nx + 1, last + 1):
            if self.heap[i] > max_key:
                max_key, nx = self.heap[i], i

        return nx

    def extract_max(self):
        max = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._immersion(0)
        return max

    def insert(self, key):
        self.heap.append(key)
        self._emersion(len(self.heap) - 1)

    def increase_key(self, index, value):
        self.heap[index] += value
        self._emersion(index)


a = DHeap(2, [-15, 232, 19, 5, 87, 2, 48, 92])
print(a)
a.print()

