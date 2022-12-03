function calculateScore(file)

    shapeReward = {
        X = 1,
        Y = 2,
        Z = 3
    }

    outcomeReward = {
        X = {
            A = 3,
            B = 0,
            C = 6
        },
        Y = {
            A = 6,
            B = 3,
            C = 0
        },
        Z = {
            A = 0,
            B = 6,
            C = 3
        }
    }

    totalReward = 0
    for line in io.lines(file) do
        oppShape = (line:sub(1, 1))
        outcomeGoal = (line:sub(3, 3))
        totalReward = totalReward + shapeReward[outcomeGoal] + outcomeReward[outcomeGoal][oppShape]
    end
    return totalReward
end

local file = 'resources/day2.txt'
print(calculateScore(file))

