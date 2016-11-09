from rtb.placement_state import PlacementState


def suspend_state_middleware_cron():
    state = PlacementState(None, None)
    state.suspend_state_middleware()
    print 'Happy end'
