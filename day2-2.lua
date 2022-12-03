function calculateScore(file)

    shapeReward = {
        A = 1,
        B = 2,
        C = 3
    }

    outcomeReward = {
        X = {
            A = shapeReward["C"],
            B = shapeReward["A"],
            C = shapeReward["B"],
        },
        Y = {
            A = 3 + shapeReward["A"],
            B = 3 + shapeReward["B"],
            C = 3 + shapeReward["C"]
        },
        Z = {
            A = 6 + shapeReward["B"],
            B = 6 + shapeReward["C"],
            C = 6 + shapeReward["A"]
        }
    }

    totalReward = 0
    for line in io.lines(file) do
        oppShape = (line:sub(1, 1))
        outcomeGoal = (line:sub(3, 3))
        totalReward = totalReward + outcomeReward[outcomeGoal][oppShape]
    end
    return totalReward
end

local file = 'resources/day2.txt'
print(calculateScore(file))

