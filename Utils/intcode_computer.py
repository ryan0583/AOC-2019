class Instruction:
    def __init__(self, opcode, param1_mode, param2_mode):
        self.opcode = opcode
        self.param1_mode = param1_mode
        self.param2_mode = param2_mode

    @staticmethod
    def get_instruction(value):
        if len(value) > 1:
            opcode = value[len(value) - 2:]
        else:
            opcode = "0" + value[len(value) - 1:]

        param1_mode = PARAM_MODE_LOOKUP
        param2_mode = PARAM_MODE_LOOKUP

        if len(value) > 2:
            param1_mode = value[len(value) - 3:len(value) - 2]

        if len(value) > 3:
            param2_mode = value[len(value) - 4:len(value) - 3]

        return Instruction(opcode, param1_mode, param2_mode)

    def get_opcode(self):
        return self.opcode

    def get_param1_mode(self):
        return self.param1_mode

    def get_param2_mode(self):
        return self.param2_mode

    def __str__(self):
        return self.opcode + ", " + self.param1_mode + ", " + self.param2_mode


def process(input_val, ints):
    def get_val(param_mode, value):
        param_mode_switcher = {
            PARAM_MODE_LOOKUP: lambda: ints[value],
            PARAM_MODE_DIRECT: lambda: value
        }
        return param_mode_switcher.get(param_mode, lambda: "Invalid param mode" + param_mode)()

    def perform_input_instruction():
        ints[ints[index + 1]] = input_val
        return index + 2,

    def perform_add():
        val1 = get_val(instruction.get_param1_mode(), ints[index + 1])
        val2 = get_val(instruction.get_param2_mode(), ints[index + 2])
        val = val1 + val2
        ints[ints[index + 3]] = val
        return index + 4,

    def perform_multiply():
        val1 = get_val(instruction.get_param1_mode(), ints[index + 1])
        val2 = get_val(instruction.get_param2_mode(), ints[index + 2])
        val = val1 * val2
        ints[ints[index + 3]] = val
        return index + 4,

    def perform_jump_if_true():
        val1 = get_val(instruction.param1_mode, ints[index + 1])

        if val1 != 0:
            return get_val(instruction.param2_mode, ints[index + 2]),
        return index + 3,

    def perform_jump_if_false():
        val1 = get_val(instruction.param1_mode, ints[index + 1])

        if val1 == 0:
            return get_val(instruction.param2_mode, ints[index + 2]),
        return index + 3,

    def perform_less_than():
        val1 = get_val(instruction.param1_mode, ints[index + 1])
        val2 = get_val(instruction.param2_mode, ints[index + 2])

        if val1 < val2:
            ints[ints[index + 3]] = 1
        else:
            ints[ints[index + 3]] = 0
        return index + 4,

    def perform_equals():
        val1 = get_val(instruction.param1_mode, ints[index + 1])
        val2 = get_val(instruction.param2_mode, ints[index + 2])

        if val1 == val2:
            ints[ints[index + 3]] = 1
        else:
            ints[ints[index + 3]] = 0
        return index + 4,

    def perform_output_instruction():
        if instruction.get_param1_mode() == "1":
            output = ints[index + 1]
        else:
            output = ints[ints[index + 1]]
        return index + 2, output

    opcode_switcher = {
        ADD: perform_add,
        MULTIPLY: perform_multiply,
        INPUT: perform_input_instruction,
        OUTPUT: perform_output_instruction,
        JUMP_IF_TRUE: perform_jump_if_true,
        JUMP_IF_FALSE: perform_jump_if_false,
        LESS_THAN: perform_less_than,
        EQUALS: perform_equals
    }

    index = 0
    last_output = 0
    instruction = Instruction.get_instruction(str(ints[index]))
    opcode = instruction.get_opcode()
    while opcode != STOP:
        if last_output != 0:
            raise Exception("Output should be 0, but was " + str(last_output))

        result = opcode_switcher.get(opcode, lambda: "Invalid opcode" + opcode)()
        index = result[0]
        if len(result) == 2:
            last_output = result[1]

        instruction = Instruction.get_instruction(str(ints[index]))
        opcode = instruction.get_opcode()
    return last_output


ADD = "01"
MULTIPLY = "02"
INPUT = "03"
OUTPUT = "04"
JUMP_IF_TRUE = "05"
JUMP_IF_FALSE = "06"
LESS_THAN = "07"
EQUALS = "08"
STOP = "99"

PARAM_MODE_LOOKUP = "0"
PARAM_MODE_DIRECT = "1"
