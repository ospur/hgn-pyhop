import hgn_pyhop


# Find a truck in the same city as the package
def find_truck(state, o):
    for t in state.trucks:
        if state.in_city[state.at[t]] == state.in_city[state.at[o]]:
            return t
    return False


# Find a plane in the same city as the package; if none available, find a random plane
def find_plane(state, o):
    for plane in state.airplanes:
        if state.in_city[state.at[plane]] == state.in_city[state.at[o]]:
            return plane
    return plane


# Find an airport in the same city as the location
def find_airport(state, l):
    for a in state.airports:
        if state.in_city[a] == state.in_city[l]:
            return a
    return False


# Operators
def drive_truck(state, t, l):
    if t in state.trucks and l in state.locations and state.in_city[state.at[t]] == state.in_city[l]:
        state.at[t] = l
        return state
    return False


def load_truck(state, o, t):
    if o in state.packages and t in state.trucks and state.at[o] == state.at[t]:
        state.at[o] = t
        return state
    return False


def unload_truck(state, o, l):
    if o in state.packages and state.at[o] in state.trucks and l in state.locations:
        t = state.at[o]
        if state.at[t] == l:
            state.at[o] = l
            return state
    return False


def fly_plane(state, plane, a):
    if plane in state.airplanes and a in state.airports:
        state.at[plane] = a
        return state
    return False


def load_plane(state, o, plane):
    if o in state.packages and plane in state.airplanes and state.at[o] == state.at[plane]:
        state.at[o] = plane
        return state
    return False


def unload_plane(state, o, a):
    if o in state.packages and state.at[o] in state.airplanes and a in state.airports:
        plane = state.at[o]
        if state.at[plane] == a:
            state.at[o] = a
            return state
    return False


hgn_pyhop.declare_operators('at', drive_truck, load_truck, unload_truck, fly_plane, load_plane, unload_plane)


# Methods
def move_within_city(state, o, l):
    if o in state.packages and state.at[o] in state.locations and state.in_city[state.at[o]] == state.in_city[l]:
        t = find_truck(state, o)
        if t:
            return [('at', t, state.at[o]), ('at', o, t), ('at', t, l), ('at', o, l)]
    return False


def move_between_airports(state, o, a):
    if o in state.packages and state.at[o] in state.airports and a in state.airports and state.in_city[state.at[o]] != state.in_city[a]:
        plane = find_plane(state, o)
        if plane:
            return [('at', plane, state.at[o]), ('at', o, plane), ('at', plane, a), ('at', o, a)]
    return False


def move_between_city(state, o, l):
    if o in state.packages and state.at[o] in state.locations and state.in_city[state.at[o]] != state.in_city[l]:
        a1 = find_airport(state, state.at[o])
        a2 = find_airport(state, l)
        if a1 and a2:
            return [('at', o, a1), ('at', o, a2), ('at', o, l)]
    return False


hgn_pyhop.declare_methods('at', move_within_city, move_between_airports, move_between_city)
