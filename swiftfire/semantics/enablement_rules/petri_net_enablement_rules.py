class EnablementRule:

    @staticmethod
    def is_enabled(net, marking, transition):
        for place in net.preset(transition):
            if place not in marking or marking[place] < 1:
                return False
        return True

    @staticmethod
    def enabled_transitions(net, marking):
        return {transition for transition in net.transitions if EnablementRule.is_enabled(net, marking, transition)}


class EnablementRuleInhibitorArcs(EnablementRule):

    @staticmethod
    def enabled_transitions(net, marking):
        # TODO: implement
        raise NotImplementedError
