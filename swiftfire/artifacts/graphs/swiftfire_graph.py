import igraph


class SwiftFireGraph(igraph.Graph.Bipartite):

    def __init__(self, node_types, arcs):
        super().__init__(node_types, arcs, directed=True)
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
