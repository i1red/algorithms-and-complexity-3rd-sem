import random

class DHeap:
    def __init__(self, max_dgr, keys=None):
        self.max_dgr = max_dgr
        self.heap = [] if keys is None else keys
        self._heapify()

    def __repr__(self):
        return f'DHeap({self.max_dgr}, {self.heap})'

    def __bool__(self):
        return bool(len(self.heap))

    def _heapify(self):
        for i in range((len(self.heap) - 1) // self.max_dgr, -1, -1):
            self._immersion(i)

    def _emersion(self, index):
        prev = (index - 1) // self.max_dgr
        while index > 0 and self.heap[index] > self.heap[prev]:
            self.heap[prev], self.heap[index] = self.heap[index], self.heap[prev]
            index = prev
            prev = (index - 1) // self.max_dgr

    def _immersion(self, index):
        nx = self._max_child(index)
        while nx > 0 and self.heap[index] < self.heap[nx]:
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



def test_dheap():
    max_dgr = random.randint(2, 10)
    init_el_q = random.randint(1200, 2000)
    extractions_q = random.randint(100, 200)
    insertions_q = random.randint(100, 200)
    init_list = [random.randint(-500, 500) for _ in range(init_el_q)]
    print(f'TEST DHEAP: max_dgr={max_dgr}, init_el_q={init_el_q}, extractions_q={extractions_q}, insertions_q={insertions_q}')

    my_heap = DHeap(max_dgr, init_list)
    for _ in range(extractions_q):
        my_heap.extract_max()

    for _ in range(insertions_q):
        my_heap.insert(random.randint(-300, 300))

    res_list = []
    while my_heap:
        res_list.append(my_heap.extract_max())

    expected = sorted(res_list,reverse=True)
    print('OK' if res_list == expected else 'FAILED')


test_dheap()