'''
Problem 3a
'''

class Node:
    def __init__(self, val:int, next):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self):
        self.root = None

    def insert(self, x):
        node = Node(x, None)
        # empty
        if self.root is None:
            self.root = node
            return
        # insert at beginning
        if self.root.val > x:
            node.next = self.root
            self.root = node
            return
        ptr = self.root
        while ptr.next is not None and ptr.next.val < x:
            ptr = ptr.next
        node.next = ptr.next
        ptr.next = node

    def search(self, x):
        ptr = self.root
        while ptr is not None:
            if ptr.val == x:
                return ptr
            ptr = ptr.next
        return None

    def delete(self, x):
        # empty
        if self.root is None:
            return
        # head
        if self.root.val == x:
            self.root = self.root.next
            return
        ptr = self.root
        while ptr.next is not None:
            if ptr.next.val == x:
                ptr.next = ptr.next.next
                return
            ptr = ptr.next
