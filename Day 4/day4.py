def meets_criteria_one(value):
    has_double_digit = False
    numbers_increase = True
    last_num = -1
    nums = list(map(int, list(value)))
    for num in nums:
        if num < last_num:
            numbers_increase = False
            break
        if not has_double_digit and num == last_num:
            has_double_digit = True
        last_num = num
    return has_double_digit and numbers_increase


def meets_criteria_two(value):
    last_was_double = False
    has_double_digit = False
    numbers_increase = True
    num_consec = 1
    last_num = -1
    nums = list(map(int, list(value)))
    for num in nums:
        if num < last_num:
            numbers_increase = False
            break

        if num == last_num:
            num_consec += 1
            if num_consec == 2:
                last_was_double = True
            else:
                last_was_double = False
        else:
            if last_was_double:
                has_double_digit = True
            last_was_double = False
            num_consec = 1

        last_num = num

    if last_was_double:
        has_double_digit = True
    return has_double_digit and numbers_increase


def run(function_to_run):
    file = open("Input.txt", "r")
    num_range = list(map(int, file.read().split("-")))
    count = function_to_run(num_range)
    print(count)
    return count


def part_one(num_range):
    count = 0
    for value in range(num_range[0], num_range[1]):
        if meets_criteria_one(str(value)):
            count += 1
    return count


def part_two(num_range):
    count = 0
    for value in range(num_range[0], num_range[1]):
        if meets_criteria_two(str(value)):
            count += 1
    return count
