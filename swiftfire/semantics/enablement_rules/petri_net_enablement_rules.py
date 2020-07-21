from typing import Dict, Set

from swiftfire.artifacts.nets.petri_net import petri_net


class EnablementRule:
    """
    Class defining enabled transitions in a Petri net.
    """

    @staticmethod
    def is_enabled(net: petri_net.PetriNet, marking: Dict[int, int], transition: int) -> bool:
        """
        Checks if a transition is enabled given a Petri net and a marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to be checked
        :type transition: integer
        :return: True if the transition is enabled, False otherwise
        :rtype: boolean
        """
        for place in net.preset(transition):
            if place not in marking or marking[place] < 1:
                return False
        return True

    @staticmethod
    def enabled_transitions(net: petri_net.PetriNet, marking: Dict[int, int]) -> Set[int]:
        """
        Returns the set of ids of enabled transitions given a Petri net and a marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :return: the set of ids of the enabled transitions in the net
        :rtype: set of integers
        """
        return {transition for transition in net.transitions if EnablementRule.is_enabled(net, marking, transition)}


class EnablementRuleInhibitorArcs(EnablementRule):
    """
    Class defining enabled transitions in a Petri net with inhibitor arcs.
    """

    @staticmethod
    def is_enabled(net: petri_net.PetriNet, marking: Dict[int, int], transition: int) -> bool:
        """
        Checks if a transition is enabled given a Petri net and a marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to be checked
        :type transition: integer
        :return: True if the transition is enabled, False otherwise
        :rtype: boolean
        """
        # TODO: implement
        raise NotImplementedError
