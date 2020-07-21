from typing import Union, Sequence, Any, Iterable, Tuple

from swiftfire.artifacts.nets.petri_net import petri_net
from swiftfire.semantics.enablement_rules import petri_net_enablement_rules
from swiftfire.semantics.firing_rules import labeled_petri_net_firing_rules
from swiftfire.identifiers import LABEL_ID


class LabeledPetriNet(petri_net.PetriNet):
    """
    Class defining a labeled Petri net.
    """

    def __init__(self, places: int = 0, transitions: Union[int, Sequence[Any]] = 0, arcs: Iterable[Tuple[int, int]] = None, inhibitor_arcs: Iterable[Tuple[int, int]] = None, reset_arcs: Iterable[Tuple[int, int]] = None, label_id: str = LABEL_ID):
        if isinstance(transitions, int):
            super(LabeledPetriNet, self).__init__(places, transitions, arcs, inhibitor_arcs, reset_arcs)
        else:
            super(LabeledPetriNet, self).__init__(places, len(transitions), arcs, inhibitor_arcs, reset_arcs)
            self.graph.nodes[self.transitions][label_id] = transitions
        self.__enablement_rule = petri_net_enablement_rules.EnablementRule if inhibitor_arcs is None else petri_net_enablement_rules.EnablementRuleInhibitorArcs
        self.__firing_rule = labeled_petri_net_firing_rules.LabeledPetriNetFiringRuleResetArcs if reset_arcs is None else labeled_petri_net_firing_rules.LabeledPetriNetFiringRule

    def __set_firing_rule(self, firing_rule: labeled_petri_net_firing_rules.LabeledPetriNetFiringRule = labeled_petri_net_firing_rules.LabeledPetriNetFiringRuleResetArcs):
        self.__firing_rule = firing_rule

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
