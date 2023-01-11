import pandas as pd


class ParserOutput:
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, work_stack):
        start_symbol = self.grammar.get_start_symbol()
        # Create a table with the starting symbol
        table_index = 1
        table = [(table_index, start_symbol, 0, 0)]

        # Keep a list of (current_parse_element, index_in_table)
        current_elements = [(start_symbol, table_index)]
        for item in work_stack:
            if item in self.grammar.get_terminals() or (item == ''):
                if current_elements[0][0] == item:
                    current_elements.pop(0)
                else:
                    raise Exception(
                        f"Element and current values do not match: item={item}, current_elements={current_elements}")
            else:
                product_start, product_result = item

                search_index = None
                for index, node in enumerate(current_elements):
                    if product_start == node[0]:
                        search_index = index
                        break

                if search_index is None:
                    raise Exception("Element and current values do not match")

                kids = []
                # Get the children and add them in the table
                for index, result in enumerate(product_result):
                    parent = current_elements[search_index][1]
                    right_sibling = table_index if index - 1 >= 0 else 0
                    if result != '':
                        table.append((table_index + 1, result, parent, right_sibling))
                        kids.append((result, table_index + 1))
                    else:
                        table.append((table_index + 1, 'epsilon', parent, right_sibling))
                    table_index += 1
                current_elements = current_elements[:search_index] + kids + current_elements[search_index + 1:]

        return table

    @staticmethod
    def print_table(table):
        headers = ['Index', 'Info', 'Parent', 'Right sibling']
        df = pd.DataFrame(table, columns=headers)
        print(df.to_string(index=False))

    @staticmethod
    def print_table_to_file(table, filename):
        headers = ['Index', 'Info', 'Parent', 'Right sibling']
        df = pd.DataFrame(table, columns=headers)
        with open(filename, 'w') as output:
            output.write(df.to_string(index=False))
