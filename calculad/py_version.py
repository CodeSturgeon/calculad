# Py version
from collections import namedtuple
Solution = namedtuple('Solution', 'ops cards')

operations = (
    lambda a, b: ("%d + %d" % (a, b), a + b),
    lambda a, b: ("%d - %d" % (a, b), a - b),
    lambda a, b: ("%d - %d" % (b, a), b - a),
    lambda a, b: ("%d * %d" % (a, b), a * b),
)


def runLevel(cards, initInts):
    solutions = []
    paths = set()

    cards = sorted(cards)
    initInts = sorted(initInts)

    def explore(stack, ints):
        ints = sorted(ints)

        # If we've already gone down this path, no need to redo work
        key = tuple(ints)
        if key in paths:
            return
        paths.add(key)

        # Check if we have a solution
        idx = 0
        for i in ints:
            if i in cards[idx:]:
                idx = cards[idx:].index(i) + idx + 1
            else:
                break
        else:
            solutions.append(Solution(stack, ints))
            return

        # We're done if we only have one number left
        if len(ints) == 1:
            return

        # We pull two numbers and apply all of the operations
        for left in ints:
            localInts = ints[:]
            localInts.remove(left)

            for right in localInts:
                localInts.remove(right)

                for op in operations:
                    r = op(left, right)
                    explore(stack + [r[0]], localInts + [r[1]])

                localInts.insert(0, right)

    explore([], initInts)

    return solutions
