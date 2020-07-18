class TransitionNotEnabledError(ValueError):
    # TODO: move to a more appropriate place
    pass


class FiringRule:
    def fire(self, net, marking, transition):
        if net.enablement_rule.is_enabled(net, transition, marking):
            for place in net.preset(transition):
                marking[place] -= 1
            for place in net.postset(transition):
                marking[place] += 1
            return marking
        else:
            raise TransitionNotEnabledError()


class FiringRuleResetArcs(FiringRule):
    def fire(self, net, marking, transition):
        # TODO: implement
        raise NotImplementedError
