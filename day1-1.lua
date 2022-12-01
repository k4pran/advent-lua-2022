function findHighestCalories(file)
    local highestCalorieCount = 0
    local currentCalorieCount = 0
    local elfCount = 1
    for line in io.lines(file) do
        if (line == "")
        then
            print("Total Calories for elf " .. elfCount .. ": " .. currentCalorieCount)
            if (currentCalorieCount > highestCalorieCount)
            then
                highestCalorieCount = currentCalorieCount
            end
            currentCalorieCount = 0
            elfCount = elfCount + 1
        else
            currentCalorieCount = currentCalorieCount + tonumber(line)
        end
    end
    return highestCalorieCount
end

local file = 'resources/day1.txt'
local highestCalorieCount = findHighestCalories(file)

print("\nHighest count: " .. highestCalorieCount)
