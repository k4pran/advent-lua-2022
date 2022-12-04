
def to_pairs(line):
    return str.split(line, ',')


def to_bounds(section_range):
    return [int(bound) for bound in str.split(section_range, '-')]


def is_fully_contained(container, contained):
    container_lower, container_upper = to_bounds(container)
    contained_lower, contained_upper = to_bounds(contained)

    return container_upper >= contained_upper and container_lower <= contained_lower

def is_overlapped(container, contained):
    container_lower, container_upper = to_bounds(container)
    contained_lower, contained_upper = to_bounds(contained)

    return {i for i in range(contained_lower, contained_upper + 1)}\
        .intersection({i for i in range(container_lower, container_upper + 1)})

with open("resources/day4.txt", 'r') as f:
    contained_count = 0
    overlap_count = 0
    for line in f.readlines():
        sect_1, sect_2 = to_pairs(line.strip())
        if is_fully_contained(sect_1, sect_2) or is_fully_contained(sect_2, sect_1):
            contained_count += 1
        if is_overlapped(sect_1, sect_2) or is_overlapped(sect_2, sect_1):
            overlap_count += 1

    print("Contained count = " + str(contained_count))
    print("Overlapped count = " + str(overlap_count))