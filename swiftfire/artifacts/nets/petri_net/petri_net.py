from itertools import islice

from swiftfire.artifacts.graphs.swiftfire_graph import SwiftFireGraph
from swiftfire.semantics.enablement_rules import petri_net_enablement_rules
from swiftfire.semantics.firing_rules import petri_net_firing_rules


class PetriNet:

    def __init__(self, places=0, transitions=0, arcs=None, inhibitor_arcs=None, reset_arcs=None):
        if arcs is None:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, [])
        else:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, arcs)
        self.__places = set(range(places))
        self.__transitions = set(range(places, places + transitions))
        self.__inhibitor_arcs = set() if inhibitor_arcs is None else inhibitor_arcs
        self.__reset_arcs = set() if reset_arcs is None else reset_arcs
        self.__enablement_rule = petri_net_enablement_rules.EnablementRule if inhibitor_arcs is None else petri_net_enablement_rules.EnablementRuleInhibitorArcs
        self.__firing_rule = petri_net_firing_rules.FiringRule if reset_arcs is None else petri_net_firing_rules.FiringRuleResetArcs

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
    places = property(__get_places)
    transitions = property(__get_transitions)
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

    def preset(self, input_value):
        if isinstance(input_value, int):
            return set(self.__graph.neighbors(input_value, mode='in'))
        else:
            presets_list = [self.__graph.neighbors(node, mode='in') for node in input_value]
            return set.union(set(presets_list[0]), *islice(presets_list, 1, None))

    def postset(self, input_value):
        if isinstance(input_value, int):
            return set(self.__graph.neighbors(input_value, mode='out'))
        else:
            postsets_list = [self.__graph.neighbors(node, mode='out') for node in input_value]
            return set.union(set(postsets_list[0]), *islice(postsets_list, 1, None))

    def is_a_place(self, place_id):
        if isinstance(place_id, int) and place_id < len(self.__graph.nodes):
            if not self.__graph.nodes[place_id]['type']:
                return True
        return False

    def add_place(self):
        self.__graph.add_vertex(type=0)
        self.__places.add(len(self.__graph.vs) - 1)

    def add_places(self, n):
        for i in range(n):
            self.add_place()

    def is_a_transition(self, transition_id):
        if isinstance(transition_id, int) and transition_id < len(self.__graph.nodes):
            if self.__graph.nodes[transition_id]['type']:
                return True
        return False

    def add_transition(self):
        self.__graph.add_vertex(type=1)
        self.__transitions.add(len(self.__graph.vs) - 1)

    def add_transitions(self, n):
        for i in range(n):
            self.add_transition()

    def add_arc(self, source, target):
        if self.__graph.nodes[source]['type'] == self.__graph.nodes[target]['type']:
            raise ValueError('Arc connecting two places or two transitions.')
        self.__graph.add_edge(source, target)

    def add_arcs(self, arcs):
        for arc in arcs:
            if self.__graph.nodes[arc[0]]['type'] == self.__graph.nodes[arc[1]]['type']:
                raise ValueError('Arc connecting two places or two transitions.')
        for arc in arcs:
            self.add_arc(arc[0], arc[1])

    def is_a_marking(self, marking):
        for place, tokens in marking.items():
            if not self.is_a_place(place) or not isinstance(tokens, int) or tokens < 0:
                return False
        return True
