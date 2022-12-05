static def parseCrates(String line) {
    String[] crates = new String[]{}
    for (int i = 1; i < line.length(); i += 4) {
        char c = line.charAt(i)
        if (c != ' ' as char) {
            crates += c
        }
    }
    return crates
}

static def extractInts(String input) {
    input.findAll( /\d+/ )*.toInteger()
}

static def findFileSplitPoint(String[] lines) {
    int i = 0
    while (lines[i] != "") {
        i++
    }
    return i;
}

def getInstructionLines(String[] lines) {
    int i = 0
    String[] instructionLines = new String[]{}
    while (lines[i] != "") {
        i++
    }


    return stackLines
}

String[] lines = new File('resources/day5.txt').readLines()

splitPoint = findFileSplitPoint(lines)

crateLines = lines[0 .. splitPoint - 2]
String stackNumbersLine = lines[splitPoint - 1]
instructionLines = lines[splitPoint + 1 .. lines.length - 1]

numberOfStacks = stackNumbersLine[stackNumbersLine.length() - 1] as Integer

int spaceBetweenCrates = 4

Map<Integer, char[]> stacks = [:]
crateNb = 1
for (int i = 1; i < numberOfStacks * spaceBetweenCrates; i += spaceBetweenCrates) {
    def crates = []
    for (int j = crateLines.size() - 1; j > -1; j--) {
        c = crateLines[j].charAt(i)
        if (c != ' ' as char) crates += c
    }

    stacks[crateNb] = crates.reverse()
    crateNb++
}

instructionLines.each{line ->
    instructions = extractInts(line)
    for (int i = 0; i < instructions[0]; i++) {
        stacks[instructions[2]].push(stacks[instructions[1]].pop())
    }
}


stacks.each{stack, crates ->
    if (crates.size > 0) {
        print(crates[0])
    }
}
