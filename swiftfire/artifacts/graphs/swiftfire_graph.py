from typing import Sequence, Iterable, Tuple, Union, Set
from itertools import repeat

from igraph import Graph


class SwiftFireGraph(Graph):
    """
    Class defining a directed bipartite graph extended from the Graph class of the igraph package.
    """

    def __init__(self, node_types: Sequence[int], arcs: Iterable[Tuple[int, int]]):
        """
        Constructor for the directed bipartite graph defined by the SwiftFireGraph class.
        :param node_types: sequence of integers, identifying the two partitions of nodes
        :type node_types: sequence of integers (either 0s or 1s)
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

    def __get_arcs(self):
        return self.__arcs

    nodes = property(__get_nodes)
    arcs = property(__get_arcs)

    # TODO: move here the definitions of neighbors on containers of nodes for the preset and postset methods of PetriNet

    def neighbors(self, input_value: Union[int, Iterable[int]], mode: str = 'all') -> Set[int]:
        """
        Overridden version of the neighbors function, which also works on iterables of nodes
        :param input_value: a node or an iterable of nodes
        :type input_value: integer or iterable of integers
        :param mode: the arc direction to use to fetch neighbors
        :type mode: string ('in', 'out' or 'all')
        :return: the set of neighbors in the graph of the given node(s)
        :rtype: set of integers
        """
        if isinstance(input_value, int):
            return set(super().neighbors(input_value, mode=mode))
        else:
            global_postset = set()
            # Efficient equivalent of:
            # for postset in [self.__graph.neighbors(node, mode='out') for node in input_value]
            for postset in map(self.neighbors, input_value, repeat(mode)):
                global_postset.update(postset)
            return global_postset
