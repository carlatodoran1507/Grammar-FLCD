class UI:
    def __init__(self, grammar):
        self.__grammar = grammar

    def __read_from_file(self):
        filename = input('Enter the filename: ')
        self.__grammar.read_from_file(filename)
        print('Read successfully')

    def __display_nonterminals(self):
        print('The nonterminals are: ' + ' '.join(self.__grammar.get_non_terminals()))

    def __display_terminals(self):
        print('The terminals are: ' + ' '.join(self.__grammar.get_terminals()))

    def __display_productions(self):
        productions = self.__grammar.get_productions()
        print('The productions are: ')
        for lhs, rhs in productions.items():
            print(lhs, rhs)

    def __display_productions_for_nt(self):
        nonterminal = input('Input the nonterminal: ')
        for production in self.__grammar.get_production_of_non_terminal(nonterminal):
            print(production)

    def __check_cfg(self):
        if self.__grammar.is_cfg():
            print('The grammar is a CFG')
        else:
            print('The grammar is a CFG')

    @staticmethod
    def __print_menu():
        print('0. Close the menu')
        print('1. Read the grammar from a given file')
        print('2. Display the nonterminals of the grammar')
        print('3. Display the terminals of the grammar')
        print('4. Display the productions of the grammar')
        print('5. Display the productions for a given nonterminal')
        print('6. Check if the grammar is CFG')

    def run(self):
        options = {'1': self.__read_from_file, '2': self.__display_nonterminals, '3': self.__display_terminals,
                   '4': self.__display_productions, '5': self.__display_productions_for_nt, '6': self.__check_cfg}

        is_over = False

        while not is_over:
            self.__print_menu()
            user_input = input('Enter your option: ').strip()
            if user_input == '0':
                is_over = True
            elif user_input in options:
                options[user_input]()
                print('\n')
            else:
                print('Incorrect input! Please try again')