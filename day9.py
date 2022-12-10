def move_up(coord):
    return (coord[0], coord[1] + 1)


def move_right(coord):
    return (coord[0] + 1, coord[1])


def move_down(coord):
    return (coord[0], coord[1] - 1)


def move_left(coord):
    return (coord[0] - 1, coord[1])


def move_north_east(coord):
    return (coord[0] + 1, coord[1] + 1)


def move_south_east(coord):
    return (coord[0] + 1, coord[1] - 1)


def move_south_west(coord):
    return (coord[0] - 1, coord[1] - 1)


def move_north_west(coord):
    return (coord[0] - 1, coord[1] + 1)


def move(direction, coord, dist):
    if direction == "U":
        movement_func = move_up
    elif direction == "R":
        movement_func = move_right
    elif direction == "D":
        movement_func = move_down
    elif direction == "L":
        movement_func = move_left
    elif direction == "NE":
        movement_func = move_north_east
    elif direction == "SE":
        movement_func = move_south_east
    elif direction == "SW":
        movement_func = move_south_west
    elif direction == "NW":
        movement_func = move_north_west
    else:
        raise Exception("Invalid move " + direction)

    visited = []
    for _ in range(dist):
        coord = movement_func(coord)
        visited.append(coord)
    return visited


def is_north(head, tail):
    return head[1] > tail[1]


def is_south(head, tail):
    return head[1] < tail[1]


def is_east(head, tail):
    return head[0] > tail[0]


def is_west(head, tail):
    return head[0] < tail[0]


def is_north_east(head, tail):
    return is_north(head, tail) and is_east(head, tail)


def is_south_east(head, tail):
    return is_south(head, tail) and is_east(head, tail)


def is_south_west(head, tail):
    return is_south(head, tail) and is_west(head, tail)


def is_north_west(head, tail):
    return is_north(head, tail) and is_west(head, tail)


def seek(target, source):
    if is_north_east(target, source):
        return move("NE", source, 1)[0]

    if is_south_east(target, source):
        return move("SE", source, 1)[0]

    if is_south_west(target, source):
        return move("SW", source, 1)[0]

    if is_north_west(target, source):
        return move("NW", source, 1)[0]

    if is_north(target, source):
        return move("U", source, 1)[0]

    if is_east(target, source):
        return move("R", source, 1)[0]

    if is_south(target, source):
        return move("D", source, 1)[0]

    if is_west(target, source):
        return move("L", source, 1)[0]


def is_caught_up(head, tail):
    return max(abs(head[0] - tail[0]), abs(head[1] - tail[1])) <= 1


def catchup(head, tail):
    caught_up = is_caught_up(head, tail)
    visited = []
    c = 0
    while not caught_up:
        tail = seek(head, tail)
        visited.append(tail)
        caught_up = is_caught_up(head, tail)
        c += 1
    if c > 1:
        raise Exception("")
    return visited


def catchup(head, tail):
    caught_up = is_caught_up(head, tail)
    visited = []
    while not caught_up:
        tail = seek(head, tail)
        visited.append(tail)
        caught_up = is_caught_up(head, tail)
    return visited


def is_same_coord(head, tail):
    return head[0] == tail[0] and head[1] == tail[1]


def manhattan_dist(head, tail):
    return abs(head[0] - tail[0]) + abs(head[1] - tail[1])


def is_adjacent(head, tail):
    return manhattan_dist(head, tail) == 1


def is_one_space_diagonal(head, tail):
    return abs(head[0] - tail[0]) == abs(head[1] - tail[1])


def get_tail_segments(start, nb_segments):
    return [start for _ in range(-nb_segments, 0)]


def update_tail_segment(head, tail):
    coords_visited = catchup(head, tail)
    if coords_visited:
        tail = coords_visited[-1]
    return tail, coords_visited


def solve(tail_size):
    ORIGIN = (0, 0)
    with open("resources/day9.txt", 'r') as f:
        all_visited = set()
        head_coord = ORIGIN
        tail_coord = get_tail_segments(ORIGIN, tail_size)
        moves = [(line[0], int(line[2:])) for line in f.read().splitlines()]

        for direction, dist in moves:
            for _ in range(dist):
                head_coord = move(direction, head_coord, 1)[-1]

                to_follow = head_coord

                for i in range(tail_size - 1, -1, -1):
                    segment, visited = update_tail_segment(to_follow, tail_coord[i])
                    tail_coord[i] = segment
                    if i == 0:
                        all_visited.update(visited)
                    to_follow = segment
    return len(all_visited) + 1  # add starting pos


print(solve(1))
print(solve(9))

