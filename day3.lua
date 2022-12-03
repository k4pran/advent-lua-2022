ALPHABET_COUNT = 26
ASCII_LOWERCASE_LETTER_START = 97
ASCII_UPPERCASE_LETTER_START = 65

function len(T)
    local count = 0
    for _ in pairs(T) do count = count + 1 end
    return count
end

function getAsciiCharacters(startPos, endPos)
    local chars  = {}
    for i=startPos, endPos do
        chars[#chars + 1] = string.char(i)
    end
    return chars
end

function enumerateTbl(tbl)
    local enumeratedTbl = {}
    for i=1, #tbl do
        enumeratedTbl[tbl[i]] = i
    end
    return enumeratedTbl
end

function concatTables(tbl1, tbl2)
    for i=1, #tbl2 do
        tbl1[#tbl1 + 1] = tbl2[i]
    end
end

function getCompartments(rucksack)
    local compartment1 = string.sub(rucksack, 1, #rucksack / 2)
    local compartment2 = string.sub(rucksack, (#rucksack / 2) + 1)

    return { compartment1, compartment2 }
end

function getLines(file)
    local lines = {}
    for line in io.lines(file) do
        lines[#lines + 1] = line
    end
    return lines
end

function CharSet(str)
    local charSet = {}
    for i = 1, #str do
        local c = str:sub(i,i)
        charSet[c] = true
    end
    return charSet
end

function intersection(set1, set2)
    local intersection = {}
    for k, v in pairs(set1) do
        if set2[k] ~= nil
        then
            intersection[k] = true
        end
    end
    return intersection
end

function calculatePriority(priorityTable, items)
    local priorityTotal = 0

    for k, _ in pairs(items) do
        priorityTotal = priorityTotal + priorityTable[k]
    end
    return priorityTotal
end

local file = 'resources/day3.txt'

local itemTypes = getAsciiCharacters(ASCII_LOWERCASE_LETTER_START, ASCII_LOWERCASE_LETTER_START + ALPHABET_COUNT - 1)
concatTables(itemTypes, getAsciiCharacters(ASCII_UPPERCASE_LETTER_START, ASCII_UPPERCASE_LETTER_START + ALPHABET_COUNT - 1))

local lines = getLines(file)
local priorityTable = enumerateTbl(itemTypes)

-- PART1
local totalPriority = 0
for i=1, #lines do
    local compartment1, compartment2 = table.unpack(getCompartments(lines[i]))

    local duplicateItems = intersection(CharSet(compartment1), CharSet(compartment2))

    local rucksackPriority = calculatePriority(priorityTable, duplicateItems)
    totalPriority = totalPriority + rucksackPriority
end

print("PART 1 answer: " .. totalPriority)

-- PART2
elfGroupSize = 3
totalPriority = 0
for i=1, #lines, elfGroupSize do
    rucksack1 = CharSet(lines[i])
    rucksack2 = CharSet(lines[i + 1])
    rucksack3 = CharSet(lines[i + 2])

    badges = intersection(rucksack3, intersection(rucksack1, rucksack2))

    totalPriority = totalPriority + calculatePriority(priorityTable, badges)
end

print("PART 2 answer: " .. totalPriority)



