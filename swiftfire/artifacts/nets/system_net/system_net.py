from typing import Iterable, Tuple, Dict
from collections import defaultdict
from itertools import repeat

from swiftfire.artifacts.nets.labeled_petri_net import labeled_petri_net


class SystemNet(labeled_petri_net.LabeledPetriNet):
    """
    Class defining a system net.
    """

    def __init__(self, places: int = 0, transitions: int = 0, arcs: Iterable[Tuple[int, int]] = None, inhibitor_arcs: Iterable[Tuple[int, int]] = None, reset_arcs: Iterable[Tuple[int, int]] = None, initial_marking: Dict[int, int] = None, final_markings: Iterable[Dict[int, int]] = None):
        """
        Constructor for the system net defined by the system_net class.
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
        super().__init__(places, transitions, arcs, inhibitor_arcs, reset_arcs)
        # if not self.is_a_marking(initial_marking):
        #     raise ValueError('Initial marking not valid.')
        # for marking in final_markings:
        #     if not self.is_a_marking(marking):
        #         raise ValueError('One or more final markings not valid.')
        # if isinstance(initial_marking, defaultdict):
        #     self.__initial_marking = initial_marking
        # else:
        #     self.__initial_marking = defaultdict(int, initial_marking)
        # self.__final_markings = map(defaultdict, repeat(int), final_markings)
        self.initial_marking = initial_marking
        self.final_markings = final_markings
        self.__enabled_transitions = self.__enablement_rule.enabled_transitions(self, self.__initial_marking)
        self.__configurations = dict()

    def __get_initial_marking(self):
        return self.__initial_marking

    def __set_initial_marking(self, initial_marking: Dict[int, int] = None):
        if not self.is_a_marking(initial_marking):
            raise ValueError('Initial marking not valid.')
        if isinstance(initial_marking, defaultdict):
            self.__initial_marking = initial_marking
        else:
            self.__initial_marking = defaultdict(int, initial_marking)

    def __get_final_markings(self):
        return self.__initial_marking

    def __set_final_markings(self, final_markings: Iterable[Dict[int, int]] = None):
        for marking in final_markings:
            if not self.is_a_marking(marking):
                raise ValueError('One or more final markings not valid.')
        self.__final_markings = map(defaultdict, repeat(int), final_markings)

    def __get_configurations(self):
        return self.__configurations

    initial_marking = property(__get_initial_marking, __set_initial_marking)
    final_markings = property(__get_final_markings, __set_final_markings)
    configurations = property(__get_configurations)

    def add_configuration(self, configuration_id: str, initial_marking: Dict[int, int], final_markings: Iterable[Dict[int, int]]):
        """
        Adds a configuration to the configuration dictionary of the system net.
        :param configuration_id: the identifier of the configuration to add
        :type configuration_id: string
        :param initial_marking: the initial marking of the configuration
        :type initial_marking: dictionary of integer: integer
        :param final_markings: the final markings of the configuration to add
        :type final_markings: iterable of dictionary of integer: integer
        :return: None
        :rtype: NoneType
        """
        self.add_configurations([(configuration_id, initial_marking, final_markings)])

    def add_configurations(self, configurations: Iterable[Tuple[str, Dict[int, int], Iterable[Dict[int, int]]]]):
        """
        Adds an iterable of configurations to the configuration dictionary of the system net.
        :param configurations: an iterable of possible configurations of the net
        :type configurations: iterable of (string, dictionary of integer: integer, iterable of dictionary of integer: integer)
        :return: None
        :rtype: NoneType
        """
        for configuration_id, initial_marking, final_markings in configurations:
            if configuration_id is None or configuration_id is '':
                raise ValueError('Configuration id must be a nonempty string.')
            for c_id in self.__configurations:
                if c_id == configuration_id:
                    raise ValueError('Configuration identifier already in use.')
            if not self.is_a_marking(initial_marking):
                raise ValueError('Initial marking not valid.')
            for marking in final_markings:
                if not self.is_a_marking(marking):
                    raise ValueError('One or more final markings not valid.')
            self.__configurations[configuration_id] = [initial_marking, self.__enablement_rule.enabled_transitions(self, initial_marking), map(defaultdict, repeat(int), final_markings)]

    def delete_configuration(self, configuration_id: str):
        """
        Deletes a configuration from the configuration dictionary of the system net.
        :param configuration_id: the identifier of the configuration to delete
        :type configuration_id: string
        :return: None
        :rtype: NoneType
        """
        del self.__configurations[configuration_id]

    def delete_configurations(self, configurations: Iterable[str]):
        """
        Deletes an iterable of configurations from the configuration dictionary of the system net.
        :param configurations: an iterable of configuration identifiers
        :type configurations: iterable of strings
        :return: None
        :rtype: NoneType
        """
        for configuration_id in configurations:
            self.delete_configuration(configuration_id)
