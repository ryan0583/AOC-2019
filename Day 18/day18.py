from Utils.debug_tools import raise_
from Utils.graphics_panel import GraphicsPanel
from Utils.point import Point


class Droid:
    def __init__(self, path, point, direction, keys, doors):
        self.path = list(path)
        self.point = point
        self.direction = direction
        self.keys = keys.copy()
        self.doors = doors.copy()

    def clone(self, direction):
        return Droid(self.path, self.point, direction, self.keys, self.doors)

    def attempt_move(self, maze_map):
        def can_move_to_space(_next_char):
            return _next_char != WALL

        droids_to_add = []
        droids_to_remove = []

        next_point = get_next_point(self.direction, self.point)
        next_char = maze_map[next_point]
        can_move = can_move_to_space(next_char)

        if can_move:
            self.point = next_point
            self.path.append(self.point)
            can_turn_left = can_move_to_space(maze_map[get_next_point(turn_left(self.direction), self.point)])
            can_turn_right = can_move_to_space(maze_map[get_next_point(turn_right(self.direction), self.point)])

            if can_turn_left:
                droids_to_add.append(self.clone(turn_left(self.direction)))

            if can_turn_right:
                droids_to_add.append(self.clone(turn_right(self.direction)))

            if next_char.isupper():
                self.doors.add(CharPoint(next_char, self.point))
            elif next_char.islower():
                self.keys.add(CharPoint(next_char, self.point))
        else:
            droids_to_remove.append(self)

        return droids_to_add, droids_to_remove


class CharPoint:
    def __init__(self, char, point):
        self.char = char
        self.point = point

    def __eq__(self, other):
        return self.point == other.point

    def __str__(self):
        return str(self.point)

    def __hash__(self):
        return hash(str(self))


def get_next_point(direction, current_point):
    direction_switcher = {
        N: lambda: Point(current_point.x, current_point.y - 1),
        S: lambda: Point(current_point.x, current_point.y + 1),
        W: lambda: Point(current_point.x - 1, current_point.y),
        E: lambda: Point(current_point.x + 1, current_point.y)
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


def map_color(char):
    if char == SPACE:
        return "black"
    if char == WALL:
        return "white"
    if char == ENTRY:
        return "blue"
    if char.islower():
        return "yellow"
    if char.isupper():
        return "red"


def get_path(point, other_point, maze_map, panel):
    droids = [Droid([], point, N, set(), set()),
              Droid([], point, S, set(), set()),
              Droid([], point, E, set(), set()),
              Droid([], point, W, set(), set())]

    found_key_droid = None

    droids_to_add = []
    droids_to_remove = []

    while found_key_droid is None:
        for droid in droids:
            panel.update_canvas(droid.point, "black")
            add, remove = droid.attempt_move(maze_map)
            panel.update_canvas(droid.point, "red")
            panel.paint_canvas()
            droids_to_add.extend(add)
            droids_to_remove.extend(remove)
            if CharPoint('', other_point) in droid.keys:
                print("found path from point " + str(point) + " to point " + str(other_point))
                found_key_droid = droid
                break
        droids.extend(droids_to_add)
        droids = list(filter(lambda _droid: _droid not in droids_to_remove, droids))
        droids_to_add = []
        droids_to_remove = []

    return found_key_droid



def part1():
    def get_paths():
        key_path_map = {}
        for key in keys:
            paths = {}
            key_path_map[key] = paths
            for other_key in keys:
                if other_key.point != key.point:
                    paths[other_key] = get_path(key.point, other_key.point, maze_map, panel)
        return key_path_map

    def process_lines():
        lines = open("input.txt", "r").read().splitlines()
        for y, line in enumerate(lines):
            chars = list(line)
            for x, char in enumerate(chars):
                point = Point(x, y)
                if char == ENTRY:
                    start_points.add(CharPoint(char, point))
                    char = SPACE
                if char.islower():
                    keys.add(CharPoint(char, point))
                if char.isupper():
                    doors.add(CharPoint(char, point))
                panel.update_canvas(point, map_color(char))
                maze_map[Point(x, y)] = char

    panel = GraphicsPanel.create_empty_panel(100, 100)
    panel.init_canvas()

    maze_map = {}
    start_points = set()
    keys = set()
    doors = set()

    process_lines()
    get_paths()

    print("DONE!")



N = "N"
S = "S"
W = "W"
E = "E"

WALL = "#"
SPACE = "."
ENTRY = "@"

part1()
