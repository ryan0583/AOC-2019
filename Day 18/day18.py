from collections import OrderedDict

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

            if next_char.isupper() and CharPoint(next_char, self.point) not in self.doors:
                self.doors.add(CharPoint(next_char, self.point))
            elif next_char.islower() and CharPoint(next_char, self.point) not in self.keys:
                self.keys[CharPoint(next_char, self.point)] = None
        else:
            droids_to_remove.append(self)

        return droids_to_add, droids_to_remove


class CharPoint:
    def __init__(self, char, point):
        self.char = char
        self.point = point

    def __eq__(self, other):
        return self.char == other.char \
               and self.point == other.point

    def __str__(self):
        return self.char + ", " + str(self.point)

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


def all_keys_found(droids, keys):
    return len(list(filter(lambda droid: len(droid.keys) == len(keys), droids))) >= 1


def get_path(start_key, start_point, maze_map, panel, keys):
    def map_keys():
        for _droid in droids:
            for key in _droid.keys:
                existing_path = paths.get(key)
                if existing_path is None:
                    paths[key] = _droid.clone(_droid.direction)

    start_keys = OrderedDict()
    if start_key is not None:
        start_keys[start_key] = None

    droids = [Droid([], start_point, N, start_keys, set()),
              Droid([], start_point, S, start_keys, set()),
              Droid([], start_point, E, start_keys, set()),
              Droid([], start_point, W, start_keys, set())]

    paths = {}
    visited_points = {start_point}
    droids_to_add = []
    droids_to_remove = []

    while len(paths.keys()) < len(keys):
        for droid in droids:
            panel.update_canvas(droid.point, "black")
            add, remove = droid.attempt_move(maze_map)
            visited_points.add(droid.point)
            panel.update_canvas(droid.point, "blue")
            panel.paint_canvas()
            droids_to_add.extend(add)
            droids_to_remove.extend(remove)

        droids.extend(droids_to_add)
        droids = list(filter(lambda _droid: _droid not in droids_to_remove, droids))
        droids = list(
            filter(lambda _droid: get_next_point(_droid.direction, _droid.point) not in visited_points, droids))
        map_keys()
        droids_to_add = []
        droids_to_remove = []

    return paths


def print_key_path(key_path):
    for key_path_key in key_path.keys():
        print(key_path_key)


def part1():
    def get_paths():
        key_path_map = {}
        for key in keys:
            # print("\n\n")
            # print(key)
            key_path_map[key] = get_path(key, key.point, maze_map, panel, keys)
            # print_key_path(key_path_map[key])

        for start_pos in start_points:
            # print("\n\n")
            # print(start_pos)
            key_path_map[start_pos] = get_path(None, start_pos.point, maze_map, panel, keys)
            # print_key_path(key_path_map[start_pos])

        # for each key, remove paths to any other keys where the keys list is more than 2
        # (or more than one for the start key)
        # for key in key_path_map.keys():
        #     _key_paths = key_path_map.get(key)
        #     num_keys_wanted = 2
        #     if key == next(iter(start_points)):
        #         num_keys_wanted = 1
        #     keys_to_delete = []
        #     for path_key in _key_paths.keys():
        #         if len(_key_paths.get(path_key).keys) > num_keys_wanted:
        #             keys_to_delete.append(path_key)
        #
        #     for key_to_delete in keys_to_delete:
        #         del _key_paths[key_to_delete]

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

    def have_all_keys(_doors, _keys):
        key_chars = set(map(lambda key: key.char, _keys.keys()))
        have_keys = True
        for door in _doors:
            if door.char.lower() not in key_chars:
                have_keys = False
                break
        return have_keys

    panel = GraphicsPanel.create_empty_panel(100, 100)
    panel.init_canvas()

    maze_map = {}
    start_points = set()
    keys = set()
    doors = set()

    process_lines()
    key_paths = get_paths()

    start_point = next(iter(start_points))
    # start_paths = key_paths.get(start_point)
    # print(print_key_path(start_paths))

    next_char_point = start_point
    next_paths = key_paths[next_char_point]
    next_droids = []
    for next_path_key in next_paths.keys():
        next_droid = next_paths[next_path_key]
        if len(next_droid.doors) == 0:
            next_droids.append(next_droid.clone(next_droid.direction))

    complete_paths = []

    next_next_droids = []
    while len(next_droids) > 0:
        next_next_droids = []
        for next_droid in next_droids:
            collected_keys = next_droid.keys
            next_key = list(next_droid.keys.keys())[len(next_droid.keys) - 1]
            next_paths = key_paths[next_key]
            for next_path_key in next_paths.keys():
                if next_path_key in next_droid.keys.keys():
                    continue
                next_next_droid = next_paths[next_path_key]
                next_next_doors = next_next_droid.doors
                if have_all_keys(next_next_doors, collected_keys):
                    next_next_droid = next_next_droid.clone(next_next_droid.direction)
                    additional_path = list(next_next_droid.path)
                    next_next_droid.path = list(next_droid.path)
                    next_next_droid.path.extend(additional_path)

                    additional_keys = next_next_droid.keys.copy()
                    next_next_droid.keys = next_droid.keys.copy()
                    next_next_droid.keys.update(additional_keys)

                    additional_doors = next_next_droid.doors.copy()
                    next_next_droid.doors = next_droid.doors.copy()
                    next_next_droid.doors.update(additional_doors)

                    print(len(next_next_droid.keys))
                    if len(next_next_droid.keys) == len(keys):
                        print(len(next_next_droid.path))
                        # for point in next_next_droid.path:
                        #     print(point)
                        print(list(map(lambda key: key.char, next_next_droid.keys.keys())))
                        print("\n\n")
                        complete_paths.append(next_next_droid.path)
                        return

                    next_next_droids.append(next_next_droid)

        next_droids = list(next_next_droids)

    print(min(list(map(lambda path: len(path), complete_paths))))
    print("DONE!")


N = "N"
S = "S"
W = "W"
E = "E"

WALL = "#"
SPACE = "."
ENTRY = "@"

part1()
