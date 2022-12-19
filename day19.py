import re
import random

ORE = "ore"
CLAY = "clay"
OBISIDIAN = "obsidian"
GEODE = "geode"


class RobotFactory:

    def __init__(self, blueprint, ore_robo_cost, clay_robo_cost, obsidian_robo_cost, geode_robo_cost):
        self.blueprint = blueprint

        self.ore_robo_cost = ore_robo_cost
        self.clay_robo_cost = clay_robo_cost
        self.obsidian_robo_cost = obsidian_robo_cost
        self.geode_robo_cost = geode_robo_cost

        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geodes_robots = 0

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        self.ore_bot_building = False
        self.clay_bot_building = False
        self.obsidian_bot_building = False
        self.geode_bot_building = False

        self.random_build = [self.build_ore_robot, self.build_clay_robot, self.build_obsidian_robot]


    def reset(self):
        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geodes_robots = 0

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

    def activate_robots(self):
        if self.ore_bot_building:
            self.ore_robots += 1
            self.ore_bot_building = False

        if self.clay_bot_building:
            self.clay_robots += 1
            self.clay_bot_building = False

        if self.obsidian_bot_building:
            self.obsidian_robots += 1
            self.obsidian_bot_building = False

        if self.geode_bot_building:
            self.geodes_robots += 1
            self.geode_bot_building = False


    def step(self):
        self.execute_strategy()

        self.ore += self.ore_robots
        # print(f"{self.ore_robots} ore robots collect {self.ore_robots} ore. You have {self.ore}")
        self.clay += self.clay_robots

        # print(f"{self.clay_robots} clay robots collect {self.clay_robots} clay. You have {self.clay}")
        self.obsidian += self.obsidian_robots

        # print(f"{self.obsidian_robots} obsidian robots collect {self.obsidian_robots} obsidian. You have {self.obsidian}")
        self.geodes += self.geodes_robots

        # print(f"{self.geodes_robots} geode robots crack {self.geodes_robots} geodes. You have {self.geodes}")
        # print("\n")

        self.activate_robots()


    def use_resources(self, costs):
        for k, v in costs.items():
            if k == ORE:
                self.ore -= v
            elif k == CLAY:
                self.clay -= v
            elif k == OBISIDIAN:
                self.obsidian -= v
            elif k == GEODE:
                self.geodes -= v
            else:
                raise Exception("Unexpected cost " + k)


    def can_afford(self, robo_cost):
        for material, required in robo_cost.items():
            if material == ORE and self.ore < required:
                return False
            if material == CLAY and self.clay < required:
                return False
            if material == OBISIDIAN and self.obsidian < required:
                return False
            if material == GEODE and self.geodes < required:
                return False
        return True

    def get_priority(self):
        ore_cost = self.geode_robo_cost[ORE]
        obsidian_cost = self.geode_robo_cost[OBISIDIAN]
        clay_cost = self.obsidian_robo_cost[CLAY]

        ore_minutes = ore_cost / (self.ore + 0.000001)
        obsidian_minutes = obsidian_cost / (self.obsidian + 0.000001)
        clay_minutes = clay_cost / (self.clay + 0.000001)

        if self.can_afford(self.ore_robo_cost) and ore_minutes > obsidian_minutes and ore_minutes > clay_minutes:
            return self.build_ore_robot

        elif self.can_afford(self.clay_robo_cost) and clay_minutes > obsidian_minutes and clay_minutes > ore_minutes:
            return self.build_clay_robot

        elif self.can_afford(self.obsidian_robo_cost) and obsidian_minutes > ore_minutes and obsidian_minutes > clay_minutes:
            return self.build_obsidian_robot

        else:
            return random.choice(self.random_build)


    def execute_strategy(self):
        if self.can_afford(self.geode_robo_cost):
            self.build_geode_robot()
            return

        # if self.clay_robots == 0 and self.can_afford(self.clay_robo_cost):
        #     self.build_clay_robot()
        #     return
        #
        # if self.obsidian_robots == 0 and self.can_afford(self.obsidian_robo_cost):
        #     self.build_obsidian_robot()
        #     return

        self.get_priority()()


    def build_ore_robot(self):
        if not self.can_afford(self.ore_robo_cost):
            return
        # print(f"Building ore robot. Using {self.ore_robo_cost}")
        self.use_resources(self.ore_robo_cost)
        self.ore_bot_building = True

    def build_clay_robot(self):
        if not self.can_afford(self.clay_robo_cost):
            return
        # print(f"Building clay robot. Using {self.clay_robo_cost}")
        self.use_resources(self.clay_robo_cost)
        self.clay_bot_building = True

    def build_obsidian_robot(self):
        if not self.can_afford(self.obsidian_robo_cost):
            return
        # print(f"Building obsidian robot. Using {self.obsidian_robo_cost}")
        self.use_resources(self.obsidian_robo_cost)
        self.obsidian_bot_building = True

    def build_geode_robot(self):
        if not self.can_afford(self.geode_robo_cost):
            return
        # print(f"Building geode robot. Using {self.geode_robo_cost}")
        self.use_resources(self.geode_robo_cost)
        self.geode_bot_building = True


    def __str__(self) -> str:
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )


def get_cost_table():
    return {ORE: 0,
            CLAY: 0,
            OBISIDIAN: 0,
            GEODE: 0}


def extract_material_costs(raw_str):
    costs = get_cost_table()
    for i, line_part in enumerate(raw_str):
        if str.isdigit(line_part):
            costs[raw_str[i + 1].strip().split(" ")[0]] = int(line_part)
    return costs


def parse_costs(line):
    cost_snippets = line.split(": ")[1].split(".")

    raw_ore_cost = re.split("(\\d+)", cost_snippets[0])
    raw_clay_cost = re.split("(\\d+)", cost_snippets[1])
    raw_obsidian_cost = re.split("(\\d+)", cost_snippets[2])
    raw_geode_cost = re.split("(\\d+)", cost_snippets[3])

    ore_costs = extract_material_costs(raw_ore_cost)
    clay_costs = extract_material_costs(raw_clay_cost)
    obsidian_costs = extract_material_costs(raw_obsidian_cost)
    geode_costs = extract_material_costs(raw_geode_cost)

    return ore_costs, clay_costs, obsidian_costs, geode_costs



with open("resources/day19.txt", 'r') as f:
    factories = {}
    for i, line in enumerate(f.read().splitlines()):
        ore_costs, clay_costs, obsidian_costs, geode_costs = parse_costs(line)

        blueprint = i + 1
        factory = RobotFactory(blueprint, ore_costs, clay_costs, obsidian_costs, geode_costs)
        factories[blueprint] = factory


    time = 24
    most_geodes = 0
    for cycle in range(1000):
        # print("\n\n\nCYCLE NUMBER " + str(cycle))
        for i in range(time):
            # print("Minute " + str(i + 1))
            factories[1].step()
        geodes = factories[1].geodes
        factories[1].reset()
        if geodes > most_geodes:
            most_geodes = geodes

    print(most_geodes)