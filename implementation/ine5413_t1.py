#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


class Graph(object):
    """A graph is a representation of a set of objects where some pairs of
    these are connected by links. The objects are called vertices, and the
    links are called edges.
    """

    def __init__(self, vertices={}, directed=False):
        """Initializes a graph object."""
        self.vertices = vertices
        self.directed = directed

    def add_vertex(self, vertex):
        """Adds a vertex to the graph."""
        if vertex not in self.vertices:
            self.vertices[vertex] = set()

    def remove_vertex(self, vertex):
        """Removes a vertex and every one of its edges from the graph."""
        if vertex in self.vertices:
            for v in self.vertices:
                if vertex in self.vertices[v]:
                    self.vertices[v].remove(vertex)
            del self.vertices[vertex]

    def connect_two_vertices(self, vert1, vert2):
        """Creates an edge between two vertices."""
        if vert1 in self.vertices and vert2 in self.vertices:
            self.vertices[vert1].update(vert2)
            if not self.directed:
                self.vertices[vert2].update(vert1)

    def disconnect_two_vertices(self, vert1, vert2):
        """Removes an edge between two vertices."""
        if vert1 in self.vertices and vert2 in self.vertices:
            self.vertices[vert1].remove(vert2)
            if not self.directed:
                self.vertices[vert2].remove(vert1)

    def graph_order(self):
        """The order of a graph is the number of its vertices."""
        return len(self.vertices)

    def get_vertices(self):
        """Returns a set with all the vertices in the graph."""
        return {v for v in self.vertices}

    def get_random_vertex(self):
        """Picks a random vertex from the available ones."""
        return random.choice(list(self.vertices.keys()))

    def get_vertex_predecessors(self, vertex):
        """In directed graphs, if a vertex is reachable from other vertices,
        then these are called predecessors of that vertex."""
        return {i for i in self.vertices if vertex in self.vertices[i]}

    def get_vertex_sucessors(self, vertex):
        """In directed graphs, the successors of a vertex are other vertices
        that can be reached from it."""
        return self.vertices[vertex]

    def get_adjacent_vertices(self, vertex):
        """Counts all vertices that are connected to a given vertex."""
        if self.directed:
            return (self.get_vertex_sucessors(vertex) |
                    self.get_vertex_predecessors(vertex))
        return self.vertices[vertex]

    def get_vertex_indegree(self, vertex):
        """In directed graphs, the indegree of a vertex is the number of
        vertices with edges that point to that vertex."""
        return len(self.get_vertex_predecessors(vertex))

    def get_vertex_outdegree(self, vertex):
        """In directed graphs, the outdegree of a vertex is the number of
        vertices that are reached from it."""
        return len(self.get_vertex_sucessors(vertex))

    def get_vertex_degree(self, vertex):
        """The degree of a vertex is the number of vertices it is connected
        to."""
        return len(self.get_adjacent_vertices(vertex))

    def graph_regularity(self):
        """A graph is regular iff all of its vertices have the same degree."""
        rand_degree = self.get_vertex_degree(self.get_random_vertex())
        for v in self.vertices:
            if rand_degree != self.get_vertex_degree(v):
                return False
        return True

    def graph_completeness(self):
        """A graph is complete if all pairs of vertices are connected through
        one unique edge (or two directed ones in the case of directed graphs).
        It is also called a k_n graph, where n is the order of the graph."""
        max_degree = self.graph_order() - 1
        for v in self.vertices:
            if max_degree != self.get_vertex_degree(v):
                return False
        return True

    def transitive_closure(self, vertex, visited=set()):
        """A transitive closure represents the set of all the vertices
        reachable directly or indirectly from a given vertex."""
        visited.add(vertex)
        for v in self.get_adjacent_vertices(vertex):
            if v not in visited:
                self.transitive_closure(v, visited)
        return visited

    def graph_connectivity(self):
        """A graph is connected iff there exists no unreachable vertices."""
        return (set(self.vertices.keys()) ==
                self.transitive_closure(self.get_random_vertex()))

    def is_tree(self):
        """A graph is a tree iff all the vertices are reachable through the
        minimum number of edges possible (the order of the graph minus one)."""

        def check_cycles(v, act_v, before_v, visited=set()):
            """A depth-first search algorithm (path searching in graphs where
            each branch is searched until its last child before backtracking)
            implementation to check for cycles in a graph."""
            if act_v in visited:
                return True

            visited.add(act_v)
            for adj in self.get_adjacent_vertices(act_v):
                if adj != before_v and check_cycles(v, adj, act_v, visited):
                        return True

            return False

        v = self.get_random_vertex()
        return self.graph_connectivity() and not check_cycles(v, v, v)
