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
        self.parser = ParserOutput(grammar)

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

    def parse_descendant_recursive(self, word):
        self.state = ParserState.normal
        self.position_input = 1
        self.working_stack = []
        self.input_stack = [grammar.get_start_symbol()]
        # alpha and beta?
        while self.state != ParserState.final and self.state != ParserState.error:
            if self.state == ParserState.normal:
                head = self.input_stack[0]
                if self.position_input == len(word) + 1 and len(self.input_stack) == 0:
                    self.success()
                elif head in self.grammar.get_non_terminals():
                    self.expand()
                elif head == word[self.position_input]:
                    self.advance()
                else:
                    self.momentary_insuccess()
            else:
                if self.state == ParserState.back:
                    head = self.working_stack[0]
                    if head == word[self.position_input]:
                        self.back()
                    else:
                        self.another_try()

        if self.state == ParserState.error:
            raise Exception('Error while parsing')
            # or print here?
        else:
            print('Sequence accepted')
            result_table = self.parser.parse(self.working_stack)
            print(result_table)
