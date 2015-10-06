#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


class Graph(object):

    def __init__(self, vertices={}, directed=False):
        self.vertices = vertices
        self.directed = directed

    def add_vertex(self, vertex):
        if vertex not in self.vertices.keys():
            self.vertices[vertex] = set()

    def remove_vertex(self, vertex):
        if vertex in self.vertices.keys():
            for v in self.vertices:
                if vertex in self.vertices[v]:
                    self.vertices[v].remove(vertex)
            del self.vertices[vertex]

    def connect_two_vertices(self, vert1, vert2):
        if vert1 and vert2 in self.vertices.keys():
            self.vertices[vert1].update(vert2)
            if not self.directed:
                self.vertices[vert2].update(vert1)

    def disconnect_two_vertices(self, vert1, vert2):
        self.vertices[vert1].remove(vert2)
        self.vertices[vert2].remove(vert1)

    def graph_order(self):
        return len(self.vertices)

    def get_vertices(self):
        return {v for v in self.vertices}

    def get_random_vertex(self):
        return random.choice(list(self.vertices.keys()))

    def get_vertex_predecessors(self, vertex):
        return {i for i in self.vertices if vertex in self.vertices[i]}

    def get_adjacent_vertices(self, vertex):
        return set(self.vertices[vertex])  # also sucessors

    def get_vertex_indegree(self, vertex):
        return len([i for i in self.vertices if vertex in self.vertices[i]])

    def get_vertex_degree(self, vertex):
        return len(self.get_adjacent_vertices(vertex))  # also outdegree

    def graph_regularity(self):
        rand_degree = self.get_vertex_degree(self.get_random_vertex())
        for v in self.vertices:
            if rand_degree != self.get_vertex_degree(v):
                return False
        return True

    def graph_completeness(self):
        max_degree = self.graph_order() - 1
        for v in self.vertices:
            if max_degree != self.get_vertex_degree(v):
                return False
        return True

    def transitive_closure(self, vertex, visited=set()):
        visited.add(vertex)
        for v in self.get_adjacent_vertices(vertex):
            if v not in visited:
                self.transitive_closure(v, visited)
        return visited

    def graph_connectivity(self):
        return (set(self.vertices.keys()) ==
                self.transitive_closure(self.get_random_vertex()))

    def is_tree(self):
        def check_cycles(v, act_v, before_v, visited=set()):
            if act_v in visited:
                return True
            visited.add(act_v)

            for adj in self.get_adjacent_vertices(act_v):
                if adj != before_v:
                    if check_cycles(v, adj, act_v, visited):
                        return True

            visited - {act_v}
            return False

        v = self.get_random_vertex()
        return self.graph_connectivity() and not check_cycles(v, v, v)
