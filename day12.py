GOAL_FOUND = False


def get_grid_nb(x):
    if x == 'S':
        return 1
    elif x == 'E':
        return 'E'
    else:
        return ord(x) - 97


def draw_grid(lines):
    return [[get_grid_nb(x) for x in line] for line in lines]


def get_height(grid, pos):
    return grid[pos[0]][pos[1]]


def get_north(grid, pos):
    if pos[1] > 0:
        return get_height(grid, (pos[0], pos[1] - 1))

def get_south(grid, pos):
    if pos[1] < len(grid[0]) - 1:
        return get_height(grid, (pos[0], pos[1] + 1))


def get_west(grid, pos):
    if pos[0] > 0:
        return get_height(grid, (pos[0] - 1, pos[1]))


def get_east(grid, pos):
    if pos[0] < len(grid) - 1:
        return get_height(grid, (pos[0] + 1, pos[1]))


def is_goal(grid, pos):
    return get_north(grid, pos) == "E" or get_south(grid, pos) == "E" or get_east(grid, pos) == "E" or get_west(grid,
                                                                                                                pos) == "E"

def get_allowed_actions(grid, pos):
    if is_goal(grid, pos):
        return ["E"]

    current_height = get_height(grid, pos)
    allowed_actions = []
    north = get_north(grid, pos)
    south = get_south(grid, pos)
    west = get_west(grid, pos)
    east = get_east(grid, pos)

    if north is not None and north <= current_height + 1:
        allowed_actions.append((pos[0], pos[1] - 1))
    if south is not None and south <= current_height + 1:
        allowed_actions.append((pos[0], pos[1] + 1))
    if west is not None and west <= current_height + 1:
        allowed_actions.append((pos[0] - 1, pos[1]))
    if east is not None and east <= current_height + 1:
        allowed_actions.append((pos[0] + 1, pos[1]))
    return allowed_actions


def find_min_steps(grid, starting_position, max_moves=500):
    dest_found = False
    visited = set()
    moves = 0
    positions = [starting_position]
    while not dest_found:
        next_positions = []
        for pos in positions:
            new_positions = list(set(get_allowed_actions(grid, pos)).difference(visited))
            if new_positions and new_positions[0] == "E":
                return moves + 1
            next_positions += new_positions
            visited.update(new_positions)
        if moves >= max_moves:
            return moves
        positions = next_positions
        moves += 1


def find_min_steps_from_a(grid):
    starting_positions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                starting_positions.append((i, j))
    move_record = []
    for start in starting_positions:
        move_record.append(find_min_steps(grid, start))
    return move_record


with open("resources/day12.txt", 'r') as f:
    lines = f.read().splitlines()
    grid = draw_grid(lines)

    print(find_min_steps(grid, (0, 0)))
    results = find_min_steps_from_a(grid)
    results.sort()
    print(results)  # some false positives so bug in this
