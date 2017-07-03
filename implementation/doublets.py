#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heapq import heappop, heappush
from re import compile as recomp
from sys import argv


def search(start, finish, words):

    def heuristic(word):
        return sum(x[0] == x[1] for x in zip(word, finish))

    def neighbours(word):
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        changes = {l + c + r[1:] for l, r in splits if r for c in letters}
        return changes.intersection(words)

    queue = [(heuristic(start), [start], start)]
    visited = set([start])
    split_table = dict()

    while queue:
        cost, path, curr = heappop(queue)
        visited.add(curr)
        cost -= heuristic(curr)

        if curr == finish:
            return path

        for n in neighbours(curr):
            if n not in visited:
                visited.add(n)
                heappush(queue, (cost + heuristic(n) + 1, path + [n], n))

    return ["No path found!"]


if __name__ == '__main__':
    assert len(argv) == 4, "Usage: {} dictfile word1 word2".format(argv[0])
    name, fp, start, end = argv
    assert len(start) == len(end), "Length of words must be equal!"

    regex = recomp(r'\b[a-z]{{{}}}\b'.format(str(len(end))))
    words = set(regex.findall(open(fp).read()))

    print(" -> ".join(search(start.lower(), end.lower(), words)))
