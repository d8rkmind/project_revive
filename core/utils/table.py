import termtables as tt


def table_print(table: dict):
    if table['value']:
        tt.print(table['value'], header=table['header'], style=tt.styles.rounded)
