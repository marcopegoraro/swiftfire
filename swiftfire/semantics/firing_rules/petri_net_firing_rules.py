from typing import Dict, Callable
from random import sample

from swiftfire.artifacts.nets.petri_net import petri_net


class TransitionNotEnabledError(ValueError):
    """
    Exception raised when trying to fire a non-enabled transition.
    """
    # TODO: move to a more appropriate place
    pass


class FiringRule:
    """
    Class defining the firing rule of a Petri net.
    """

    @classmethod
    def fire(cls, net: petri_net.PetriNet, marking: Dict[int, int], transition: int = None, transition_selector: Callable = None) -> Dict[int, int]:
        """
        Method that fires an enabled transitions given a Petri net and a marking, and returns the resulting marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :param transition_selector:
        :type transition_selector:
        :return: the marking resulting from firing the transition in the given Petri net
        :rtype: dictionary of integer: integer
        """
        if transition is not None:
            if not net.enablement_rule.is_enabled(net, marking, transition):
                raise TransitionNotEnabledError(f'Transition {transition} is not enabled.')
        elif transition_selector is None:
            transition = sample(net.enablement_rule.enabled_transitions(net, marking), 1)
        else:
            transition = transition_selector(net.enablement_rule.enabled_transitions(net, marking))
        return cls.unchecked_fire(net, marking, transition, transition_selector)

    @classmethod
    def unchecked_fire(cls, net: petri_net.PetriNet, marking: Dict[int, int], transition: int = None, transition_selector: Callable = None) -> Dict[int, int]:
        """
        Method that fires a transitions given a Petri net and a marking, and returns the resulting marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :param transition_selector: a function that randomly selectes a transition
        :type transition_selector: callable
        :return: the marking resulting from firing the transition in the given Petri net
        :rtype: dictionary of integer: integer
        """
        if transition is None:
            if transition_selector is None:
                transition = sample(net.transitions, 1)
            else:
                transition = transition_selector(net.transitions)
        for place in net.preset(transition):
            marking[place] -= 1
        for place in net.postset(transition):
            if place in marking:
                marking[place] += 1
            else:
                marking[place] = 1
        return marking


class FiringRuleResetArcs(FiringRule):
    """
    Class defining the firing rule of a Petri net with reset arcs.
    """

    @classmethod
    def fire(cls, net: petri_net.PetriNet, marking: Dict[int, int], transition: int = None, transition_selector: Callable = None) -> Dict[int, int]:
        """
        Method that fires an enabled transitions given a Petri net and a marking, and returns the resulting marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :param transition_selector: a function that randomly selectes a transition
        :type transition_selector: callable
        :return: the marking resulting from firing the transition in the given Petri net
        :rtype: dictionary of integer: integer
        """
        # TODO: implement
        raise NotImplementedError
