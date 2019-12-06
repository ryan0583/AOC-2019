class Node:
    def __init__(self, name):
        self.name = name
        self.next_node = None

    def get_next_node(self):
        return self.next_node

    def set_next_node(self, next_node):
        self.next_node = next_node

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name


def parse_nodes():
    def create_node():
        def update_next_node():
            _node = node_name_to_node.get(main_obj_name)
            new_node.set_next_node(_node) if _node is not None else new_node.set_next_node(Node(main_obj_name))

        def update_prev_nodes():
            _nodes = next_node_name_to_nodes.get(orbit_obj_name)
            if _nodes is not None:
                for _node in _nodes:
                    _node.set_next_node(new_node)

        new_node = Node(orbit_obj_name)
        update_next_node()
        update_prev_nodes()
        return new_node

    def update_maps():
        node_name_to_node[node.get_name()] = node
        next_node = node.get_next_node()
        if next_node is not None:
            next_node_name = next_node.get_name()
            existing_node_list = next_node_name_to_nodes.get(next_node_name)
            if existing_node_list is None:
                next_node_name_to_nodes[next_node_name] = [node]
            else:
                existing_node_list.append(node)

    node_list = []
    node_name_to_node = {}
    next_node_name_to_nodes = {}
    for orbit in orbit_data:
        split = orbit.split(")")
        main_obj_name = split[0].strip()
        orbit_obj_name = split[1].strip()
        node = create_node()
        node_list.append(node)
        update_maps()

    return node_list


def count_orbits(node_list):
    def count_node_orbits():
        node_count = 0
        next_node = node.get_next_node()
        while next_node is not None:
            node_count += 1
            next_node = next_node.get_next_node()
        return node_count

    count = 0
    for node in node_list:
        count += count_node_orbits()
    return count


def find_node_for_name(node_list, name):
    for node in node_list:
        if node.get_name() == name:
            return node


def get_steps(node):
    steps = {}
    step_count = 0
    next_node = node.get_next_node()
    while next_node is not None:
        steps[next_node.get_name()] = step_count
        step_count += 1
        next_node = next_node.get_next_node()
    return steps


def find_num_transfers(you_node, san_node):
    san_steps = get_steps(san_node)
    san_step_count = None
    you_step_count = 0
    next_node = you_node.get_next_node()

    while san_step_count is None and next_node is not None:
        san_step_count = san_steps.get(next_node.get_name())
        if san_step_count is None:
            you_step_count += 1
            next_node = next_node.get_next_node()

    if san_step_count is not None:
        return you_step_count + san_step_count
    else:
        raise Exception("Failed to find common orbit")


def part1():
    return count_orbits(parse_nodes())


def part2():
    nodes = parse_nodes()
    return find_num_transfers(find_node_for_name(nodes, "YOU"),
                              find_node_for_name(nodes, "SAN"))


debug = False
file = open("input.txt", "r")
orbit_data = file.readlines()
