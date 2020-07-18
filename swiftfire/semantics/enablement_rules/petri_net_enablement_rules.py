class EnablementRule:

    def is_enabled(self, net, marking, transition):
        for place in net.preset(transition):
            if marking[place] < 1:
                return False
        return True

    def enabled_transitions(self, net, marking):
        return {transition for transition in net.transitions if self.is_enabled(net, marking, transition)}


class EnablementRuleInhibitorArcs(EnablementRule):
    def enabled_transitions(self, net, marking):
        # TODO: implement
        raise NotImplementedError
