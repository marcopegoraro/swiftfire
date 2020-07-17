class EnablementRule:
    def enabled_transitions(self, net, marking):
        # return {transition for transition in net.transitions if min(marking[place] for place in net.graph.degree(type="in")[transition]) > 0}
        enabled_transitions = set()
        for transition in net.transitions:
            enabled = True
            for place in net.graph.degree(type="in")[transition]:
                if marking[place] < 1:
                    enabled = False
                    break
            if enabled:
                enabled_transitions.add(transition)
        return enabled_transitions


class EnablementRuleInhibitorArcs(EnablementRule):
    def enabled_transitions(self, net, marking):
        pass
