from Utils.debug_tools import raise_
from Utils.graphics_panel import GraphicsPanel
from Utils.intcode_computer import IntcodeComputer
from Utils.point import Point


class Droid:
    def __init__(self, brain, point, direction, path):
        self.brain = brain
        self.point = point
        self.direction = direction
        self.path = list(path)
        self.last_output = None
        self.is_blocked = False

    def move(self):
        self.brain.replace_next_input(self.direction)
        self.last_output = self.brain.process()
        if self.last_output == BLOCKED:
            self.is_blocked = True
        elif self.last_output == MOVED:
            self.path.append(self.point)
            self.point = get_next_point(self.direction, self.point)


def get_next_point(direction, current_point):
    direction_switcher = {
        N: lambda: Point(current_point.x, current_point.y - 1),
        S: lambda: Point(current_point.x, current_point.y + 1),
        W: lambda: Point(current_point.x - 1, current_point.y),
        E: lambda: Point(current_point.x + 1, current_point.y)
    }
    return direction_switcher.get(direction, lambda: raise_("Invalid direction: " + direction))()


def print_direction(direction):
    direction_switcher = {
        N: lambda: print("N"),
        S: lambda: print("S"),
        W: lambda: print("W"),
        E: lambda: print("E")
    }
    return direction_switcher.get(direction, lambda: raise_("Invalid direction: " + direction))()


def turn_right(direction):
    direction_switcher = {
        N: lambda: E,
        S: lambda: W,
        W: lambda: N,
        E: lambda: S
    }
    return direction_switcher.get(direction, lambda: raise_("Invalid direction: " + direction))()


def turn_left(direction):
    direction_switcher = {
        N: lambda: W,
        S: lambda: E,
        W: lambda: S,
        E: lambda: N
    }
    return direction_switcher.get(direction, lambda: raise_("Invalid direction: " + direction))()


def update_panel(point, color, graphics_panel):
    normalised_point = Point(22 + point.x, 22 + point.y)
    graphics_panel.update_canvas(normalised_point, color)


def part1():
    def add_right_droid(_droids, _droid):
        next_right_position = get_next_point(turn_right(_droid.direction), _droid.point)
        if next_right_position not in checked_points and next_right_position not in blocked_points:
            _droids.append(
                Droid(IntcodeComputer.copy(_droid.brain), _droid.point, turn_right(_droid.direction), _droid.path))

    def add_left_droid(_droids, _droid):
        next_left_position = get_next_point(turn_left(_droid.direction), _droid.point)
        if next_left_position not in checked_points and next_left_position not in blocked_points:
            _droids.append(
                Droid(IntcodeComputer.copy(_droid.brain), _droid.point, turn_left(_droid.direction), _droid.path))

    def move_droids(_droids, move_color):
        _o2_tank_point = None
        _path = None
        _final_droid = None
        _droids_to_add = []

        for _droid in _droids:
            checked_points.add(_droid.point)
            _droid.move()
            if _droid.last_output == MOVED:
                update_panel(_droid.point, move_color, graphics_panel)
            elif _droid.last_output == BLOCKED:
                blocked_points.add(get_next_point(_droid.direction, _droid.point))
                update_panel(get_next_point(_droid.direction, _droid.point), BLOCKED_COLOR, graphics_panel)
            elif _droid.last_output == FOUND_O2_SYSTEM:
                _o2_tank_point = get_next_point(_droid.direction, _droid.point)
                update_panel(_o2_tank_point, O2_COLOR, graphics_panel)
                _path = _droid.path
                _final_droid = _droid

            add_right_droid(_droids_to_add, _droid)

            add_left_droid(_droids_to_add, _droid)

        _droids.extend(_droids_to_add)
        _droids = list(filter(lambda _droid: _droid.point not in checked_points and _droid.point not in blocked_points,
                              _droids))

        graphics_panel.paint_canvas()
        return _droids, _o2_tank_point, _path, _final_droid

    tile_map = {}
    for x in range(0, 43):
        for y in range(0, 43):
            tile_map[Point(x, y)] = "black"

    graphics_panel = GraphicsPanel(tile_map)
    graphics_panel.init_game()
    graphics_panel.paint_canvas()

    current_point = Point(0, 0)
    checked_points = set()
    blocked_points = set()

    update_panel(current_point, DROID_COLOR, graphics_panel)
    graphics_panel.paint_canvas()

    droids = [Droid(IntcodeComputer([], "input.txt", True), current_point, N, [current_point]),
              Droid(IntcodeComputer([], "input.txt", True), current_point, S, [current_point]),
              Droid(IntcodeComputer([], "input.txt", True), current_point, E, [current_point]),
              Droid(IntcodeComputer([], "input.txt", True), current_point, W, [current_point])]

    path = None
    o2_tank_point = None
    final_droid = None

    while path is None:
        droids, o2_tank_point, path, final_droid = move_droids(droids, DROID_COLOR)
        graphics_panel.paint_canvas()
        # time.sleep(.1)

    graphics_panel.paint_canvas()
    print("Path to O2 system is " + str(len(path)) + " steps")
    print("O2 tank is at " + str(o2_tank_point))

    checked_points = set()
    current_droid_position = get_next_point(final_droid.direction, final_droid.point)
    droids = [Droid(IntcodeComputer.copy(final_droid.brain), current_droid_position, N, [o2_tank_point]),
              Droid(IntcodeComputer.copy(final_droid.brain), current_droid_position, S, [o2_tank_point]),
              Droid(IntcodeComputer.copy(final_droid.brain), current_droid_position, E, [o2_tank_point]),
              Droid(IntcodeComputer.copy(final_droid.brain), current_droid_position, W, [o2_tank_point])]

    minutes = -1
    while len(droids) > 0:
        minutes += 1
        droids, o2_tank_point, path, final_droid = move_droids(droids, O2_COLOR)

    print("Filled with O2 after: " + str(minutes) + " minutes")
    input("Press any key...")


N = 1
S = 2
W = 3
E = 4

RIGHT = 0
LEFT = 1
NONE = 3

BLOCKED = 0
MOVED = 1
FOUND_O2_SYSTEM = 2

EMPTY_COLOR = "black"
DROID_COLOR = "red"
BLOCKED_COLOR = "yellow"
O2_COLOR = "blue"

part1()
