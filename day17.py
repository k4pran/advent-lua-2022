from collections import deque

import numpy as np


def get_horizontal_line_shape():
    return np.array([[-3, 2], [-3, 3], [-3, 4], [-3, 5]])


def get_plus_shape():
    return np.array([[-5, 3], [-4, 2], [-4, 3], [-4, 4], [-3, 3]])


def get_corner_shape():
    return np.array([[-5, 4], [-4, 4], [-3, 2], [-3, 3], [-3, 4]])


def get_vertical_line_shape():
    return np.array([[-6, 2], [-5, 2], [-4, 2], [-3, 2]])


def get_box_shape():
    return np.array([[-4, 2], [-4, 3], [-3, 2], [-3, 3]])


def generate_grid(height, width):
    return [[_ for _ in range(width)] for _ in range(height)]


def jet_push(rocks, shape, direction, grid_cols):
    if direction == '>':
        if not collision_check(rocks, shape, (0, 1)):
            shape[:, 1] = shape[:, 1] + 1 if max(shape[:, 1]) < grid_cols - 1 else shape[:, 1]
    else:
        if not collision_check(rocks, shape, (0, -1)):
            shape[:, 1] = shape[:, 1] - 1 if min(shape[:, 1]) > 0 else shape[:, 1]
    return shape


def collision_check(rocks: set, shape, vector):
    return len(rocks.intersection({(point[0] + vector[0], point[1] + vector[1]) for point in shape.tolist()})) != 0


def fall(shape):
    shape[:, 0] = shape[:, 0] + 1
    return shape


def set_vertical_position(shape, highest_rock, dist):
    bottom_edge = max(shape[:, 0])
    shape[:, 0] = shape[:, 0] - (bottom_edge + (dist + highest_rock))
    return shape

def get_shape_top_edge(shape):
    return min(shape[:, 0])

def get_shape_bottom_edge(shape):
    return max(shape[:, 0])

def prepend_to_file(rocks, width):
    with open("day17_visual.txt", 'r+') as f:
        f.seek(0, 0)
        top = min([i[0] for i in rocks])
        bottom = max([i[0] for i in rocks])
        for row in range(top, bottom + 1):
            for col in range(width):
                if (row, col) in rocks:
                    f.write("#")
                else:
                    f.write(" ")
            f.write("\n")



# Part 1
# with open("resources/day17.txt", 'r') as f:
#     open("day17_visual.txt", 'w').close()
#     push_vectors = f.read().splitlines()[0]
#
#     shape_generators = [get_horizontal_line_shape, get_plus_shape, get_corner_shape, get_vertical_line_shape, get_box_shape]
#
#     grid_width = 7
#     step = 0
#     current_shape_index = 0
#     current_shape = shape_generators[current_shape_index]()
#     floor = {(1, col) for col in range(0, grid_width)}
#     rocks = set()
#     highest_rock = 0
#     target_rocks = 2022
#     starting_vertical_dist = 4
#     while True:
#         current_shape = jet_push(rocks, current_shape, push_vectors[step % len(push_vectors)], grid_width)
#         if collision_check(rocks.union(floor), current_shape, (1, 0)):
#             rocks.update({tuple(i) for i in current_shape.tolist()})
#             highest_rock = abs(min([i[0] for i in rocks]))
#             prepend_to_file(rocks, grid_width)
#             current_shape_index += 1
#             if current_shape_index == target_rocks:
#                 print(highest_rock + 1)
#                 break
#             current_shape = set_vertical_position(shape_generators[current_shape_index % len(shape_generators)](), highest_rock, starting_vertical_dist)
#         else:
#             fall(current_shape)
#         step += 1
#
#
# def get_cycle_sig(rocks, width):
#     top = min([i[0] for i in rocks])
#     bottom = max([i[0] for i in rocks])
#     sig = ""
#     for row in range(top, bottom + 1):
#         for col in range(width):
#             if (row, col) in rocks:
#                 sig += str(row) + str(col)
#     return sig


# part 2
with open("resources/day17.txt", 'r') as f:
    # open("day17_visual.txt", 'w').close()
    push_vectors = f.read().splitlines()[0]

    shape_generators = [get_horizontal_line_shape, get_plus_shape, get_corner_shape, get_vertical_line_shape, get_box_shape]

    grid_width = 7
    step = 0
    current_shape_index = 0
    current_shape = shape_generators[current_shape_index]()
    floor = {(1, col) for col in range(0, grid_width)}
    rocks = set()
    highest_rock = 0
    # write a bigger file and manually search for a cycle :/
    # 3 - 2086 complete cycle
    # 364 cycle begins
    cycle_length = 2086 - 3
    starting_vertical_dist = 4
    start_count = 364

    cycle_start_height = 0
    cycle_length_height = 0
    while True:
        current_shape = jet_push(rocks, current_shape, push_vectors[step % len(push_vectors)], grid_width)
        if collision_check(rocks.union(floor), current_shape, (1, 0)):
            rocks.update({tuple(i) for i in current_shape.tolist()})
            highest_rock = abs(min([i[0] for i in rocks]))
            # prepend_to_file(rocks, grid_width)
            current_shape_index += 1
            if current_shape_index == start_count:
                cycle_start_height = highest_rock
            if current_shape_index == start_count + cycle_length:
                cycle_length_height = highest_rock - cycle_start_height
                print(highest_rock)
                break
            current_shape = set_vertical_position(shape_generators[current_shape_index % len(shape_generators)](), highest_rock, starting_vertical_dist)
        else:
            fall(current_shape)
        step += 1

    # print(cycle_start_height)
    # print(cycle_length_height)
    #
    # print(((100000000000 - start_count) / 2086) * cycle_length_height)
    # 1540804597682
    print(cycle_start_height + (cycle_length_height * (100000000000 - start_count) // cycle_length))