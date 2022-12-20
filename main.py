from Grammar import Grammar
from UI import UI
from ParserOutput import ParserOutput
from RecDescentParser import RecDescentParser

if __name__ == '__main__':
    grammar = Grammar()
    grammar.read_from_file("input/g4.txt")
    rec_descent_parser = RecDescentParser(grammar)
    rec_descent_parser.parse_descendant_recursive('aacbc')

