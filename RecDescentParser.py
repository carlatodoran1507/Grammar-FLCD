from enum import Enum


class ParserState(Enum):
    normal = 1
    back = 2
    final = 3
    error = 4

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

    # todo Carla: (expand, momentary insuccess, another try)
    def expand(self):
        non_terminal_value = self.input_stack.pop(0)
        production = self.grammar.get_production_of_non_terminal(non_terminal_value)
        self.working_stack.append((non_terminal_value, production))

    def momentary_insuccess(self):
        self.state = ParserState.back

    def another_try(self):
