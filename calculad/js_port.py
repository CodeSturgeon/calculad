# Raw port from Javascript

operations = (
    lambda a, b: {'str': "%d + %d" % (a, b), 'result': a + b},
    lambda a, b: {'str': "%d - %d" % (a, b), 'result': a - b},
    lambda a, b: {'str': "%d - %d" % (b, a), 'result': b - a},
    lambda a, b: {'str': "%d * %d" % (a, b), 'result': a * b},
)


def runLevel(cards, initInts):
    global called, doneCheck, doneDone, search, doneWork

    solutions = []
    paths = {}

    # Used for checking how many times each section was called
    called = 0
    doneCheck = 0
    doneDone = 0
    search = 0

    # How many times will we run through the original for loop?
    totalWork = len(initInts) * (len(initInts) - 1) / 2
    doneWork = 0

    cards = sorted(cards)
    initInts = sorted(initInts)

    def explore(stack, ints, init=False):
        global called, doneCheck, doneDone, search, doneWork
        called += 1
        ints = sorted(ints)

        # If we've already gone down this path, no need to redo work
        key = ','.join(map(str, ints))
        if key in paths:
            return
        paths[key] = True

        # Base case
        if len(ints) <= len(cards):
            doneCheck += 1

            # We're done if all of the ints we have match (uniquely) cards
            j = 0
            for i in range(len(cards)):
                # PY added range check as PY balks at out of range check
                if j < len(ints) and cards[i] == ints[j]:
                    # Match, increment both
                    j += 1

            # If all of the integer cards have matches, we've got a solution!
            if j == len(ints):
                doneDone += 1

                solution = {'stack': stack, 'ints': ints}
                # This check may be redundant with the dynamic programming stuff above
                if solution not in solutions:
                    solutions.append(solution)
                return

        # We're done if we only have one number left (and it doesn't match a card)
        if len(ints) == 1:
            return

        # Search!
        search += 1

        # We pull two numbers out of our set of integers & apply all of the operations
        for i in range(len(ints)):
            left = ints[i]
            localInts = ints[:]
            localInts.pop(i)

            for j in range(len(localInts)):
                right = localInts.pop(j)

                for k in range(len(operations)):
                    r = operations[k](left, right)

                    explore(stack + [r['str']], localInts + [r['result']])

                if init:
                    doneWork += 1
                    #print float(doneWork) / float(totalWork)
                    #print left, right

                localInts.insert(0, right)

            localInts.insert(0, left)

    explore([], initInts, True)

    #print "'explore' was called", called, 'times'
    #print "'done check' was called", doneCheck, 'times'
    #print "'doneDone check' was called", doneDone, 'times'
    #print "'search check' was called", search, 'times'
    print called

    return solutions
