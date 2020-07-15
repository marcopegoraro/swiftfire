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

    def __get_graph(self):
        return self.__graph

    def __set_graph(self, graph):
        self.__graph = graph

    def __get_inhibitor_arcs(self):
        return self.__inhibitor_arcs

    def __set_inhibitor_arcs(self, inhibitor_arcs):
        self.__inhibitor_arcs = inhibitor_arcs

    def __get_reset_arcs(self):
        return self.__reset_arcs

    def __set_reset_arcs(self, reset_arcs):
        self.__reset_arcs = reset_arcs

    def __get_enablement_rule(self):
        return self.__enablement_rule

    def __set_enablement_rule(self, enablement_rule):
        self.__enablement_rule = enablement_rule

    def __get_firing_rule(self):
        return self.__firing_rule

    def __set_firing_rule(self, firing_rule):
        self.__firing_rule = firing_rule

    graph = property(__get_graph, __set_graph)
    inhibitor_arcs = property(__get_inhibitor_arcs, __set_inhibitor_arcs)
    reset_arcs = property(__get_reset_arcs, __set_reset_arcs)
    enablement_rule = property(__get_enablement_rule, __set_enablement_rule)
    firing_rule = property(__get_firing_rule, __set_firing_rule)

    def __getitem__(self, key):
        return self.__graph[key]

    def __setitem__(self, key, value):
        self.__graph[key] = value

    def __delitem__(self, key):
        del self.__graph[key]

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self.__graph[key] = value
