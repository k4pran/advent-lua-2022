from functools import reduce

WORRY_MODULO = 1

class Monkey:

    def __init__(self, name, items, operation, div_test_number, throw_result, damage_div):
        self.name = name
        self.items = items
        self.div_test_number = div_test_number
        self.throw_result = throw_result
        self.damage_div = damage_div
        self.inspect_count = 0
        self.execute_fn = eval('lambda old: ' + operation)

    def exec_operation(self, old):
        self.inspect_count += 1
        # locals()["old"] = old
        return self.execute_fn(old)


    def update_worry_levels(self):
        levels = []
        for item in self.items:
            levels.append((self.exec_operation(item) // self.damage_div) % WORRY_MODULO)
        self.items = levels

    def do_divisible_test(self, worry_level):
        return worry_level % self.div_test_number == 0

    def get_throw_targets(self):
        targets = []
        self.update_worry_levels()
        for level in self.items:
            targets.append(self.throw_result[self.do_divisible_test(level)])

        return targets


    def remove_all_items(self):
        items = self.items
        self.items = []
        return items

def set_global_modulo(monkeys):
    global WORRY_MODULO
    for monkey in monkeys:
        WORRY_MODULO *= monkey.div_test_number


def parse_monkeys(lines, damage_div):
    lines_per_monkey = 7
    monkeys = []
    for i in range(lines_per_monkey, len(lines) + lines_per_monkey, lines_per_monkey):
        monkey_lines = lines[i - lines_per_monkey: i]
        name = monkey_lines[0].split(" ")[-1][:-1]
        items = [int(i) for i in monkey_lines[1].split("Starting items: ")[-1].split(",")]
        operation = monkey_lines[2].split("Operation: new = ")[-1]
        divisible_test = int(monkey_lines[3].split(" ")[-1])
        throw_result = {
            True: monkey_lines[4].split(" ")[-1],
            False: monkey_lines[5].split(" ")[-1]
        }
        monkeys.append(Monkey(name, items, operation, divisible_test, throw_result, damage_div))
    return monkeys


def get_throw_targets(monkey: Monkey):
    targets = monkey.get_throw_targets()
    items = monkey.remove_all_items()
    return [(items[i], targets[i]) for i in range(len(items))]


def execute_throws(throw_results, monkeys):
    for item, target in throw_results:
        for monkey in monkeys:
            if monkey.name == str(target):
                monkey.items.append(item)


def execute_round(monkeys):
    for monkey in monkeys:
        throw_results = get_throw_targets(monkey)
        execute_throws(throw_results, monkeys)


def execute_notes(monkeys, rounds):
    for i in range(rounds):
        execute_round(monkeys)

with open("resources/day11.txt", 'r') as f:
    lines = f.read().splitlines()
    monkeys = parse_monkeys(lines, 3)
    set_global_modulo(monkeys)
    execute_notes(monkeys, 20)

    inspect_counts = [monkey.inspect_count for monkey in monkeys]
    inspect_counts.sort()
    print(reduce((lambda x, y: x * y), inspect_counts[len(monkeys) - 2:]))

    monkeys = parse_monkeys(lines, 1)
    execute_notes(monkeys, 10000)

    inspect_counts = [monkey.inspect_count for monkey in monkeys]
    inspect_counts.sort()
    print(reduce((lambda x, y: x * y), inspect_counts[len(monkeys) - 2:]))
