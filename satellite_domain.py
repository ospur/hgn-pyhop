import hgn_pyhop


# Find an instrument that supports mode m
def find_instrument(state, m):
    for i in state.instruments:
        if m in state.supports[i]:
            return i
    return False


# Operators
def turn_to(state, s, d):
    if s in state.satellites and d in state.directions:
        state.pointing[s] = d
        return state
    return False


def switch_on(state, i, val):
    if i in state.instruments and state.power_avail[state.on_board[i]]:
        state.power_on[i] = True
        state.power_avail[state.on_board[i]] = False
        return state
    return False


def switch_off(state, i, val):
    if i in state.instruments and state.power_on[i]:
        state.power_on[i] = False
        state.power_avail[state.on_board[i]] = True
        return state
    return False


def calibrate(state, i, val):
    if i in state.instruments and state.power_on[i] and state.pointing[state.on_board[i]] == state.calibration_target[i]:
        state.calibrated[i] = True
        return state
    return False


def take_image(state, d, m):
    if d in state.directions and m in state.modes:
        i = find_instrument(state, m)
        if state.power_on[i] and state.calibrated[i] and state.pointing[state.on_board[i]] == d:
            state.have_image[d] = m
            return state
    return False


hgn_pyhop.declare_operators('pointing', turn_to)
hgn_pyhop.declare_operators('power_on', switch_on, switch_off)
hgn_pyhop.declare_operators('calibrated', calibrate)
hgn_pyhop.declare_operators('have_image', take_image)


# Methods
def capture_image(state, d, m):
    if d in state.directions and m in state.modes:
        i = find_instrument(state, m)
        if not state.power_on[i] or not state.calibrated[i] or not state.pointing[state.on_board[i]] == d:
            return [('power_on', i, True), ('calibrated', i, True), ('pointing', state.on_board[i], d), ('have_image', d, m)]
    return False


def calibrate_instrument(state, i, val):
    if i in state.instruments and state.power_on[i] and not state.pointing[state.on_board[i]] == state.calibration_target[i]:
        return [('pointing', state.on_board[i], state.calibration_target[i]), ('calibrated', i, True)]
    return


def activate(state, i, val):
    if i in state.instruments and not state.power_avail[state.on_board[i]]:
        for i0 in state.instruments:
            if state.on_board[i0] == state.on_board[i] and i0 != i and state.power_on[i0]:
                return [('power_on', i0, False), ('power_on', i, True)]
    return False


hgn_pyhop.declare_methods('power_on', activate)
hgn_pyhop.declare_methods('calibrated', calibrate_instrument)
hgn_pyhop.declare_methods('have_image', capture_image)
