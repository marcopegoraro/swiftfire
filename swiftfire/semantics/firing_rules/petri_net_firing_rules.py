class TransitionNotEnabledError(ValueError):
    # TODO: move to a more appropriate place
    pass


class FiringRule:

    @staticmethod
    def fire(net, marking, transition):
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

    @staticmethod
    def fire(net, marking, transition):
        # TODO: implement
        raise NotImplementedError
