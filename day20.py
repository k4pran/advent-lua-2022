
# p1
with open("resources/day20.txt", 'r') as f:
    code = [i for i in map(int, f.read().splitlines())]
    encryption = [(k, v) for k, v in enumerate(code)]

    index = 0
    print([i[1] for i in encryption])
    for n, movement in enumerate(code):

        for j in range(len(code)):
            if encryption[j][0] == n:
                index = j
                break

        distance = encryption[j][1]
        encryption.insert(((index + distance)) % (len(encryption) - 1), encryption.pop(index % len(encryption)))
        print([i[1] for i in encryption])


    # find 0 index
    for i, val in enumerate(encryption):
        if val[1] == 0:
            break
    groove = encryption[(i + 1000) % len(encryption)][1] + encryption[(i + 2000) % len(encryption)][1] + encryption[(i + 3000) % len(encryption)][1]
    print(groove)

#p2
with open("resources/day20.txt", 'r') as f:
    code = [i * 811589153 for i in map(int, f.read().splitlines())]
    encryption = [(k, v) for k, v in enumerate(code)]

    index = 0
    print([i[1] for i in encryption])
    for k in range(10):
        for n, movement in enumerate(code):

            for j in range(len(code)):
                if encryption[j][0] == n:
                    index = j
                    break

            distance = encryption[j][1]
            encryption.insert(((index + distance)) % (len(encryption) - 1), encryption.pop(index % len(encryption)))
            print([i[1] for i in encryption])


    # find 0 index
    for i, val in enumerate(encryption):
        if val[1] == 0:
            break
    groove = encryption[(i + 1000) % len(encryption)][1] + encryption[(i + 2000) % len(encryption)][1] + encryption[(i + 3000) % len(encryption)][1]
    print(groove)