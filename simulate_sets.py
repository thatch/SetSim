"""
A brute-force simulation of the card game 'Set'.  This uses a recursive
solution-finder, which keeps bit-strings to easily identify whether a
feature presents a possible solution.  Can generalize very easily to more
factors and sets of sizes > 3.

Tim Hatch and Eric Anderson
Dec 29, 2008
"""

import sys
import random

SET_SIZE = 3 # find 3 cards where each factor...
DESIRED_BOARD = 12 # number of cards face-up on the table
DRAW_SIZE = 3 # number drawn when no matches exist

def pop(n):
    """Number of set bits in n"""
    x = 0
    if n & 4: x += 1
    if n & 2: x += 1
    if n & 1: x += 1
    return x

factors = [
    ('colors', {1: 'blue', 2: 'red', 4: 'green'}),
    ('shapes', {1: 'diamond', 2: 'oval', 4: 'squiggly'}),
    ('numbers', {1: 'one', 2: 'two', 4: 'three'}), # HA
    ('shades', {1: 'empty', 2: 'striped', 4: 'full'}),
    ('finish', {1: 'matte', 2: 'gloss', 4: 'rough'}),
    ('taste', {1: 'sweet', 2: 'sour', 4: 'spicy'}),
]

#for (_, d) in factors:
#    for k, v in d.items():
#        globals()[v] = k

#def randomcards(n):
#    r = []
#    for i in range(n):
#        r.append(tuple([1 << random.randint(0, 2) for x in range(4)]))
#    return r

def pprintcard(tup):
    return [d[v] for ((_, d), v) in zip(factors, tup)]

def find_a_set(cards, next_i, so_far, so_far_list, cards_so_far, cards_left):
    if cards_left == 0:
        return so_far_list

    # so_far is a tuple of bits, which we check against the set of bits in c
    # to see what whether a match/difference exists for this card compared
    # with the previous set.
    # TODO verify stop value is sane (makes sense to not recurse when
    # there are fewer cards left than recursions needed, but doesn't seem to
    # really save that much time)
    for i, c in enumerate(cards[next_i:len(cards)-cards_left+1]):
        broke = False

        #new_so_far = [c[x] | so_far[x] for x in range(len(factors))]
        new_so_far = [x | y for x, y in zip(c, so_far)]

        # new_so_far only needs to be calculated once, because for the elif
        # case below, c[factor] == so_far[factor].  Don't check these until
        # the third card (because for the first and second card selection,
        # anything goes.
        if cards_so_far >= 2:
            for factor in range(len(factors)):
                p = pop(new_so_far[factor])
                # The first part means that the factors are all different,
                # while the second means that they're all the same.
                if not ((p == cards_so_far+1) or p == 1):
                    broke = True
                    break
        if not broke:
            # Whenever the loop above runs to completion, we recurse.  This
            # might return None (meaning not satisfiable), or a list of
            # cards that satisfy the conditions, so short-circuit.
            x = find_a_set(cards, i+next_i+1, new_so_far,
                           so_far_list + [i+next_i], cards_so_far + 1,
                           cards_left-1)
            if x:
                return x
    return None

def cartesian(args):
    """
    Cartesian join of the arguments (each of which is iterable).

    >>> list(cartesian([1, 2], [11, 12]))
    [(1, 11), (1, 12), (2, 11), (2, 12)]
    """
    if len(args) == 1:
        for a in args[0]:
            yield (a,)
    else:
        for a in args[0]:
            for b in cartesian(args[1:]):
                yield (a,) + b


def deck_obvious():
    """
    Better to use cartesian() instead of this, because it isn't hard-coded.
    The main difference is that this always returns a sorted deck, whereas
    cartesian uses dict key order.
    """
    deck = []
    for color in (1, 2, 4):
        for shape in (1, 2, 4):
            for number in (1, 2, 4):
                for shade in (1, 2, 4):
                    deck.append((color, shape, number, shade, finish))
    return deck

def play_a_game(deck):


    out = []

    for i in range(DESIRED_BOARD):
        out.append(deck.pop())

    prev_was_draw = False
    while out or deck:
        f = find_a_set(out, 0, (0,) * len(factors), [], 0, SET_SIZE)
        if f is None:
            if deck:
                print "draw with %d cards out, consecutive=%s" % \
                      (len(out), prev_was_draw)
                for i in range(DRAW_SIZE):
                    if deck: out.append(deck.pop())
            else:
                print "Deck exhausted (%d out)" % (len(out),)
                break
            prev_was_draw = True
        else:
            print "solution", f
            #for i in f:
            #    print "  ", repr(pprintcard(out[i]))

            # The solution f is guaranteed to be in ascending order by
            # index, so reverse it such that the del call doesn't mess
            # things up.
            for i in f[::-1]:
                del out[i]
            while deck and len(out) < DESIRED_BOARD:
                out.append(deck.pop())
            prev_was_draw = False

    print "End of game\n"
    #out = randomcards(12)
    #f = find_a_set(c, 0, (0, 0, 0, 0), [], 0, 3)
    #print '\n'.join(map(repr, map(pprintcard, (c[i] for i in f))))

def main(rounds=1, num_factors=4, board_size=12, set_size=3, draw_size=3):
    del factors[int(num_factors):]
    global DESIRED_BOARD, SET_SIZE, DRAW_SIZE
    DESIRED_BOARD = int(board_size)
    SET_SIZE = int(set_size)
    DRAW_SIZE = int(draw_size)

    deck = list(cartesian([d.keys() for _, d in factors]))
    for i in range(int(rounds)):
        print "Game", i+1
        c = deck[:]
        random.shuffle(c)
        play_a_game(c)


if __name__ == '__main__':
    main(*sys.argv[1:])

