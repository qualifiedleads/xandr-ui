from rtb.placement_state import PlacementState


def suspend_state_middleware_cron():
    state = PlacementState(None, None)
    state.placement_targets_list()
