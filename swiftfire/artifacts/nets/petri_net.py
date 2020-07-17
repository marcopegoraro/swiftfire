from swiftfire.artifacts.graphs.swiftfire_graph import SwiftFireGraph
from swiftfire.semantics.enablement_rules import petrinet_enablement_rules
from swiftfire.semantics.firing_rules import petrinet_firing_rules


class PetriNet:

    def __init__(self, places=0, transitions=0, arcs=None, inhibitor_arcs=None, reset_arcs=None):
        if arcs is None:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, [])
        else:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, arcs)
        self.__places = list(range(places))
        self.__transitions = list(range(places, places + transitions))
        self.__inhibitor_arcs = set() if inhibitor_arcs is None else inhibitor_arcs
        self.__reset_arcs = set() if reset_arcs is None else reset_arcs
        self.__enablement_rule = petrinet_enablement_rules.EnablementRule if inhibitor_arcs is None else petrinet_enablement_rules.EnablementRuleInhibitorArcs
        self.__firing_rule = petrinet_firing_rules.FiringRule if reset_arcs is None else petrinet_firing_rules.FiringRuleResetArcs

    def __get_graph(self):
        return self.__graph

    def __get_places(self):
        return self.__places

    def __get_transitions(self):
        return self.__transitions

    def __get_inhibitor_arcs(self):
        return self.__inhibitor_arcs

    def __get_reset_arcs(self):
        return self.__reset_arcs

    def __get_enablement_rule(self):
        return self.__enablement_rule

    def __set_enablement_rule(self, enablement_rule):
        self.__enablement_rule = enablement_rule

    def __get_firing_rule(self):
        return self.__firing_rule

    def __set_firing_rule(self, firing_rule):
        self.__firing_rule = firing_rule

    graph = property(__get_graph)
    inhibitor_arcs = property(__get_inhibitor_arcs)
    reset_arcs = property(__get_reset_arcs)
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

    def is_a_place(self, place_id):
        if place_id in self.__graph:
            if not self.__graph[place_id]['type']:
                return True
        return False

    def add_place(self, **kwds):
        kwds['type'] = 0
        self.__graph.add_node(**kwds)

    def add_places(self, n):
        for i in range(n):
            self.add_place()

    def is_a_transition(self, transition_id):
        if transition_id in self.__graph:
            if self.__graph[transition_id]['type']:
                return True
        return False

    def add_transition(self, **kwds):
        kwds['type'] = 1
        self.__graph.add_node(**kwds)

    def add_transitions(self, n):
        for i in range(n):
            self.add_transition()

    def add_edge(self, source, target, **kwds):
        self.__graph.add_edge(source, target, **kwds)

    def is_a_marking(self, marking):
        for place, tokens in marking.items():
            if not self.is_a_place(place) or not isinstance(tokens, int) or tokens < 0:
                return False
        return True
