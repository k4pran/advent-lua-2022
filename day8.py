def read_grid(data):
    return [[int(i) for i in j] for j in data]


def is_edge(grid, row, col):
    return row == 0 or col == 0 or row == len(grid) - 1 or col == len(grid[0]) - 1


def get_left_trees(grid, row, col):
    return grid[row][:col]

def get_right_trees(grid, row, col):
    return grid[row][col + 1:]

def get_up_trees(grid, row, col):
    return [r[col] for r in grid[:row]]

def get_down_trees(grid, row, col):
    return [r[col] for r in grid[row + 1:]]

def is_left_visible(grid, row, col):
    return all([x < grid[row][col] for x in get_left_trees(grid, row, col)])


def is_right_visible(grid, row, col):
    return all([x < grid[row][col] for x in get_right_trees(grid, row, col)])


def is_up_visible(grid, row, col):
    return all([x < grid[row][col] for x in get_up_trees(grid, row, col)])


def is_down_visible(grid, row, col):
    return all([x < grid[row][col] for x in get_down_trees(grid, row, col)])

def is_visible_anywhere(grid, row, col):
    if is_edge(grid, row, col):
        return True
    return is_left_visible(grid, row, col) or \
           is_right_visible(grid, row, col) or \
           is_up_visible(grid, row, col) or \
           is_down_visible(grid, row, col)


def get_score(trees, current_tree_height):
    visible_tree_count = 0
    trees = [i for i in trees]
    for tree in trees:
        if tree >= current_tree_height:
            visible_tree_count += 1
            break
        visible_tree_count += 1
    return visible_tree_count


def get_scenic_score(grid, row, col):
    return get_score(reversed(get_left_trees(grid, row, col)), grid[row][col]) * \
           get_score(get_right_trees(grid, row, col), grid[row][col]) * \
           get_score(reversed(get_up_trees(grid, row, col)), grid[row][col]) * \
           get_score(get_down_trees(grid, row, col), grid[row][col])


with open("resources/day8.txt", 'r') as f:
    grid = read_grid(f.read().splitlines())

    visible_trees = 0
    highest_scenic_score = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if is_visible_anywhere(grid, row, col):
                visible_trees += 1
            scenic_score = get_scenic_score(grid, row, col)
            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score

    print("Trees visible from anywhere = " + str(visible_trees))
    print("Highest scenic score = " + str(highest_scenic_score))