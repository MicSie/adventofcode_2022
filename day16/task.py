from datetime import datetime
import functools
import os
import re
from .context import basics as helpers

_valves = {}


class Valve:
    def __init__(self) -> None:
        self.name = ''
        self.flow_rate = 0
        self.connected_tunnels = []


def read_input(file_name):
    helpers.ensure_directory(os.path.dirname(__file__))
    valves = {}
    for input_line in helpers.read_file(file_name):
        valve = Valve()
        valve.name = re.search('(?<=Valve )..', input_line).group().strip()
        valve.flow_rate = int(re.search('\d+', input_line).group().strip())
        valve.connected_tunnels = [tunnel.strip() for tunnel in re.search(
            '(?<=valve ).*|(?<=valves ).*', input_line).group().split(',')]
        valves[valve.name] = valve
    return valves


def open_valves(valves, with_elephant=False):
    global _valves
    _valves = valves
    minute = 26 if with_elephant else 30
    valves_to_go = [key for key, valve in _valves.items(
    ) if valve.flow_rate > 0]
    released_pressure = _find_best_way(
        frozenset(valves_to_go), 'AA', minute, with_elephant)

    return released_pressure


@functools.cache
def _find_best_way(valves_to_go, current_position, time, with_elephant=False):
    # find the best remaining way for the elephant from start position
    best_possible_release = _find_best_way(
        valves_to_go,
        'AA',
        26) if with_elephant else 0
    for possible_valve in valves_to_go:
        route_length = _find_shortest_route_lenth(
            current_position, possible_valve)
        if route_length > time:
            continue
        time_left = time - route_length - 1
        possible_release = time_left * _valves[possible_valve].flow_rate
        next_release = _find_best_way(
            valves_to_go-{possible_valve},
            possible_valve,
            time_left,
            with_elephant)

        best_possible_release = max(
            best_possible_release, possible_release + next_release)
    return best_possible_release


def find_shortest_route_testing(start, target, valves):
    global _valves
    _valves = valves
    return _find_shortest_route(start, target)


@functools.cache
def _find_shortest_route_lenth(start, target):
    return len(_find_shortest_route(start, target))


def _find_shortest_route(start, target, came_from=None):
    if target in _valves[start].connected_tunnels:
        return [target] if came_from == None else [start, target]

    interect = list(set(_valves[start].connected_tunnels).intersection(
        set(_valves[target].connected_tunnels)))
    if len(interect) > 0:
        return [interect[0], target] if came_from == None else [start, interect[0], target]
    else:
        source = list(came_from) if came_from != None else []
        source.append(start)
        routes = [_find_shortest_route(tunnel, target, frozenset(source))
                  for tunnel in _valves[start].connected_tunnels if tunnel not in source]
        routes = [route for route in routes if route != None]
        if len(routes) == 1:
            return routes[0] if came_from == None else [start] + routes[0]
        elif len(routes) > 1:
            sorted_routes = sorted(routes, key=functools.cmp_to_key(_compare))
            return sorted_routes[:1][0] if came_from == None else [start] + sorted_routes[:1][0]


def _compare(left, right):
    if len(left) < len(right):
        return -1
    if len(left) > len(right):
        return 1
    elif len(left) == 0 and len(right):
        return 0

    left.sort(key=lambda valve: _valves[valve].flow_rate, reverse=True)
    right.sort(key=lambda valve: _valves[valve].flow_rate, reverse=True)

    for index in range(len(left)):
        if _valves[left[index]].flow_rate < _valves[right[index]].flow_rate:
            return -1
        elif _valves[left[index]].flow_rate > _valves[right[index]].flow_rate:
            return 1
    return 0


def run_day():
    print('Day16')
    valves = read_input('input.txt')
    date_time = datetime.now().strftime('%X.%f')
    print(f'{date_time}: released pressure: {open_valves(valves)}')
    date_time = datetime.now().strftime('%X.%f')
    print(f'{date_time}: released pressure: {open_valves(valves, True)}')
