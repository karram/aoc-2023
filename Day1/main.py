filename = "sample_input.txt"

replace_map = {"one": "1",
               "two": "2",
               "three": "3",
               "four": "4",
               "five": "5",
               "six": "6",
               "seven": "7",
               "eight": "8",
               "nine": "9",
               "zero": "0"}

def part_a(filename):
    contents = open(filename).readlines()
    nums = ["".join(c for c in x if c.isdigit()) for x in contents]
    nums = [int(x[0] + x[-1]) for x in nums]
    return sum(nums)

def replace_first_num(input_str: str):
    offsets = [(input_str.find(k), k) for k in replace_map.keys()]
    offsets = [x for x in offsets if x[0] != -1]
    if not offsets:
        return input_str
    first_pos, first_num = min(offsets)
    new_str = input_str.replace(first_num, replace_map.get(first_num),1)
    return new_str


def replace_last_num(input_str: str):
    offsets = [(input_str.rfind(k), k) for k in replace_map.keys()]
    offsets = [x for x in offsets if x[0] != -1]
    if not offsets:
        return input_str
    last_pos, last_num = max(offsets)
    new_str = replace_map.get(last_num).join(input_str.rsplit(last_num,1))
    return new_str

def replace_words_with_nums(input_str: str):
    newstr = replace_first_num(input_str)
    newstr = replace_last_num(newstr)
    return newstr

def get_first_digit(input_str):
    newstr = replace_first_num(input_str)
    fn = "".join(c for c in newstr if c.isdigit())
    fn = fn[0]
    return fn

def get_last_digit(input_str):
    newstr = replace_last_num(input_str)
    ln = "".join(c for c in newstr if c.isdigit())
    ln = ln[-1]
    return ln

def part_b(filename):
    contents = open(filename).readlines()
    nums = [(get_first_digit(x), get_last_digit(x)) for x in contents]
    nums = [int(x[0] + x[-1]) for x in nums]
    return sum(nums)

sample_total = part_a("sample_input.txt")
print(f"{sample_total=}")

total = part_a("input.txt")
print(f"{total=}")

sample_str = "twockgseven4seven6bp"
print(f"{sample_str=} and replaced={replace_words_with_nums(sample_str)}")

sample_total = part_b("sample2.txt")
print(f"{sample_total=}")

total = part_b("input.txt")
print(f"{total=}")
