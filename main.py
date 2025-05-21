import random

# permutations and orientations of the 20 pieces
cp = [0,1,2,3,4,5,6,7]
co = [0,0,0,0,0,0,0,0]
ep = [0,1,2,3,4,5,6,7,8,9,10,11]
eo = [0,0,0,0,0,0,0,0,0,0,0,0]

# lists (cycles)
cornerCycles = []
edgeCycles = []

# randomly scramble the cube
def scramble(mustBeValidScramble, printPosition, printDetailed, printAlgs):
    cornerParity = 0
    edgeParity = 0

    random.shuffle(cp)
    for i in range(8):
        co[i] = random.choice([0, 1])
        cornerParity += co[i]
    random.shuffle(ep)
    for i in range(12):
        eo[i] = random.choice([0, 1])
        edgeParity += eo[i]

    # adjust parity to be valid
    if mustBeValidScramble:
        if cornerParity % 2:
            co[0] = (co[0] + 1) % 2
        if edgeParity % 2:
            eo[0] = (eo[0] + 1) % 2

        # permutation parity: if number of 2 corner+edge swaps required to solve is odd, swap first two edges
        cpSwaps = [0,0,0,0,0,0,0,0]
        epSwaps = [0,0,0,0,0,0,0,0,0,0,0,0]
        temp = 0
        swaps = 0
        for i in range(8):
            cpSwaps[i] = cp[i]
        for i in range(12):
            epSwaps[i] = ep[i]
        for i in range(8):
            for j in range(8):
                if i != j and cpSwaps[j] == i:
                    temp = cpSwaps[i]
                    cpSwaps[i] = cpSwaps[j]
                    cpSwaps[j] = temp
                    swaps += 1
                    break
        for i in range(12):
            for j in range(12):
                if i != j and epSwaps[j] == i:
                    temp = epSwaps[i]
                    epSwaps[i] = epSwaps[j]
                    epSwaps[j] = temp
                    swaps += 1
                    break
        if swaps % 2:
            temp = ep[0]
            ep[0] = ep[1]
            ep[1] = temp
            
        
    cornerCycles = [[0]]
    edgeCycles = [[0]]
    cornersLeft = [1,2,3,4,5,6,7]
    edgesLeft = [1,2,3,4,5,6,7,8,9,10,11]

    # update cornerCycles
    currentCycle = 0
    nextPiece = cp[0]
    while True:
        if nextPiece == cornerCycles[currentCycle][0]:
            # if next piece is the one at start of cycle, end cycle and start cycle using next unrecorded piece
            currentCycle += 1
            cornerCycles.append([])
            if cornersLeft.count(nextPiece) > 0:
                cornersLeft.remove(nextPiece)
            if len(cornersLeft) == 0:
                break
            nextPiece = cornersLeft[0]
            cornerCycles[currentCycle].append(nextPiece)
            nextPiece = cp[nextPiece]
        else:
            # otherwise, continue this cycle
            cornerCycles[currentCycle].append(nextPiece)
            cornersLeft.remove(nextPiece)
            if len(cornersLeft) == 0:
                break
            nextPiece = cp[nextPiece]

    # update edgeCycles
    currentCycle = 0
    nextPiece = ep[0]
    while True:
        if nextPiece == edgeCycles[currentCycle][0]:
            # if next piece is the one at start of cycle, end cycle and start cycle using next unrecorded piece
            currentCycle += 1
            edgeCycles.append([])
            if edgesLeft.count(nextPiece) > 0:
                edgesLeft.remove(nextPiece)
            if len(edgesLeft) == 0:
                break
            nextPiece = edgesLeft[0]
            edgeCycles[currentCycle].append(nextPiece)
            nextPiece = ep[nextPiece]
        else:
            # otherwise, continue this cycle
            edgeCycles[currentCycle].append(nextPiece)
            edgesLeft.remove(nextPiece)
            if len(edgesLeft) == 0:
                break
            nextPiece = ep[nextPiece]

    # remove empty cycles at end if necessary
    if cornerCycles[len(cornerCycles) - 1] == []:
        cornerCycles.pop()
    if edgeCycles[len(edgeCycles) - 1] == []:
        edgeCycles.pop()

    if printPosition:
        bad = 0
        for i in range(len(cp)):
            if i != cp[i]: bad += 1
        print("Corner permutation: " + str(cp) + " - " + str(bad) + " misplaced corners.")
        bad = 0
        for i in range(len(co)):
            if co[i] == 1: bad += 1
        print("Corner orientation: " + str(co) + " - " + str(bad) + " bad corners.")
        bad = 0
        for i in range(len(ep)):
            if i != ep[i]: bad += 1
        print("Edge permutation: " + str(ep) + " - " + str(bad) + " misplaced edges.")
        bad = 0
        for i in range(len(eo)):
            if eo[i] == 1: bad += 1
        print("Edge orientation: " + str(eo) + " - " + str(bad) + " bad edges.")

        print("\nCorner cycles:")
        for i in cornerCycles:
            print(i)
        print("\nEdge cycles:")
        for i in edgeCycles:
            print(i)
        print("")

    count3c = 0
    count3e = 0
    count2c = 0
    count2e = 0
    count1c = 0
    count1e = 0

    for cycle in cornerCycles:
        cycleLength = len(cycle)
        if cycleLength == 1:
            count1c += 1
        elif cycleLength % 2:
            count3c += int(cycleLength / 2)
        else:
            count3c += int(cycleLength / 2) - 1
            count2c += 1

    for cycle in edgeCycles:
        cycleLength = len(cycle)
        if cycleLength == 1:
            count1e += 1
        elif cycleLength % 2:
            count3e += int(cycleLength / 2)
        else:
            count3e += int(cycleLength / 2) - 1
            count2e += 1

    if printDetailed:
        print(str(count1c) + " 1Cs, " + str(count2c) + " 2Cs, " + str(count3c) + " 3Cs, " + str(count1e) + " 1Es, " + str(count2e) + " 2Es, " + str(count3e) + " 3Es, " + str(int((count2c + count2e + 1) / 2) + count3c + count3e) + " algs needed.")
        if(count2c + count2e) % 2:
            print("Permutation parity is impossible.\n")
        elif count2c % 2:
            print("Permutation parity is bad.\n")
        else:
            print("Permutation parity is good.\n")

    corner3s = []
    corner2s = []
    edge3s = []
    edge2s = []
    parity = []
    if(printAlgs):
        # construct corner cycles
        for i in range(len(cornerCycles)):
            for j in range(0, len(cornerCycles[i]) - 1, 2):
                if j < len(cornerCycles[i]) - 2:
                    cycle = [cornerCycles[i][0], cornerCycles[i][j+1], cornerCycles[i][j+2]]
                    corner3s.append(cycle)
                else:
                    if len(corner2s) == 0:
                        cycle = [cornerCycles[i][0], cornerCycles[i][j+1]]
                        corner2s.append(cycle)
                    elif len(corner2s[-1]) == 4:
                        cycle = [cornerCycles[i][0], cornerCycles[i][j+1]]
                        corner2s.append(cycle)
                    else:
                        corner2s[-1].append(cornerCycles[i][0])
                        corner2s[-1].append(cornerCycles[i][j+1])

        # construct edge cycles
        for i in range(len(edgeCycles)):
            for j in range(0, len(edgeCycles[i]) - 1, 2):
                if j < len(edgeCycles[i]) - 2:
                    cycle = [edgeCycles[i][0], edgeCycles[i][j+1], edgeCycles[i][j+2]]
                    edge3s.append(cycle)
                else:
                    if len(edge2s) == 0:
                        cycle = [edgeCycles[i][0], edgeCycles[i][j+1]]
                        edge2s.append(cycle)
                    elif len(edge2s[-1]) == 4:
                        cycle = [edgeCycles[i][0], edgeCycles[i][j+1]]
                        edge2s.append(cycle)
                    else:
                        edge2s[-1].append(edgeCycles[i][0])
                        edge2s[-1].append(edgeCycles[i][j+1])

        # handle parity
        if len(corner2s) > 0 and len(edge2s) > 0:
            if len(corner2s[-1]) == 2 and len(edge2s[-1]) == 2:
                parity = [corner2s[-1][0], corner2s[-1][1], edge2s[-1][0], edge2s[-1][1]]
                corner2s.pop()
                edge2s.pop()

        for i in corner3s:
            print("3 Corners: " + str(i))
        for i in corner2s:
            print("2+2 Corners: " + str(i))
        for i in edge3s:
            print("3 Edges: " + str(i))
        for i in edge2s:
            print("2+2 Edges: " + str(i))
        print("Parity: " + str(parity) + "\n\n")


def main():
    scramble(True, True, True, True)
    scramble(True, True, True, True)
    scramble(True, True, True, True)
    scramble(True, True, True, True)

main()
