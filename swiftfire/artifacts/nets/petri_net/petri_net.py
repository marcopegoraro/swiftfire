from typing import Iterable, Tuple, Union, Set, Dict

from swiftfire.artifacts.graphs.swiftfire_graph import SwiftFireGraph
from swiftfire.semantics.enablement_rules import petri_net_enablement_rules
from swiftfire.semantics.firing_rules import petri_net_firing_rules


class PetriNet(dict):
    """
    Class defining a Petri net.
    """

    def __init__(self, places: int = 0, transitions: int = 0, arcs: Iterable[Tuple[int, int]] = None, inhibitor_arcs: Iterable[Tuple[int, int]] = None, reset_arcs: Iterable[Tuple[int, int]] = None):
        """
        Constructor for the Petri net defined by the PetriNet class.
        :param places: the number of places in the net
        :type places: integer
        :param transitions: the number of transitions in the net
        :type transitions: integer
        :param arcs: the arcs in the net, codified by node ids (consecutive integers)
        :type arcs: iterable of 2-uples of integers
        :param inhibitor_arcs: the inhibitor arcs in the net
        :type inhibitor_arcs: iterable of 2-uples of integers
        :param reset_arcs: the reset arcs in the net
        :type reset_arcs: iterable of 2-uples of integers
        """
        super().__init__()
        if arcs is None:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, [])
        else:
            self.__graph = SwiftFireGraph([0] * places + [1] * transitions, arcs)
        self.__places = set(range(places))
        self.__transitions = set(range(places, places + transitions))
        self.__inhibitor_arcs = set() if inhibitor_arcs is None else set(inhibitor_arcs)
        self.__reset_arcs = set() if reset_arcs is None else set(reset_arcs)
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

    def __set_enablement_rule(self, enablement_rule: petri_net_enablement_rules.EnablementRule):
        self.__enablement_rule = enablement_rule

    def __get_firing_rule(self):
        return self.__firing_rule

    def __set_firing_rule(self, firing_rule: petri_net_firing_rules.FiringRule):
        self.__firing_rule = firing_rule

    graph = property(__get_graph)
    places = property(__get_places)
    transitions = property(__get_transitions)
    inhibitor_arcs = property(__get_inhibitor_arcs)
    reset_arcs = property(__get_reset_arcs)
    enablement_rule = property(__get_enablement_rule, __set_enablement_rule)
    firing_rule = property(__get_firing_rule, __set_firing_rule)

    def preset(self, input_value: Union[int, Iterable[int]]) -> Set[int]:
        """
        Computes the preset of a node or a container of nodes.
        :param input_value: a node or an iterable of nodes
        :type input_value: integer or iterable of integers
        :return: the set of node ids in the preset of the input
        :rtype: set of integers
        """
        return self.__graph.neighbors(input_value, mode='in')

    def postset(self, input_value: Union[int, Iterable[int]]) -> Set[int]:
        """
        Computes the postset of a node or a container of nodes.
        :param input_value: a node or an iterable of nodes
        :type input_value: integer or iterable of integers
        :return: the set of node ids in the postset of the input
        :rtype: set of integers
        """
        return self.__graph.neighbors(input_value, mode='out')

    def is_a_place(self, place_id: int) -> bool:
        """
        Checks if a node is a valid place.
        :param place_id: the id of the place to check
        :type place_id: integer
        :return: True if the id belongs to a valid place, False otherwise
        :rtype: boolean
        """
        if isinstance(place_id, int) and place_id < len(self.__graph.nodes):
            if not self.__graph.nodes[place_id]['type']:
                return True
        return False

    def add_place(self):
        """
        Adds a place to the Petri net.
        :return: None
        :rtype: NoneType
        """
        self.__graph.add_vertex(type=0)
        self.__places.add(len(self.__graph.vs) - 1)

    def add_places(self, n: int):
        """
        Adds multiple places to the Petri net.
        :param n: the number of places to be added
        :type n: integer
        :return: None
        :rtype: NoneType
        """
        for i in range(n):
            self.add_place()

    def is_a_transition(self, transition_id: int) -> bool:
        """
        Checks if a node is a valid transition.
        :param transition_id: the id of the transition to check
        :type transition_id: integer
        :return: True if the id belongs to a valid transition, False otherwise
        :rtype: boolean
        """
        if isinstance(transition_id, int) and transition_id < len(self.__graph.nodes):
            if self.__graph.nodes[transition_id]['type']:
                return True
        return False

    def add_transition(self):
        """
        Adds a transition to the Petri net.
        :return: None
        :rtype: Nonetype
        """
        self.__graph.add_vertex(type=1)
        self.__transitions.add(len(self.__graph.vs) - 1)

    def add_transitions(self, n: int):
        """
        Adds multiple transitions to the Petri net.
        :param n: the number of transitions to be added
        :type n: integer
        :return: None
        :rtype: NoneType
        """
        for i in range(n):
            self.add_transition()

    def add_arc(self, source: int, target: int):
        """
        Adds an arc to the Petri net.
        :param source: the source node of the arc
        :type source: integer
        :param target: the target node of the arc
        :type target: integer
        :return: None
        :rtype: NoneType
        """
        if self.__graph.nodes[source]['type'] == self.__graph.nodes[target]['type']:
            raise ValueError('Arc connecting two places or two transitions.')
        self.__graph.add_edge(source, target)

    def add_arcs(self, arcs: Iterable[Tuple[int, int]]):
        """
        Adds multiple arcs to the Petri net.
        :param arcs: the arcs to be added - an iterable of 2-uples (source id, target id)
        :type arcs: iterable of 2-uples of integers
        :return: None
        :rtype: NoneType
        """
        for arc in arcs:
            if self.__graph.nodes[arc[0]]['type'] == self.__graph.nodes[arc[1]]['type']:
                raise ValueError('Arc connecting two places or two transitions.')
        for arc in arcs:
            self.add_arc(arc[0], arc[1])

    def is_a_marking(self, marking: Dict[int, int]) -> bool:
        """
        Checks if a marking is valid for the Petri net.
        :param marking: the marking to be checked
        :type marking: dictionary of integer: integer
        :return: True if the marking is valid, False otherwise
        :rtype: boolean
        """
        for place, tokens in marking.items():
            if not self.is_a_place(place) or not isinstance(tokens, int) or tokens < 0:
                return False
        return True
