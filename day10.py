


with open("resources/day10.txt", 'r') as f:

    x = 1
    cycle_stops = [20, 60, 100, 140, 180, 220]
    signal_strengths = 0
    cycles = 0
    pixels = [["-" for _ in range(40)] for _ in range(len(cycle_stops))]
    i_index = x
    j_index = 0
    for line in f.read().splitlines():
        if line.startswith("addx"):
            if cycle_stops and cycles + 2 >= cycle_stops[0]:
                signal_strengths += cycle_stops[0] * x
                cycle_stops = cycle_stops[1:]

            add_val = line.split(" ")[-1]
            x += int(add_val)
            cycles += 2
        else:
            if cycle_stops and cycles + 1 >= cycle_stops[0]:
                signal_strengths += cycle_stops[0] * x
                cycle_stops = cycle_stops[1:]
            cycles += 1


    print(signal_strengths)


def draw_pixel(pixel):
    print(pixel, end='')


def get_pixel(crt_pos, x_pos):
    if abs(crt_pos - x_pos) <= 1:
        return "#"
    return "."


def next_row():
    print("\n", end='')


def update_crt(crt, cycle):
    if cycle % 40 == 0:
        next_row()
        return 0
    return crt + 1


def update_x(x, x_add):
    return x + x_add


def solve(lines):

    cycle = 0
    x = 1
    crt_pos = 0
    for line in lines:
        if line.startswith("addx"):
            cycle += 1
            draw_pixel(get_pixel(crt_pos, x))
            crt_pos = update_crt(crt_pos, cycle)

            cycle += 1
            draw_pixel(get_pixel(crt_pos, x))
            crt_pos = update_crt(crt_pos, cycle)

            x = update_x(x, int(line.split(" ")[-1]))

        else:
            cycle += 1
            draw_pixel(get_pixel(crt_pos, x))
            crt_pos = update_crt(crt_pos, cycle)


with open("resources/day10.txt", 'r') as f:
    solve(f.read().splitlines())
