def get_faces(cube, size=1):
    half_size = size / 2
    return {(cube[0] - half_size, cube[1], cube[2]),
            (cube[0] + half_size, cube[1], cube[2]),
            (cube[0], cube[1] - half_size, cube[2]),
            (cube[0], cube[1] + half_size, cube[2]),
            (cube[0], cube[1], cube[2] - half_size),
            (cube[0], cube[1], cube[2] + half_size)}


def get_adjacent_cubes(cube):
    return ((cube[0] - 1, cube[1], cube[2]),
            (cube[0] + 1, cube[1], cube[2]),
            (cube[0], cube[1] - 1, cube[2]),
            (cube[0], cube[1] + 1, cube[2]),
            (cube[0], cube[1], cube[2] - 1),
            (cube[0], cube[1], cube[2] + 1))


def get_corners(cube, size=1):
    half_size = size / 2
    return {(cube[0] + half_size, cube[1] + half_size, cube[2] + half_size),
            (cube[0] + half_size, cube[1] + half_size, cube[2] - half_size),
            (cube[0] + half_size, cube[1] - half_size, cube[2] + half_size),
            (cube[0] + half_size, cube[1] - half_size, cube[2] - half_size),
            (cube[0] - half_size, cube[1] + half_size, cube[2] + half_size),
            (cube[0] - half_size, cube[1] + half_size, cube[2] - half_size),
            (cube[0] - half_size, cube[1] - half_size, cube[2] + half_size),
            (cube[0] - half_size, cube[1] - half_size, cube[2] + half_size)}


def is_air_pocket(path, min_values, max_values):
    minx, miny, minz = min_values
    maxx, maxy, maxz = max_values
    for point in path:
        x, y, z = point
        if x <= minx or x >= maxx:
            return False
        if y <= miny or y >= maxy:
            return False
        if z <= minz or z >= maxz:
            return False
    return True


# def find_farthest_point(current_position, cubes, visited_cubes, mins, maxes): NOPE
#
#     visited_cubes.add(current_position)
#     min_x, min_y, min_z = mins
#     max_x, max_y, max_z = maxes
#     for cube in get_adjacent_cubes(current_position):
#         if cube in cubes:
#             continue
#         if cube[0] < min_x or cube[0] > max_x:
#             return cube
#         if cube[1] < min_y or cube[1] > max_y:
#             return cube
#         if cube[2] < min_z or cube[2] > max_z:
#             return cube
#         if cube not in visited_cubes:
#             visited_cubes.add(cube)
#             current_position = find_farthest_point(cube, cubes, visited_cubes, mins, maxes)
#     return current_position


# got most of this idea for reddit when recursion failed
def find_farthest(start, cubes, min_values, max_values):
    queue = [start]
    distances = {}
    distances[start] = 0
    minx, miny, minz = min_values
    maxx, maxy, maxz = max_values

    while queue:
        current_position = queue.pop(0)
        for adj_position in get_adjacent_cubes(current_position):
            if adj_position[0] < minx or adj_position[0] > maxx:
                continue
            if adj_position[1] < miny or adj_position[1] > maxy:
                continue
            if adj_position[2] < minz or adj_position[2] > maxz:
                continue
            if adj_position in cubes:
                continue
            if adj_position in distances:
                continue
            distances.setdefault(adj_position, 0)
            distances[adj_position] = distances[current_position] + 1
            queue.append(adj_position)
    return distances


with open("resources/day18.txt", 'r') as f:
    cubes = [tuple(map(int, cube.split(","))) for cube in f.read().splitlines()]

    all_faces = {}
    count = 0
    for cube in cubes:
        for face in get_faces(cube):
            if face not in all_faces:
                all_faces[face] = 0
            all_faces[face] += 1

    surface = [k for k, v in all_faces.items() if v == 1]
    print(len(surface))

    # part 2

    maxx = max(f[0] for f in cubes)
    maxy = max(f[1] for f in cubes)
    maxz = max(f[2] for f in cubes)
    minx = min(f[0] for f in cubes)
    miny = min(f[1] for f in cubes)
    minz = min(f[2] for f in cubes)

    mins = [minx, miny, minz]
    maxes = [maxx, maxy, maxz]
    interior_sides = 0
    pockets = set()
    non_pockets = set()
    for cube in cubes:
        for adj_cube in get_adjacent_cubes(cube):
            if adj_cube in cubes:
                interior_sides += 1
            elif adj_cube not in pockets and adj_cube not in non_pockets:
                path = find_farthest(adj_cube, cubes, mins, maxes)
                if is_air_pocket(path, mins, maxes):
                    pockets.update([key for key in path])
                else:
                    non_pockets.update([key for key in path])
            if adj_cube in pockets:
                interior_sides += 1

    print((len(cubes) * 6) - interior_sides)
