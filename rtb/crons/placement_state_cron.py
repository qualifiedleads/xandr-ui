from rtb.placement_state import PlacementState


def suspend_state_middleware_cron():
    state = PlacementState(None, None)
    state.suspend_state_middleware()
    print 'Happy end'


def platform_placement_targets():
    state = PlacementState(None, None)
    state.placement_targets_list()

def change_state_placement_by_cron_settings():
    state = PlacementState(None, None)
    state.change_state_placement_by_cron()


