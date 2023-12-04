import re
import itertools
from math import prod

class SchematicItem:
    def __init__(self, value, startpos: tuple, endpos: tuple):
        self.value = value
        self.startpos = startpos
        self.endpos = endpos

    def get_adjacent_cells(self):
        """
        Returns the adjacent cells
        :return:
        """
        startx, starty = self.startpos
        endx, endy = self.endpos
        container = {(x, y) for x in range(startx - 1, endx + 2) for y in range(starty - 1, endy + 2)}
        selfrow = {(x, y) for x in range(startx, endx + 1) for y in range(starty, endy + 1)}
        neighbours = container - selfrow
        return sorted(tuple(neighbours))

    def __repr__(self):
        return f"{self.value} @ {self.startpos}-{self.endpos}"


class SchematicNumber(SchematicItem):
    def __init__(self, value, startpos, endpos):
        super().__init__(value, startpos, endpos)


class SchematicGear:
    def __init__(self, pos):
        self.value = "*"
        self.pos = pos
        self.partnums = []

    def __repr__(self):
        return f"*{self.pos}: {self.partnums}"

    def set_partnums(self, partnums):
        self.partnums = partnums

    def score(self):
        if not self.partnums:
            return 0

        return prod([p.value for p in self.partnums])


class Schematic:
    def __init__(self, filename):
        self.filename = filename
        self.raw_contents = open(filename).readlines()
        self.contents = self.read_schematic(self.raw_contents)
        self.part_numbers = dict()
        self.gears = dict()
        self.process_schematic()

    def read_schematic(self, raw_contents):
        """
        Convert a list of lines representing the schematic into a dictionary
        :param raw_contents:
        :return:
        """
        contents = {(x, y): val for x, c in enumerate(raw_contents) for y, val in enumerate(c.strip())}
        return contents

    def get(self, pos):
        """
        Return the value at a given position
        :param x:
        :param y:
        :return:
        """
        return self.contents.get(pos, ".")

    def get_numbers_in_row(self, rownum):
        numbers = []
        try:
            row = self.raw_contents[rownum]
        except IndexError:
            print("Cannot find row %s. Returning []", rownum)
            return numbers
        for match in re.finditer(r'[0-9]+', row):
            start = match.start()
            end = match.end() - 1
            value = int(match.string[start:end + 1])
            schema_num = SchematicNumber(value, (rownum, start), (rownum, end))
            adjacent = schema_num.get_adjacent_cells()
            neighbours = {self.get(c) for c in adjacent}
            if neighbours != {"."}:
                numbers.append(schema_num)
        return numbers

    def process_schematic(self):
        for row in range(len(self.raw_contents)):
            self.part_numbers[row] = self.get_numbers_in_row(row)

        for row in range(len(self.raw_contents)):
            gears = self.get_gears_in_row(row)
            if gears:
                self.gears[row] = gears

    def score(self):
        partnums = list(itertools.chain(*self.part_numbers.values()))
        return sum([x.value for x in partnums])

    def gear_score(self):
        score = 0
        gears = list(itertools.chain(*self.gears.values()))
        scores = [g.score() for g in gears]
        return sum(scores)

    def get_gears_in_row(self, rownum):
        row = self.raw_contents[rownum]
        gears = []

        for match in re.finditer(r'\*', row):
            start = match.start()
            gear = SchematicGear((rownum, start))
            adjacent_parts = [self.part_numbers.get(r,[]) for r in [rownum-1, rownum, rownum+1]]
            adjacent_parts = list(itertools.chain(*adjacent_parts))
            close = [p for p in adjacent_parts if (rownum, start) in p.get_adjacent_cells()]
            if len(close) == 2:
                gear.set_partnums(close)
                gears.append(gear)
        return gears




sample = Schematic("sample_input.txt")
print(sample.part_numbers)
print(sample.gears)
print(sample.score())
print(f"{sample.gear_score()=}")

sample = Schematic("input_a.txt")
print(sample.part_numbers)
print(sample.score())
print(f"{sample.gear_score()=}")
