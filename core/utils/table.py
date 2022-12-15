# import termtables as tt
from prettytable import PrettyTable


# def table_print(table: dict):
#     if table['value']:
#         tt.print(table['value'], header=table['header'], style=tt.styles.rounded)


def table_print(table: dict):
    if table['value']:
        x = PrettyTable(table['header'])
        for i in table['value']:
            x.add_row(i)
        print(x)
