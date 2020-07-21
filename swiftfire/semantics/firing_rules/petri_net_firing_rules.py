from typing import Dict

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

    @staticmethod
    def fire(net: petri_net.PetriNet, marking: Dict[int, int], transition: int) -> Dict[int, int]:
        """
        Method that fires an enabled transitions given a Petri net and a marking, and returns the resulting marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :return: the marking resulting from firing the transition in the given Petri net
        :rtype: dictionary of integer: integer
        """
        if net.enablement_rule.is_enabled(net, marking, transition):
            for place in net.preset(transition):
                marking[place] -= 1
            for place in net.postset(transition):
                if place in marking:
                    marking[place] += 1
                else:
                    marking[place] = 1
            return marking
        else:
            raise TransitionNotEnabledError()


class FiringRuleResetArcs(FiringRule):
    """
    Class defining the firing rule of a Petri net with reset arcs.
    """

    @staticmethod
    def fire(net: petri_net.PetriNet, marking: Dict[int, int], transition: int) -> Dict[int, int]:
        """
        Method that fires an enabled transitions given a Petri net and a marking, and returns the resulting marking.
        :param net: a Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.PetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :return: the marking resulting from firing the transition in the given Petri net
        :rtype: dictionary of integer: integer
        """
        # TODO: implement
        raise NotImplementedError
