function findCalorieCounts(file)
    local currentCalorieCount = 0
    local elfCount = 1
    local calorieCounts = {}
    for line in io.lines(file) do
        if (line == "")
        then
            print("Total Calories for elf " .. elfCount .. ": " .. currentCalorieCount)
            calorieCounts[#(calorieCounts) + 1] = currentCalorieCount
            currentCalorieCount = 0
            elfCount = elfCount + 1
        else
            currentCalorieCount = currentCalorieCount + tonumber(line)
        end
    end
    return calorieCounts
end

function getTopNCalorieTotal(calories, n)
    local total = 0
    for i = 1, n do
        total = total + calories[i]
    end
    return total
end

local file = 'resources/day1.txt'
local calories = findCalorieCounts(file)

table.sort(calories, function(a, b) return a > b end)

print("\nTop three calories total: " .. getTopNCalorieTotal(calories, 3))
