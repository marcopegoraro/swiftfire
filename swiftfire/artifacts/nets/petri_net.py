from swiftfire.artifacts.graphs.swiftfire_graph import SwiftFireGraph
from swiftfire.semantics.enablement_rules import petrinet_enablement_rules
from swiftfire.semantics.firing_rules import petrinet_firing_rules


class PetriNet:

    def __init__(self, places=0, transitions=0, arcs=None, inhibitor_arcs=None, reset_arcs=None):
        if arcs is None:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, [])
        else:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, arcs)
        self.__inhibitor_arcs = set() if inhibitor_arcs is None else inhibitor_arcs
        self.__reset_arcs = set() if reset_arcs is None else reset_arcs
        self.__enablement_rule = petrinet_enablement_rules.EnablementRule if inhibitor_arcs is None else petrinet_enablement_rules.EnablementRuleInhibitorArcs
        self.__firing_rule = petrinet_firing_rules.FiringRule if reset_arcs is None else petrinet_firing_rules.FiringRuleResetArcs

    def __getitem__(self, key):
        return self.__graph[key]

    def __setitem__(self, key, value):
        self.__graph[key] = value

    def __delitem__(self, key):
        del self.__graph[key]

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self.__graph[key] = value
