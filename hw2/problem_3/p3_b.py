'''
Problem 3b
'''

import random

class Node: 
    def __init__(self, val, level):
        self.val = val
        self.next = [None] * level
        self.level = level

class SkipList:
    def __init__(self, max_level, p):
        self.max_level = max_level
        self.p = p
        self.sentinel = Node(None, self.max_level)
        self.root = None

    def insert(self, x: int) -> None:
        level = 1
        while random.random() < self.p:
            if level < self.max_level:
                level += 1
        new_node = Node(x, level)

        nodes_to_insert_after = [None] * self.max_level
        ptr = self.sentinel

        for i in reversed(range(self.max_level)):
            while ptr.next[i] is not None and ptr.next[i].val < x:
                ptr = ptr.next[i]
            nodes_to_insert_after[i] = ptr

        for i in range(level):
            new_node.next[i] = nodes_to_insert_after[i].next[i]
            nodes_to_insert_after[i].next[i] = new_node

        if self.root is None or x < self.root.val:
            self.root = self.sentinel.next[0]

    def delete(self, x: int) -> None:
        nodes_to_delete_after = [None] * self.max_level
        ptr = self.sentinel

        for i in reversed(range(self.max_level)):
            while ptr.next[i] is not None and ptr.next[i].val < x:
                ptr = ptr.next[i]
            nodes_to_delete_after[i] = ptr

        target = nodes_to_delete_after[0].next[0]
        if target is None or target.val != x:
            return

        for i in range(target.level):
            if nodes_to_delete_after[i].next[i] == target:
                nodes_to_delete_after[i].next[i] = target.next[i]

        if self.root is not None and self.root.val == x:
            self.root = self.sentinel.next[0]

    def search(self, x: int) -> Node:
        ptr = self.sentinel
        for i in reversed(range(self.max_level)):
            while ptr.next[i] is not None and ptr.next[i].val < x:
                ptr = ptr.next[i]
        ptr = ptr.next[0]
        if ptr is None:
            return None
        if ptr.val == x:
            return ptr
        return None
