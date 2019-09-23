import reprlib

class Node:
    def __init__(self, priority, obj):
        self.priority = priority
        self.obj = obj
        self.lt = None
        self.rt = None


def preorder(cur: Node):
    if cur is not None:
        yield from preorder(cur.lt)
        yield (cur.priority, cur.obj)
        yield from preorder(cur.rt)


class PriorityQueueBST:
    def __init__(self, seq=None):
        self._root = None
        self._length = 0
        if seq is not None:
            for pair in seq:
                self.append(*pair)

    def __len__(self):
        return self._length


    def __bool__(self):
        return bool(len(self))


    def __eq__(self, other):
        if len(self) != len(other):
            return False

        return list(preorder(self._root)) == list(preorder(other._root))


    def __iter__(self):
        return preorder(self._root)

    def __repr__(self):
        if self._root is None:
            return 'PriorityQueueBST()'

        return f'PriorityQueueBST({reprlib.repr(list(iter(self)))})'


    def append(self, priority, obj):
        if self._root is None:
            self._root = Node(priority, obj)
        else:
            tmp = self._root

            while True:
                if tmp.priority > priority:
                    if tmp.lt is None:
                        tmp.lt = Node(priority, obj)
                        break
                    tmp = tmp.lt
                else:
                    if tmp.rt is None:
                        tmp.rt = Node(priority, obj)
                        break
                    tmp = tmp.rt

        self._length += 1


    def pop(self):
        if self._root is None:
            raise LookupError("Can't pop from empty queue")

        pair = None

        if self._root.lt is None:
            pair = (self._root.priority, self._root.obj)
            self._root = self._root.rt
        else:
            tmp, prev = self._root, None
            while tmp.lt is not None:
                prev, tmp = tmp, tmp.lt

            pair = (tmp.priority, tmp.obj)
            prev.lt = tmp.rt

        self._length -= 1

        return pair


class ListNode:
    def __init__(self, pair, nx=None):
        self.pair = pair
        self.nx = nx


class PriorityQueueList:
    def __init__(self, seq=None):
        self._head = None
        self._tail = None
        self._length = 0
        if seq is not None:
            for pair in seq:
                self.append(*pair)


    def __len__(self):
        return self._length


    def __bool__(self):
        return bool(len(self))


    def __eq__(self, other):
        if len(self) != len(other):
            return False

        tmp_self, tmp_other = self._head, other._head
        while tmp_self is not None:
            if tmp_self.pair != tmp_other.pair:
                return False
            tmp_self, tmp_other = tmp_self.nx, tmp_other.nx

        return True


    def __iter__(self):
        tmp = self._head
        while tmp is not None:
            yield tmp.pair
            tmp = tmp.nx


    def __repr__ (self):
        if self._head is None:
            return 'PriorityQueueList()'

        return f'PriorityQueueList({reprlib.repr(list(iter(self)))})'


    def append(self, prirority, obj):
        if self._head is None:
            self._head = ListNode((prirority, obj))
        elif self._head.pair[0] > prirority:
            tmp = ListNode((prirority, obj), self._head)
            self._head = tmp
        else:
            tmp = self._head
            while tmp.nx is not None and tmp.nx.pair[0] <= prirority:
                tmp = tmp.nx
            tmp.nx = ListNode((prirority, obj), tmp.nx)

        self._length += 1


    def pop(self):
        if self._head is None:
            raise LookupError("Can't pop from empty queue")

        pair = self._head.pair
        self._head = self._head.nx
        self._length -= 1
        return pair
