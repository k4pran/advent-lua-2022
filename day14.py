
occupied_types = {'#', 'o'}

def get_point(s):
    return tuple(map(int, s.split(",")))


def points_along_line(p1, p2):
    x1, x2 = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
    y1, y2 = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])
    return [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]


def points_along_path(path):
    points = []
    for i in range(1, len(path)):
        points += points_along_line(get_point(path[i - 1]), get_point(path[i]))
    return points


def get_bounding_box(known_points):
    x_vals = [i[0] for i in known_points]
    y_vals = [i[1] for i in known_points]
    return min(x_vals), max(x_vals), min(y_vals), max(y_vals)

def get_rocks(paths):
    rocks = []
    for path in paths:
        rocks += points_along_path(path)
    return rocks


def generate_grid(rocks, sand_sources, minx, maxx, miny, maxy):
    grid = [['.' for _ in range(maxx - minx + 1)] for _ in range(maxy - miny + 1)]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x + minx, y + miny) in rocks:
                grid[y][x] = "#"

    for sand_source in sand_sources:
        grid[sand_source[1] - miny][sand_source[0] - minx] = "+"

    return grid


def print_grid(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            print(grid[x][y] + " ", end='')
        print("\n")


def is_occupied_ahead(grid, loc):
    return grid[loc[0] + 1][loc[1]] in occupied_types


def get_bottom_left(loc):
    return loc[0] + 1, loc[1] - 1

def get_bottom_right(loc):
    return loc[0] + 1, loc[1] + 1

def is_occupied(grid, loc):
    return grid[loc[0]][loc[1]] in occupied_types

def add_sand_if_unoccupied(grid, loc):
    if not is_occupied(grid, loc):
        grid[loc[0]][loc[1]] = 'o'
        return True
    return False


# def fall_and_rest(grid, loc, fall_func):
#     fall_loc = fall_func(loc)
#     if is_occupied(grid, fall_loc):
#         return False
#     while True:
#         next_loc = fall_func(fall_loc)
#         if is_occupied(grid, next_loc):
#             break
#         fall_loc = next_loc
#
#     add_sand_if_unoccupied(grid, fall_loc)
#     return True

def fall(grid, loc, fall_func):
    fall_loc = fall_func(loc)
    return fall_loc if not is_occupied(grid, fall_loc) else None


def sand_fall_step(grid, falling_sand):
    fall_loc = fall(grid, falling_sand, get_bottom_left)
    if fall_loc:
        return sand_fall_step(grid, fall_loc)

    fall_loc = fall(grid, falling_sand, get_bottom_right)
    if fall_loc:
        return sand_fall_step(grid, fall_loc)

    if not is_occupied(grid, falling_sand):
        return falling_sand

    return None


def perform_simulation(grid, sand_source):
    falling_sand = sand_source[0], sand_source[1]
    sand_units = 0
    while True:
        # if falling_sand[1] < 0 or falling_sand[0] + 1 >= len(grid):
        #     return sand_units
        if is_occupied_ahead(grid, falling_sand):
            # if falling_sand[0] <= 0:
            #     return sand_units
            new_loc = fall(grid, falling_sand, get_bottom_left)
            if new_loc:
                falling_sand = new_loc
                continue

            new_loc = fall(grid, falling_sand, get_bottom_right)
            if new_loc:
                falling_sand = new_loc
                continue

            if not is_occupied(grid, falling_sand):
                add_sand_if_unoccupied(grid, falling_sand)
                sand_units += 1
            else:
                return sand_units

            falling_sand = sand_source[0] + 1, sand_source[1]
        else:
            falling_sand = falling_sand[0] + 1, falling_sand[1]



with open("resources/day14.txt", 'r') as f:
    lines = [line.replace(' ', '').split("->") for line in f.read().splitlines()]
    rocks = get_rocks(lines)
    sand_source = (500, -1)
    minx, maxx, miny, maxy = get_bounding_box(rocks + [sand_source])
    grid = generate_grid(rocks, [sand_source], minx, maxx, miny, maxy)
    sand_units = perform_simulation(grid, (sand_source[1] - miny, sand_source[0] - minx))
    # print_grid(grid)
    print(sand_units)

    # part 2
    # It worked after a long wait ... :/
    minx -= 500
    maxx += 500
    maxy += 2
    rocks += [(x, maxy) for x in range(minx, maxx + 1)]
    grid = generate_grid(rocks, [sand_source], minx, maxx, miny, maxy)
    sand_units = perform_simulation(grid, (sand_source[1] - miny, sand_source[0] - minx))
    print(sand_units)