from typing import Dict, Callable, Tuple, Any

from swiftfire.semantics.firing_rules import petri_net_firing_rules
from swiftfire.artifacts.nets.labeled_petri_net import labeled_petri_net
from swiftfire.identifiers import LABEL_ID


class LabeledPetriNetFiringRule(petri_net_firing_rules.FiringRule):
    """
    Class defining the firing rule of a Petri net.
    """

    @staticmethod
    def fire(net: labeled_petri_net.LabeledPetriNet, marking: Dict[int, int], transition: int, label_id: str = LABEL_ID, on_fire_function: Callable = None) -> Tuple[Dict[int, int], Any]:
        """
        Method that fires an enabled transitions given a Petri net and a marking, and returns the resulting marking.
        :param net: a labeled Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.LabeledPetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :param label_id: the label identifier
        :type label_id: string
        :param on_fire_function: a function applied on the transition label
        :type on_fire_function: callable
        :return: the marking resulting from firing the transition in the given Petri net and the label of the fired transition
        :rtype: dictionary of integer: integer
        """
        if on_fire_function is None:
            return super().fire(net, marking, transition), net.graph.nodes[transition][label_id]
        else:
            return super().fire(net, marking, transition), on_fire_function(net.graph.nodes[transition][label_id])


class LabeledPetriNetFiringRuleResetArcs(LabeledPetriNetFiringRule):
    """
    Class defining the firing rule of a Petri net with reset arcs.
    """

    @staticmethod
    def fire(net: labeled_petri_net.LabeledPetriNet, marking: Dict[int, int], transition: int, label_id: str = LABEL_ID, on_fire_function: Callable = None) -> Tuple[Dict[int, int], Any]:
        """
        Method that fires an enabled transitions given a Petri net and a marking, and returns the resulting marking.
        :param net: a labeled Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.LabeledPetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :param label_id: the label identifier
        :type label_id: string
        :param on_fire_function: a function applied on the transition label
        :type on_fire_function: callable
        :return: the marking resulting from firing the transition in the given Petri net and the label of the fired transition
        :rtype: dictionary of integer: integer
        """
        # TODO: implement. Might be unnecessary, depending on the implementation in the superclass
        raise NotImplementedError
