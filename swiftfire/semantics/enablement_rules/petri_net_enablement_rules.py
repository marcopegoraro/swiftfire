from typing import Dict, Iterable, Set

from swiftfire.artifacts.nets.petri_net import petri_net


class EnablementRule:
    """
    Class defining enabled transitions in a Petri net.
    """

    @classmethod
    def is_enabled(cls, net: petri_net.PetriNet, marking: Dict[int, int], transition: int) -> bool:
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

    @classmethod
    def enabled_transitions(cls, net: petri_net.PetriNet, marking: Dict[int, int], transitions: Iterable[int] = None) -> Set[int]:
        """
        Returns the set of ids of enabled transitions given a Petri net and a marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transitions: the ids of transitions to be checked
        :type transitions: iterable of integers
        :return: the set of ids of the enabled transitions in the net
        :rtype: set of integers
        """
        if transitions is None:
            # TODO: use this method whenever the parameters of the nets and marking and the number of transitions to check makes it faster than using enabled_transition
            empty_places = net.places - {place for place, tokens in marking.items() if tokens < 1}
            return net.transitions - net.postset(empty_places)
        return {transition for transition in transitions if EnablementRule.is_enabled(net, marking, transition)}

    @classmethod
    def enabled_after_firing(cls, net: petri_net.PetriNet, transition: int, enabled_transitions: Iterable[int], marking: Dict[int, int]) -> Iterable[int]:
        """
        Given a Petri net, a marking, a transition enabled in that marking and the resulting marking after firing the transition, updates the set of enabled transitions.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param transition: an enabled transition
        :type transition: int
        :param enabled_transitions: the transitions enabled by the starting marking
        :type enabled_transitions: iterable of integers
        :param marking: the marking after firing the transition
        :type marking: dictionary of integer: integer
        :return: the updated set of enabled transitions
        :rtype: set of integers
        """
        enabled_transitions -= net.postset({place for place in net.preset(transition) if marking[place] < 1})
        enabled_transitions += cls.enabled_transitions(net, marking, net.postset(net.postset(transition)))
        return enabled_transitions


class EnablementRuleInhibitorArcs(EnablementRule):
    """
    Class defining enabled transitions in a Petri net with inhibitor arcs.
    """

    @classmethod
    def is_enabled(cls, net: petri_net.PetriNet, marking: Dict[int, int], transition: int) -> bool:
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
