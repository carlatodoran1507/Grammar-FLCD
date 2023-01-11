from enum import Enum
from ParserOutput import ParserOutput


class ParserState(Enum):
    normal = 1
    back = 2
    final = 3
    error = 4


def find_next_production(list_prod, prod):
    # Finds the next production in the list_prod, following prod
    # If the received production is the last, the result is -1
    for index, element in enumerate(list_prod):
        if element == prod:
            if index + 1 >= len(list_prod):
                return -1
            return list_prod[index + 1]
    return -1


class RecDescentParser:
    def __init__(self, grammar):
        self.__grammar = grammar
        self.__state = ParserState.normal
        self.__position_input = 1
        self.__working_stack = []
        self.__input_stack = [grammar.get_start_symbol()]
        self.__parser = ParserOutput(grammar)

    def __advance(self):
        self.__position_input += 1
        terminal_value = self.__input_stack.pop(0)
        self.__working_stack.append(terminal_value)

    def __back(self):
        self.__position_input -= 1
        terminal_value = self.__working_stack.pop()
        self.__input_stack.insert(0, terminal_value)

    def __success(self):
        self.__state = ParserState.final

    def __expand(self):
        non_terminal_value = self.__input_stack.pop(0)
        production = self.__grammar.get_production_of_non_terminal(non_terminal_value)[0]
        self.__working_stack.append((non_terminal_value, production))
        self.__input_stack = production + self.__input_stack

    def __momentary_insuccess(self):
        self.__state = ParserState.back

    def __another_try(self):
        production = self.__working_stack.pop()
        non_terminal_value, production_result = production
        all_ntv_production_results = self.__grammar.get_production_of_non_terminal(non_terminal_value)
        result = find_next_production(all_ntv_production_results, production_result)

        initial_state = self.__grammar.get_start_symbol()
        if self.__position_input == 1 and initial_state == non_terminal_value:
            self.__state = ParserState.error
            raise Exception('Error while doing another try. The working stack is: ', self.__working_stack)
        elif result != -1:
            self.__state = ParserState.normal
            self.__working_stack.append((non_terminal_value, result))
            self.__input_stack = self.__input_stack[len(production_result):]
            if '' not in result:
                self.__input_stack = result + self.__input_stack
        else:
            if '' not in production_result:
                self.__input_stack = self.__input_stack[len(production_result):]
            self.__input_stack.insert(0, non_terminal_value)

    def parse_descendant_recursive(self, word, output_file=None):
        self.__state = ParserState.normal
        self.__position_input = 1
        self.__working_stack = []
        self.__input_stack = [self.__grammar.get_start_symbol()]
        while self.__state != ParserState.final and self.__state != ParserState.error:
            if self.__state == ParserState.normal:
                if self.__position_input == len(word) + 1 and len(self.__input_stack) == 0:
                    self.__success()
                else:
                    if len(self.__input_stack) > 0:
                        head = self.__input_stack[0]
                        if head in self.__grammar.get_non_terminals():
                            self.__expand()
                        elif self.__position_input <= len(word) and head == word[self.__position_input - 1]:
                            self.__advance()
                        else:
                            self.__momentary_insuccess()
                    else:
                        self.__momentary_insuccess()
            else:
                if self.__state == ParserState.back:
                    head = self.__working_stack[-1]
                    if head in self.__grammar.get_terminals():
                        self.__back()
                    else:
                        self.__another_try()

        if self.__state == ParserState.error:
            raise Exception('Error while parsing. The working stack is: ', self.__working_stack)
        else:
            print('Sequence accepted')
            result_table = self.__parser.parse(self.__working_stack)
            self.__parser.print_table(result_table)
            if output_file is not None:
                self.__parser.print_table_to_file(result_table, output_file)
