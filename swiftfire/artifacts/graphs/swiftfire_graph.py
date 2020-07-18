from igraph import Graph


class SwiftFireGraph(Graph):

    def __init__(self, node_types, arcs):
        for arc in arcs:
            if node_types[arc[0]] == node_types[arc[1]]:
                raise ValueError('Arc connecting two places or two transitions.')
        super().__init__(len(node_types), arcs, directed=True)
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
