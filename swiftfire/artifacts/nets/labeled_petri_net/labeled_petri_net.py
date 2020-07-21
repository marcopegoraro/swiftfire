from typing import Any

from swiftfire.artifacts.nets.petri_net.petri_net import PetriNet


class LabeledPetriNet(PetriNet):
    """
    Class defining a labeled Petri net.
    """

    def add_place(self, **kwds: Any):
        """
        Adds a place to the labeled Petri net.
        :param kwds: Arbitrary keyword arguments
        :type kwds: keyword-value couples
        :return: None
        :rtype: NoneType
        """
        kwds['type'] = 0
        self.__graph.add_node(**kwds)
        self.__places.append(len(self.__graph.vs))

    def add_transition(self, **kwds: Any):
        """
        Adds a transition to the labeled Petri net.
        :param kwds: Arbitrary keyword arguments
        :type kwds: keyword-value couples
        :return: None
        :rtype: NoneType
        """
        kwds['type'] = 1
        self.__graph.add_node(**kwds)
        self.__transitions.append(len(self.__graph.vs))

    def add_arc(self, source: int, target: int, **kwds: Any):
        """
        Adds an arc to the labeled Petri net.
        :param source: the source node of the arc
        :type source: integer
        :param target: the source node of the arc
        :type target: integer
        :param kwds: Arbitrary keyword arguments
        :type kwds: keyword-value couples
        :return: None
        :rtype: NoneType
        """
        self.__graph.add_edge(source, target, **kwds)
