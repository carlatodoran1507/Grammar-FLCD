class Grammar:
    #     read a grammar from file, print set of nonterminals, set of terminals,
    #     set of productions, productions for a given nonterminal, CFG check
    def __init__(self):
        self.__start_symbol = None
        self.__productions = {}
        self.__non_terminals = []
        self.__terminals = []

    def read_from_file(self, filename):
        with open(filename) as inp_file:
            self.__non_terminals = [non_terminal for non_terminal in inp_file.readline().strip().split()]
            self.__terminals = [terminal for terminal in inp_file.readline().strip().split()]
            self.__start_symbol = inp_file.readline().strip().split()[0]

            # Read the productions
            for line in inp_file.readlines():
                if len(line) < 2:
                    continue
                lhs, rhs = line.strip().split('->')
                key = lhs.strip()
                values = [result.strip().split() for result in rhs.strip().split(' | ')]
                self.__productions[key] = values
                # print(lhs, values)

    def get_non_terminals(self):
        return self.__non_terminals

    def get_terminals(self):
        return self.__terminals

    def get_productions(self):
        return self.__productions

    def get_production_of_non_terminal(self, terminal):
        return self.__productions[terminal]

    def is_cfg(self):
        for key in self.__productions.keys():
            if ' ' in key:
                return False
        return True




