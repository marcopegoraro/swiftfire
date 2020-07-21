from typing import List, Iterable, Tuple
from igraph import Graph


class SwiftFireGraph(Graph):
    """
    Class defining a directed bipartite graph extended from the Graph class of the igraph package.
    """

    def __init__(self, node_types: List[int], arcs: Iterable[Tuple[int, int]]):
        """
        Constructor for the directed bipartite graph defined by the SwiftFireGraph class.
        :param node_types: list of integers, identifying the two partitions of nodes
        :type node_types: list of integers (either 0s or 1s)
        :param arcs: list of arcs of the graph (pairs of node ids)
        :type arcs: iterable of 2-uples of integers
        """
        for arc in arcs:
            if node_types[arc[0]] == node_types[arc[1]]:
                raise ValueError('Arc connecting two places or two transitions.')
        if isinstance(arcs, list):
            super().__init__(len(node_types), arcs, directed=True)
        else:
            super().__init__(len(node_types), list(arcs), directed=True)
        self.vs['type'] = node_types
        self.__nodes = self.vs
        self.__arcs = self.es

    def __get_nodes(self):
        return self.__nodes

    def __set_nodes(self, nodes):
        self.__nodes = nodes

    def __get_arcs(self):
        return self.__arcs

    def __set_arcs(self, arcs):
        self.__arcs = arcs

    nodes = property(__get_nodes, __set_nodes)
    arcs = property(__get_arcs, __set_arcs)
