from Grammar import Grammar
from RecDescentParser import RecDescentParser

if __name__ == '__main__':
    grammar = Grammar()
    grammar.read_from_file("input/g2.txt")
    rec_descent_parser = RecDescentParser(grammar)
    with open('input/pif.in') as inp:
        pif_data = [line.strip() for line in inp.readlines()]

    rec_descent_parser.parse_descendant_recursive(pif_data, 'out2.txt')

    # # ui = UI(grammar)
    # # ui.run()
    # parser = ParserOutput(grammar)
    # result_table = parser.parse([('S', ['a', 'S', 'b', 'S']),
    #                     'a',
    #                     ('S', ['a', 'S']),
    #                     'a',
    #                     ('S', ['c']),
    #                     'c',
    #                     'b',
    #                     ('S', ['c']),
    #                     'c'])
    # parser.print_table(result_table)
    # # parser.print_table_to_file(result_table, "test.txt")
