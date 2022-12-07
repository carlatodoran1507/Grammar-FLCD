from Grammar import Grammar
from RecDescentParser import RecDescentParser, ParserState


def test_advance():
    # given
    grammar = Grammar()
    parser = RecDescentParser(grammar, "aacbc")
    parser.state = ParserState.normal
    parser.position_input = 1
    parser.working_stack = ['S1']
    parser.input_stack = ['a', 'S', 'b', 'S']
    # when
    parser.advance()
    # then
    assert parser.state == ParserState.normal
    assert parser.position_input == 2
    assert parser.working_stack == ['S1', 'a']
    assert parser.input_stack == ['S', 'b', 'S']


def test_back():
    # given
    grammar = Grammar()
    parser = RecDescentParser(grammar, "aacbc")
    parser.state = ParserState.back
    parser.position_input = 5
    parser.working_stack = ['S1', 'a', 'S1', 'a', 'S3', 'c', 'b']
    parser.input_stack = ['S', 'b', 'S']
    # when
    parser.back()
    # then
    assert parser.state == ParserState.back
    assert parser.position_input == 4
    assert parser.working_stack == ['S1', 'a', 'S1', 'a', 'S3', 'c']
    assert parser.input_stack == ['b', 'S', 'b', 'S']


def test_success():
    # given
    grammar = Grammar()
    parser = RecDescentParser(grammar, "a")
    parser.state = ParserState.normal
    parser.position_input = 2
    parser.working_stack = ['S1', 'a']
    parser.input_stack = []
    # when
    parser.success()
    # then
    assert parser.state == ParserState.final
    assert parser.position_input == 2
    assert parser.working_stack == ['S1', 'a']
    assert parser.input_stack == []
