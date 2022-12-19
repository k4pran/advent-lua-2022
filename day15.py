def manhattan_dist(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def get_bounding_points(points):
    x_vals = [i[0] for i in points]
    y_vals = [i[1] for i in points]
    return min(x_vals), max(x_vals), min(y_vals), max(y_vals)


def get_x_coverage(sensor, beacon, y):
    dist = manhattan_dist(sensor, beacon)
    x_coverage = dist - abs(y - sensor[1])
    if dist >= 0:
        return [x_1 for x_1 in range(sensor[0] - x_coverage, sensor[0] + x_coverage + 1)]
    return []


def get_x_intervals(sensor, beacon, y, minx, maxx):
    dist = manhattan_dist(sensor, beacon)
    x_coverage = dist - abs(y - sensor[1])
    if dist >= 0:
        left, right = max(minx, min(maxx, sensor[0] - x_coverage)), max(minx, min(maxx,  sensor[0] + x_coverage))
        if right < left:
            return []
        return left, right
    return []


# nabbed this algorithm as mine was too slow
def get_interval_coverage(sorted_intervals, maxx):
    top = -1
    for interval in sorted_intervals:
        if top >= maxx:
            return -1
        if top + 1 < interval[0]:
            return top + 1
        if interval[1] > top:
            top = interval[1]
    return -1


with open("resources/day15.txt", 'r') as f:
    lines = f.read().splitlines()
    sensors = []
    beacons = []
    for line in lines:
        split_line = line.split(" ")
        sensor, beacon = (int(split_line[2][2:-1]), int(split_line[3][2:-1])), (int(split_line[-2][2:-1]), int(split_line[-1][2:]))
        sensors.append(sensor)
        beacons.append(beacon)

    minx, maxx, miny, maxy = get_bounding_points(sensors + beacons)
    Y = 2000000
    invalid_beacon_positions = set()
    for i in range(len(sensors)):
        invalid_beacon_positions.update([(x, Y) for x in (get_x_coverage(sensors[i], beacons[i], Y))])


    invalid_beacon_positions.difference_update(set(beacons))
    print(len(invalid_beacon_positions))

    # Part 2
    dim = 4000000
    for row in range(0, dim):
        invalid_beacon_intervals = set()
        for i in range(len(sensors)):
            interval = get_x_intervals(sensors[i], beacons[i], row, 0, dim)
            if interval:
                invalid_beacon_intervals.add(interval)

        coverage = get_interval_coverage(sorted(invalid_beacon_intervals, key=lambda t: (t[0], -t[1])), dim)
        if coverage >= 0:
            print(dim * coverage + row)


