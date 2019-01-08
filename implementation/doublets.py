#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""doublets.py

Doublets is a word puzzle invented by Lewis Carroll, of Alice in Wonderland
fame. Given a language L and two words `w1` and `w2`, both in L, one must
connect these through a series of small changes to each word, consisting of
just one letter, such that these middle words are also in L.

This problem can be modeled as an undirected graph where vertices are words
and edges are the one letter changes between each pair of words. Hence, to
solve the proposed problem, it suffices to use Dijkstra's algorithm to find
one of the smallest paths between the two given nodes.
"""

from __future__ import absolute_import
from heapq import heappop, heappush
from re import compile as recomp
from sys import argv


def search(start, finish, words):
    """
    A Dijkstra's algorithm implementation using a min-priority queue.

    Args:
        start:  a string denoting `w1`.
        finish: a string denoting `w2`.
        words:  a list of all words in L.

    Returns:
        A list of strings representing a path between `start` and `finish`.
    """

    def heuristic(word):
        """
        Metric that measures if two words are close enough.

        Args:
            word:   a string.

        Returns:
            An integer that represents how many times the same
            letter is in the same position in both words.
        """
        return sum(x[0] == x[1] for x in zip(word, finish))

    def neighbours(word):
        """
        Constructs all valid words that can be reached from another word.

        Args:
            word:   a string.

        Returns:
            A set of words inside a given dictionary that may be produced
            from another word using only one letter change.
        """
        letters = "abcdefghijklmnopqrstuvwxyz"
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        changes = {l + c + r[1:] for l, r in splits if r for c in letters}
        return changes.intersection(words)

    queue = [(heuristic(start), [start], start)]
    visited = set([start])

    while queue:
        cost, path, curr = heappop(queue)
        visited.add(curr)
        cost -= heuristic(curr)

        if curr == finish:
            return path

        for node in neighbours(curr):
            if node not in visited:
                visited.add(node)
                elem = (cost + heuristic(node) + 1, path + [node], node)
                heappush(queue, elem)

    return ["No path found!"]


def main():
    """Parses arguments and executes the program."""
    assert len(argv) == 4, "Usage: {} dictfile word1 word2".format(argv[0])
    start, end = argv[2], argv[3]
    assert len(start) == len(end), "Length of words must be equal!"

    regex = recomp(r"\b[a-z]{{{}}}\b".format(str(len(end))))
    words = set(regex.findall(open(argv[1]).read()))

    print(" -> ".join(search(start.lower(), end.lower(), words)))


if __name__ == "__main__":
    main()
