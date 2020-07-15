from swiftfire.artifacts.graphs.swiftfire_graph import SwiftFireGraph


class PetriNet:

    def __init__(self, name='', places=0, transitions=0, arcs=None, inhibitor_arcs=None, reset_arcs=None, properties=None):
        self.__name = '' if name is None else properties
        if arcs is None:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, [])
        else:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, arcs)
        self.__inhibitor_arcs = set() if inhibitor_arcs is None else inhibitor_arcs
        self.__reset_arcs = set() if reset_arcs is None else reset_arcs
        self.__properties = dict() if properties is None else properties
