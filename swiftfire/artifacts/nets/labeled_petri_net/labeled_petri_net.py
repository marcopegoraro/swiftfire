from swiftfire.artifacts.nets.petri_net.petri_net import PetriNet

class LabeledPetriNet(PetriNet):

    def add_place(self, **kwds):
        kwds['type'] = 0
        self.__graph.add_node(**kwds)
        self.__places.append(len(self.__graph.vs))

    def add_transition(self, **kwds):
        kwds['type'] = 1
        self.__graph.add_node(**kwds)
        self.__transitions.append(len(self.__graph.vs))

    def add_edge(self, source, target, **kwds):
        self.__graph.add_edge(source, target, **kwds)
