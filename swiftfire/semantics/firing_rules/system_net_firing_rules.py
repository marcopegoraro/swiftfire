from typing import Union, Dict, Callable, Tuple, Any
from random import sample
from collections import defaultdict

from swiftfire.semantics.firing_rules import petri_net_firing_rules, labeled_petri_net_firing_rules
from swiftfire.artifacts.nets.system_net import system_net
from swiftfire.identifiers import LABEL_ID, DEFAULT_CONFIG, CURRENT_MARKING, ENABLED_TRANSITIONS


class SystemNetFiringRule(labeled_petri_net_firing_rules.LabeledPetriNetFiringRule):
    """
    Class defining the firing rule of a Petri net.
    """

    @classmethod
    def fire(cls, net: system_net.SystemNet, marking: Union[Dict[int, int], str] = None, transition: int = None, transition_selector: Callable = None, label_id: str = LABEL_ID, on_fire_function: Callable = None) -> Tuple[Dict[int, int], Any]:
        """
        Method that fires an enabled transitions given a system net and a marking, and returns the resulting marking.
        :param net: a labeled Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.LabeledPetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :param transition_selector: a function that randomly selectes a transition
        :type transition_selector: callable
        :param label_id: the label identifier
        :type label_id: string
        :param on_fire_function: a function applied on the transition label
        :type on_fire_function: callable
        :return: the marking resulting from firing the transition in the given Petri net and the label of the fired transition
        :rtype: dictionary of integer: integer
        """
        if isinstance(marking, dict):
            return super().fire(net, marking, transition, transition_selector, label_id, on_fire_function)
        if marking is None:
            marking = DEFAULT_CONFIG
        enabled_transitions = net.configurations[marking][ENABLED_TRANSITIONS]
        if transition is None:
            if transition_selector is None:
                transition = sample(enabled_transitions, 1)
            else:
                transition = transition_selector(enabled_transitions)
        else:
            if transition not in enabled_transitions:
                raise petri_net_firing_rules.TransitionNotEnabledError(f'Transition {transition} is not enabled on configuration "{marking}".')
        pre_marking = defaultdict(int, net.configurations[marking][CURRENT_MARKING])
        resulting_marking, label = super().unchecked_fire(net, net.configurations[marking][CURRENT_MARKING], transition, label_id, on_fire_function)
        net.enablement_rule.enabled_after_firing(net, transition, pre_marking, enabled_transitions, net.configurations[marking][CURRENT_MARKING])
        return resulting_marking, label


class SystemNetFiringRuleResetArcs(SystemNetFiringRule):
    """
    Class defining the firing rule of a Petri net with reset arcs.
    """

    @classmethod
    def fire(cls, net: system_net.SystemNet, marking: Union[Dict[int, int], str] = None, transition: int = None, transition_selector: Callable = None, label_id: str = LABEL_ID, on_fire_function: Callable = None) -> Tuple[Dict[int, int], Any]:
        """
        Method that fires an enabled transitions given a system net and a marking, and returns the resulting marking.
        :param net: a labeled Petri net
        :type net: swiftfire.artifacts.nets.petri_net.petri_net.LabeledPetriNet
        :param marking: the current marking of the Petri net
        :type marking: dictionary of integer: integer
        :param transition: the id of the transition to fire
        :type transition: int
        :param transition_selector: a function that randomly selectes a transition
        :type transition_selector: callable
        :param label_id: the label identifier
        :type label_id: string
        :param on_fire_function: a function applied on the transition label
        :type on_fire_function: callable
        :return: the marking resulting from firing the transition in the given Petri net and the label of the fired transition
        :rtype: dictionary of integer: integer
        """
        # TODO: implement. Might be unnecessary, depending on the implementation in the superclass
        raise NotImplementedError
