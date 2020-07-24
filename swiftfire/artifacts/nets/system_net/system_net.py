from typing import Iterable, Tuple, Dict
from collections import defaultdict
from itertools import repeat
import warnings

from swiftfire.artifacts.nets.labeled_petri_net import labeled_petri_net
from swiftfire.identifiers import DEFAULT_CONFIG, INITIAL_MARKING, CURRENT_MARKING, ENABLED_TRANSITIONS, FINAL_MARKINGS


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
        self.add_configuration(DEFAULT_CONFIG, initial_marking, final_markings)
        self.__configurations = dict()

    def __get_configurations(self):
        return self.__configurations

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
        self.add_configurations(((configuration_id, initial_marking, final_markings),))

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
            for final_marking in final_markings:
                if not self.is_a_marking(final_marking):
                    raise ValueError('One or more final markings not valid.')
            self.__configurations[configuration_id][INITIAL_MARKING] = initial_marking
            self.__configurations[configuration_id][CURRENT_MARKING] = defaultdict(int, initial_marking)
            self.__configurations[configuration_id][ENABLED_TRANSITIONS] = self.__enablement_rule.enabled_transitions(self, initial_marking)
            self.__configurations[configuration_id][FINAL_MARKINGS] = map(defaultdict, repeat(int), final_markings)

    def delete_configuration(self, configuration_id: str):
        """
        Deletes a configuration from the configuration dictionary of the system net.
        :param configuration_id: the identifier of the configuration to delete
        :type configuration_id: string
        :return: None
        :rtype: NoneType
        """
        if configuration_id == DEFAULT_CONFIG:
            warnings.warn('Deletion of default configuration skipped', RuntimeWarning)
        else:
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

    def reset_configuration(self, configuration_id: str):
        """
        Resets a configuration to the initial marking from the configuration dictionary of the system net.
        :param configuration_id: the identifier of the configuration to reset
        :type configuration_id: string
        :return: None
        :rtype: NoneType
        """
        self.__configurations[configuration_id][CURRENT_MARKING] = defaultdict(int, self.__configurations[configuration_id][INITIAL_MARKING])

    def reset_configurations(self, configurations: Iterable[str]):
        """
        Resets an iterable of configurations to the initial marking from the configuration dictionary of the system net.
        :param configurations: an iterable of configuration identifiers
        :type configurations: iterable of strings
        :return: None
        :rtype: NoneType
        """
        for configuration_id in configurations:
            self.reset_configuration(configuration_id)
