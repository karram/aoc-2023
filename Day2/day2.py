from math import prod

MAX_CUBES = {'r': 12, 'g': 13, 'b': 14}

def is_valid_subgame(subgame: dict, maxcubes:dict = MAX_CUBES):
    """
    Returns true if subgame is valid, ie, all r, g, b cube count is <= MAX
    :param subgame:
    :param maxcubes:
    :return:
    """
    return all([subgame.get(k) <= maxcubes.get(k) for k in subgame.keys()])

def is_valid_game(game: list[dict]):
    """
    Returns true if a game is valid.
    A game is valid only when all subgames are valid
    :param game:
    :return:
    """
    return all([is_valid_subgame(subgame) for subgame in game])

def get_cubes(subgame: str):
    """
    Given a subgame, return a dict containing cubes and count
    Input 3 blue, 4 red
    Returns {"b": 3, "r": 4}
    :param subgame:
    :return:
    """
    retval = dict()
    cubes = subgame.split(", ")
    for c in cubes:
        parts = c.split(" ")
        retval[parts[1][0]] = int(parts[0])
    return retval


def get_subgames(line: str):
    """
   Parse a single line to extract a list of subgames
   Subgames are separated by "; "
   Individual cube counts within a game by ", "
   For example: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green as input would return
   [{"b": 3, "r" : 4}, {"r": 1, "g" : 2, "b": 6}, {"g": 2}]
   :param line: A single game
   :return: List of cube sets within the game
   """
    parts = line.split("; ")
    subgames = [get_cubes(subgame) for subgame in parts]
    return subgames


def get_game(input: str):
    """
    Parse a line to extract games
    :param input:
    :return:
    """
    parts = input.split(": ")
    _, gameid = tuple(parts[0].split(" "))
    subgames = get_subgames(parts[1])
    return [int(gameid), subgames]

def get_games_from_file(filename):
    contents = open(filename).readlines()
    games = []
    for c in contents:
        game = get_game(c)
        games.append(game)
    return games

def part_a(filename):
    games = get_games_from_file(filename)
    valid_games = [g for g in games if is_valid_game(g[1])]
    print(f"{valid_games=}")
    score = sum([x[0] for x in valid_games])
    return score

def get_min_cubes(games_list: list[dict]):
    """
    Given a list of subgames, find the min number of cubes
    :param games_list:
    :return:
    """
    maxes = []
    for color in ("r", "g", "b"):
        cmax = max([game.get(color, 0) for game in games_list])
        maxes.append(cmax)
    return tuple(maxes)

def part_b(filename):
    games = get_games_from_file(filename)
    min_cubes = [get_min_cubes(g[1]) for g in games]
    print(min_cubes)
    score = sum([prod(x) for x in min_cubes])
    print(f"{score=}")
    return score

# sample_score = part_a("sample_input.txt")
# print(f"{sample_score=}")

# score = part_a("input_a.txt")
# print(f"{score=}")

sample_score = part_b("sample_input.txt")
print(f"{sample_score=}")

score = part_b("input_a.txt")
print(f"{score=}")
