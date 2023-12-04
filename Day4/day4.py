from collections import deque


def parse_card_entry(card_entry: str):
    """
    Parse a line containing a card and return it as a ({wins},{mine}) tuple
    :param card_entry:
    :return:
    """
    id, entry = card_entry.split(": ")
    card_id = int(id.split(" ")[-1])
    wins, mine = entry.split("| ")
    wins = {int(x) for x in wins.split()}
    mine = {int(x) for x in mine.split()}
    return (card_id, wins, mine)


def part_a(filename):
    games = get_cards(filename)
    mywins = [wins.intersection(mine) for _, wins, mine in games]
    win_count = [len(x) for x in mywins if x]
    score = sum([pow(2, x - 1) for x in win_count])
    return score


def get_cards(filename):
    contents = open(filename).readlines()
    cards = [parse_card_entry(e) for e in contents]
    return cards


def part_b_2(filename):
    cards = get_cards(filename)
    card_copies = [1 for x in cards]
    # print(f"{card_copies=}")
    for c in cards:
        id, wins, mine = c
        win_count = len(wins.intersection(mine))
        new_cards = list(range(id + 1, id + win_count + 1))
        # print(f"{id=} wins={win_count} {new_cards=}")
        current_card_count = card_copies[id - 1]
        for nc in new_cards:
            card_copies[nc - 1] += current_card_count
        # print(f"{card_copies=}")
    return sum(card_copies)


# score = part_a("sample_input.txt")
# print(f"{score=}")

# score = part_a("input_a.txt")
# print(f"{score=}")

score = part_b_2("sample_input.txt")
print(f"{score=}")

score = part_b_2("input_a.txt")
print(f"{score=}")
