from enum import Enum


class ParserState(Enum):
    normal = 1
    back = 2
    final = 3
    error = 4


def find_index(list_prod, prod):
    for index, element in enumerate(list_prod):
        if element == prod:
            if index + 1 > len(list_prod):
                return -1
            return list_prod[index + 1]
    return -1


class RecDescentParser:
    def __init__(self, grammar, input_seq):
        self.grammar = grammar
        self.state = ParserState.normal
        self.position_input = 1
        self.working_stack = []
        self.input_stack = [grammar.get_start_symbol()]
        self.input_seq = input_seq

    # todo Liviu: (advance, back, success)
    def advance(self):
        self.position_input += 1
        terminal_value = self.input_stack.pop(0)
        self.working_stack.append(terminal_value)

    def back(self):
        self.position_input -= 1
        terminal_value = self.working_stack.pop()
        self.input_stack.insert(0, terminal_value)

    def success(self):
        self.state = ParserState.final

    # todo Carla: (expand, momentary insuccess, another try)
    def expand(self):
        non_terminal_value = self.input_stack.pop(0)
        production = self.grammar.get_production_of_non_terminal(non_terminal_value)[0]
        self.working_stack.append((non_terminal_value, production))

    def momentary_insuccess(self):
        self.state = ParserState.back

    def another_try(self):
        production = self.working_stack.pop()
        non_terminal_value = production[0]
        productions = self.grammar.get_production_of_non_terminal(non_terminal_value)
        result = find_index(productions, production[1])

        initial_state = self.grammar.get_start_symbol()
        if self.position_input == 1 and initial_state == non_terminal_value:
            self.state = ParserState.error
            raise Exception('Error')
        elif result != -1:
            self.state = ParserState.normal
            self.working_stack.append((non_terminal_value, result))
            self.input_stack.pop(0)
            self.input_stack.insert(0, result)
        else:
            self.input_stack.insert(0, non_terminal_value)
