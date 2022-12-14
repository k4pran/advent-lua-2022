from functools import cmp_to_key

def group_packets(l, n):
    grouped_lines = []
    for i in range(0, len(l), n):
        grouped_lines.append(l[i : i + n])
    return grouped_lines


def render_formats(group1, group2):
    if isinstance(group1, list) and not isinstance(group2, list):
        return group1, [group2]
    elif isinstance(group2, list) and not isinstance(group1, list):
        return [group1], group2
    else:
        return group1, group2


def check_sorted(group1, group2):
    for i in range(min(len(group1), len(group2))):

        if isinstance(group1[i], int) and isinstance(group2[i], int):
            if group1[i] == group2[i]:
                continue
            return group1[i] - group2[i]

        g1, g2 = render_formats(group1[i], group2[i])

        sorted = check_sorted(g1, g2)
        if sorted:
            return sorted

    return len(group1) - len(group2)

with open("resources/day13.txt", 'r') as f:
    lines = [l for l in f.read().splitlines() if l != '']
    packet_pairs = group_packets(lines, 2)
    idx = 1
    result = 0
    for pair in packet_pairs:
        packet1, packet2 = render_formats(pair[0], pair[1])

        if check_sorted(eval(pair[0]), eval(pair[1])) < 0:
            result += idx
        idx += 1

    print(result)

    # part 2
    all_packets = [eval(line) for line in lines]
    all_packets += [[[2]], [[6]]]
    sorted_packets = sorted(all_packets, key=cmp_to_key(check_sorted))

    divider_one = sorted_packets.index([[2]]) + 1
    divider_two = sorted_packets.index([[6]]) + 1
    print(divider_one * divider_two)
